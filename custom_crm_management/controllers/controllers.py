from odoo import http, _
from odoo.http import request
import json

class CrmApiController(http.Controller):

    def _authenticate_request(self):
        """Checks API key in the request header."""
        auth_header = request.httprequest.headers.get('Authorization')
        stored_api_key = request.env['ir.config_parameter'].sudo().get_param('custom_crm.api_key')
        if not auth_header or not stored_api_key:
            return {
                'error': 'Unauthorized',
                'message': 'Invalid or missing API key',
                'status': 401
            }
        return None


    @http.route('/api/crm/leads', type='json', auth='public', csrf=False, methods=['GET'])
    def get_open_leads(self):
        try:
            auth_error = self._authenticate_request()

            if auth_error:
                return auth_error

            leads = request.env['crm.lead'].sudo().search([('stage_id.is_won', '=', False)])
            data = [{
                'id': lead.id,
                'name': lead.name,
                'stage': lead.stage_id.name if lead.stage_id else '',
                'assigned_user': lead.user_id.name if lead.user_id else ''
            } for lead in leads]

            return {'status': 200,'message':'All Leads Fetched!', 'data': data}
        except Exception as e:
            return {'error': 'Internal Server Error', 'message': str(e), 'status': 500}


    @http.route('/api/crm/create_lead', type='json', auth='public', csrf=False, methods=['POST'])
    def create_lead(self, **kwargs):
        auth_error = self._authenticate_request()
        if auth_error:
            return auth_error
        try:
            jdata = json.loads(request.httprequest.stream.read())
        except:
            try:
                jdata = json.loads(request.httprequest.data)
            except:
                jdata = {}
        try:
            name = jdata.get('name')
            email = jdata.get('email')
            phone = jdata.get('phone')
            contact_name = jdata.get('contact_name')
            print(name,email,phone,contact_name,"kgk")

            if not name:
                return {'error': 'Bad Request', 'message': 'Lead name is required', 'status': 400}

            lead_vals = {
                'name': name,
                'email_from': email,
                'phone': phone,
                'contact_name': contact_name
            }

            lead = request.env['crm.lead'].sudo().create(lead_vals)

            return {
                'status': 201,
                'message': 'Lead created successfully',
                'lead_id': lead.id
            }

        except Exception as e:
            return {'error': 'Internal Server Error', 'message': str(e), 'status': 500}

    @http.route('/api/crm/lead_stage_history/<int:lead_id>', type='json', auth='public', csrf=False, methods=['GET'])
    def lead_stage_history(self, lead_id):
        auth_error = self._authenticate_request()
        if auth_error:
            return auth_error
        try:

            lead = request.env['crm.lead'].sudo().search([('id', '=', lead_id)], limit=1)
            if not lead:
                return {'error': 'Not Found', 'message': f'Lead ID {lead_id} does not exist', 'status': 404}

            history = request.env['crm.stage.history'].sudo().search([('lead_id', '=', lead_id)], order='changed_on desc')

            history_data = [{
                'previous_stage': rec.previous_stage,
                'new_stage': rec.new_stage,
                'changed_by': rec.changed_by.name,
                'changed_on': rec.changed_on.strftime('%Y-%m-%d %H:%M:%S') if rec.changed_on else ''
            } for rec in history]

            return {'status': 200, 'lead_id': lead_id, 'history': history_data}
        except Exception as e:
            return {'error': 'Internal Server Error', 'message': str(e), 'status': 500}
