from odoo import models, fields

class CrmStageHistory(models.Model):
    _name = "crm.stage.history"
    _description = "CRM Stage Change History"

    lead_id = fields.Many2one('crm.lead', string="Lead", required=True, ondelete="cascade")
    previous_stage = fields.Char(string="Previous Stage")
    new_stage = fields.Char(string="New Stage")
    changed_by = fields.Many2one('res.users', string="Changed By", default=lambda self: self.env.user)
    changed_on = fields.Datetime(string="Changed On", default=fields.Datetime.now)
