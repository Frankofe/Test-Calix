from odoo import http, _
from odoo.http import request
from datetime import datetime


class CreditGroupController(http.Controller):

    @http.route(['/endpoint_credit_group'], type='json', auth='public', method=['POST'], csrf=False)
    def create_or_update_credit_group(self, **kwargs):
        errors=[]

        post_data = request.jsonrequest
        credit_groups=post_data.get('grupo_creditos', [])

        for group_data in credit_groups:
            name=group_data.get('name')
            code=group_data.get('codigo')
            sale_channel_id=group_data.get('canal')
            credit_global=group_data.get('credito_global')

            channel=request.env['sales.channel'].sudo().search([
                ('code', '=', sale_channel_id)
            ])

            if not channel:
                errors.append(
                    {
                        'status': '400',
                        'message': 'No se encontro el canal %s' %sale_channel_id,
                    }
                )
                continue

            credit_group=request.env['credit.group'].sudo().search([
                ('code', '=', code)
            ])

            if credit_group:
                credit_group.sudo().write(
                    {
                        'name': name,
                        'sale_channel_id': channel.id,
                        'credit_global': credit_global,                        
                    }
                )
            else:
                request.env['credit.group'].sudo().create(
                    {
                        'name': name,
                        'code': code,
                        'sale_channel_id': channel.id,
                        'credit_global': credit_global,                        
                    }
                )
        if errors:
            return {
                'status': 'error',
                'errors': errors,
            }
        return {
            'status': '200',
            'message': 'OK',
        }

        