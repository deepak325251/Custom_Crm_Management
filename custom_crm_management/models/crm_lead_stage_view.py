from odoo import models, fields

class LeadStageView(models.Model):
    _name = 'lead.stage.view'
    _description = 'Lead Stage View'
    _auto = False  # Important: This tells Odoo it's a SQL view

    lead_id = fields.Many2one('crm.lead', string='Lead')
    lead_name = fields.Char(string='Lead Name')
    current_stage = fields.Char(string='Current Stage')
    last_changed_stage = fields.Char(string='Last Changed Stage')
    changed_by = fields.Many2one('res.users', string='Changed By')
    changed_on = fields.Datetime(string='Changed On')

    def init(self):
        self.env.cr.execute("""
                    CREATE OR REPLACE VIEW lead_stage_view AS (
                        SELECT
                            row_number() OVER () AS id,
                            l.id AS lead_id,
                            l.name AS lead_name,
                            l.stage_id::varchar AS current_stage,  -- fallback if you need stage name, adjust if needed
                            h_new.new_stage AS last_changed_stage,
                            h_new.changed_by AS changed_by,
                            h_new.changed_on AS changed_on
                        FROM crm_lead l
                        LEFT JOIN (
                            SELECT DISTINCT ON (lead_id) *
                            FROM crm_stage_history
                            ORDER BY lead_id, changed_on DESC
                        ) h_new ON l.id = h_new.lead_id
                    )
                """)