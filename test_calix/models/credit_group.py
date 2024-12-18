from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = 'Credit Groups'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sale_channel_id = fields.Many2one(comodel_name='sales.channel', string='Sales channels', required=True)
    credit_global = fields.Monetary(string='Global Credit', required=True)
    credit_used = fields.Monetary(string='Used Credit', compute='_compute_credit_used', store=True)
    credit_available = fields.Monetary(string='Available Credit', compute='_compute_credit_available', store=True)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if '026' in record.code:
                raise ValidationError(_('The code cannot contain the sequence "026".'))
    
    @api.depends('credit_global', 'credit_used')
    def _compute_credit_available(self):
        for record in self:
            record.credit_available = record.credit_global - record.credit_used
    
    @api.depends('sale_channel_id')
    def _compute_credit_used(self):
        SaleOrder = self.env['sale.order']
        AccountMove = self.env['account.move']

        for record in self:
            total_confirmed_sales = sum(SaleOrder.search([
                ('sales_channels_id', '=', record.sale_channel_id.id),
                ('state', 'in', ['sale', 'done']),
                ('invoice_status', '=', 'to invoice')
            ]).mapped('amount_total'))

            total_unpaid_invoices = sum(AccountMove.search([
                ('sales_channels_id', '=', record.sale_channel_id.id),
                ('state', '=', 'posted'),
                ('payment_state', '!=', 'paid')
            ]).mapped('amount_residual'))

            record.credit_used = total_confirmed_sales + total_unpaid_invoices
