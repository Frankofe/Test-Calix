from odoo import models, fields, api, _ 

class AccountMove(models.Model):
    _inherit = 'account.move'

    sales_channels_id = fields.Many2one(comodel_name='sales.channel',string='Channel id')

    @api.onchange('sales_channels_id')
    def _onchange_sales_channels_id(self):
        if self.sales_channels_id:
            self.journal_id = self.sales_channels_id.journal_id.id

    
        