from odoo import models, fields, api
from datetime import datetime, timedelta
import workdays

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        lead = super().create(vals)
        if vals.get('stage_id'):
            stage_name = self.env['crm.stage'].browse(vals['stage_id']).name
            self.env['crm.stage.history'].create({
                'lead_id': lead.id,
                'previous_stage': '',
                'new_stage': stage_name,
                'changed_by': self.env.user.id,
            })
        return lead

    def write(self, vals):
        for lead in self:
            if 'stage_id' in vals and vals['stage_id'] != lead.stage_id.id:
                previous_stage = lead.stage_id.name if lead.stage_id else ''
                new_stage = self.env['crm.stage'].browse(vals['stage_id']).name
                self.env['crm.stage.history'].create({
                    'lead_id': lead.id,
                    'previous_stage': previous_stage,
                    'new_stage': new_stage,
                    'changed_by': self.env.user.id,
                })
        return super().write(vals)

    @api.model
    def archive_old_leads(self):
        today = datetime.today().date()
        threshold_date = workdays.workday(today, -30)  # Get date 30 working days ago
        old_leads = self.search([('create_date', '<=', threshold_date), ('active', '=', True)])
        old_leads.write({'active': False})
