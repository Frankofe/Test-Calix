from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CreditGroupReport(models.AbstractModel):
    _name='report.test_calix.credit_group_report'
    _description='Credit Group Reports'

    @api.model
    def get_report_values(self,docids,data=None):
        docs=self.env['credit.group'].browse(docids)
        return{
            'doc_ids': docids,
            'doc_model': 'credit.group',
            'docs': docs,
            'data': data,
        }