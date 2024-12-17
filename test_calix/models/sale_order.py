from odoo import models, fields, api, _ 

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_channels_id = fields.Many2one(comodel_name='sales.channel',string='Channel id')

    @api.onchange('sales_channels_id')
    def _onchange_sales_channels_id(self):
        if self.sales_channels_id:
            self.warehouse_id = self.sales_channels_id.deposit.id
