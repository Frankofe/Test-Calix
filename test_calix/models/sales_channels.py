from odoo import models, fields, api, _ 

class SalesChannels(models.Model):
    _name = 'sales.channel'
    _description = 'sales channels'


    name = fields.Char(string='Name')
    code = fields.Char(string='Code', readonly=True)
    deposit = fields.Many2one(comodel_name='stock.warehouse', string='Deposit')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')
    
    #@api.model
    #def _generate_code(self):
    #    sequence=self.env['ir.sequence'].next_by_code('sales.channel')
    #    return sequence
    
    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code']=self.env['ir.sequence'].next_by_code('sales.channel')
        return super(SalesChannels,self).create(vals)