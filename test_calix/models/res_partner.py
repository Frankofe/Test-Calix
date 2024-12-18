from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean(string='Credit Control', default=False)
    credit_group_ids = fields.Many2many(comodel_name='credit.group',string='Credit Groups id')


    @api.onchange('credit_control')
    def _onchange_credit_control(self):
        if not self.credit_control:
            self.credit_group_ids=False

