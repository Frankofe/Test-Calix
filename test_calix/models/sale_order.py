from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_channels_id = fields.Many2one(comodel_name='sales.channel',string='Channel id')
    credit_control = fields.Boolean(related='partner_id.credit_control', string='Credit Control')
    credit_type = fields.Selection([
        ('no_limit', 'Without credit limit'),
        ('available_credit', 'Available credit'),
        ('blocked_credit', 'Blocked credit'),
    ], string='Credit Type', compute='_compute_credit_type')

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
    
    @api.depends('partner_id', 'sales_channels_id', 'amount_total')
    def _compute_credit_type(self):
        for order in self:
            credit_status = 'no_limit'

            if order.partner_id and order.sales_channels_id:
                credit_groups = order.partner_id.credit_group_ids


                if credit_groups:
                    credit_available = sum(group.credit_available for group in credit_groups)
                    
                    if order.amount_total > credit_available:
                        credit_status = 'blocked_credit'
                    else:
                        credit_status = 'available_credit'

            order.credit_type = credit_status
    
    def action_confirm(self):
        if self.credit_type == 'blocked_credit':
            raise ValidationError(_('This partner has blocked credit.'))
        res=super(SaleOrder,self).action_confirm()
        return res
    