from odoo import models, fields, api, _ 

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_channels_id = fields.Many2one(comodel_name='sales.channel',string='Channel id')

    @api.onchange('sales_channels_id')
    def _onchange_sales_channels_id(self):
        if self.sales_channels_id:
            self.warehouse_id = self.sales_channels_id.deposit.id

    def _prepare_invoice(self):
        res= super(SaleOrder, self)._prepare_invoice()
        if self.sales_channels_id:
            res['sales_channels_id']=self.sales_channels_id.id
            res['journal_id']=self.sales_channels_id.journal_id.id

        return res