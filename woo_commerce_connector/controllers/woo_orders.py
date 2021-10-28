# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
import dateutil.parser
import odoo
import pytz
import logging

_logger = logging.getLogger(__name__)


class WebHookOrders(http.Controller):
    @http.route('/orders', type='json', auth='none', method=['GET', 'POST'],
                csrf=False)
    def get_create_order_webhook_url__(self, *args, **kwargs):
        ''' creating order from woocommerce to odoo'''
        _logger.info("order.......%s",request.jsonrequest)

        try:
            customer_name = request.jsonrequest['shipping'].get('first_name') + ' ' + request.jsonrequest[
                'shipping'].get('last_name')
            partner_id = request.env['res.partner'].with_user(SUPERUSER_ID).search([('woo_id', '=',request.jsonrequest.get('customer_id') )],
                                                                                   limit=1)
            _logger.info("before.....")
            time_slot = request.jsonrequest['meta_data']
            _logger.info("time slot.. %s", time_slot)
            for rec in time_slot:
                _logger.info("rec... %s", rec)
                _logger.info("rec[key]... %s", rec['key'])
                if rec['key'] == 'delivery_time':
                    delivery_time_slot = rec['value']

                    _logger.info("del_time_slot.. %s", delivery_time_slot)
                else:
                    delivery_time_slot = ''
                    _logger.info("del_time_slot.. %s", delivery_time_slot)
                if rec['key'] == 'delivery_date':
                    delivery_date = rec['value']
                else:
                    delivery_date = False
            if not partner_id:
                partner_id = request.env['res.partner'].with_user(SUPERUSER_ID).create({'name': customer_name})
            partner_id.with_user(SUPERUSER_ID).update({
                'street':request.jsonrequest['shipping'].get('address_1'),
                'street2':request.jsonrequest['shipping'].get('address_2'),
                'city':request.jsonrequest['shipping'].get('city'),
                'state_id':request.env['res.country.state'].search([('name','=','Kerala')]).id if request.jsonrequest['shipping'].get('state') else False,
                'zip':request.jsonrequest['shipping'].get('postcode'),
                'country_id': request.env['res.country'].search(
                    [('code', '=', request.jsonrequest['shipping'].get('country'))]).id if request.jsonrequest[
                    'shipping'].get('country') else False,
                'phone':request.jsonrequest['billing'].get('phone'),
                'email':request.jsonrequest['billing'].get('email'),

            })
            so = request.env['sale.order'].with_user(SUPERUSER_ID).create({
                "partner_id": partner_id.id,
                "date_order": odoo.fields.Datetime.to_string(
                    dateutil.parser.parse(request.jsonrequest['date_created']).astimezone(pytz.utc)),
                "l10n_in_gst_treatment": "consumer",
                "woo_id": request.jsonrequest['id'],
                "del_time_slot": delivery_time_slot,
                "deliver_date": delivery_date,
            })
            _logger.info("so.. %s", so)
            line_items = request.jsonrequest.get('line_items')
            shipping_lines = request.jsonrequest.get('shipping_lines')
            if request.jsonrequest.get('line_items'):
                for line in line_items:
                    line_total = line.get('quantity') * line.get('price')

                    product_id = request.env['product.product'].with_user(SUPERUSER_ID).search(
                        [('woo_var_id', '=', line.get('variation_id'))])

                    if product_id:
                        so.write({
                            'order_line': [
                                (0, 0, {
                                    'name': product_id.name,
                                    'product_id': product_id.id,
                                    'product_uom_qty': line.get('quantity'),
                                    # 'price_unit': line.get('price'),
                                    'price_unit': line.get('price') + float(line.get('total_tax')) / line.get('quantity') if line.get('total_tax')!=0 else line.get('price'),
                                    'price_subtotal': line_total,
                                })
                            ],
                        })

            if shipping_lines:
                _logger.info("soo.. ", )
                for line in shipping_lines:
                    _logger.info("line.. %s", line)
                    deli_product_id = request.env['product.product'].with_user(SUPERUSER_ID).search([('name','=','Delivery Charges')])

                    _logger.info("deli_product_id....%s",deli_product_id)
                    so.write({
                        'order_line':[(0,0,
                                       {
                                       'name': deli_product_id.name,
                                       'product_id': deli_product_id.id,
                                       'product_uom_qty': 1,
                                      # 'price_unit': line.get('price'),
                                       'price_unit': line.get('total') + line.get('total_tax')

                    }
                    )]
                    })


            # if request.jsonrequest.get('status') == 'processing':
            so.action_confirm()

            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/update_orders', type='json', auth='none', method=['PUT'],
                csrf=False)
    def get_update_order_webhook_url__(self, *args, **kwargs):
        ''' updating order from woocommerce to odoo'''
        _logger.info("update order.......")
        print("orderr")

        record = request.env['sale.order'].with_user(SUPERUSER_ID).search(
            [('woo_id', '=', int(request.jsonrequest['id']))])

        customer_name = request.jsonrequest['shipping'].get('first_name') + ' ' + request.jsonrequest[
            'shipping'].get('last_name')
        partner_id = request.env['res.partner'].with_user(SUPERUSER_ID).search([('name', '=', customer_name)],
                                                                               limit=1)
        _logger.info("before update.....")
        time_slot = request.jsonrequest['meta_data']
        _logger.info("update time slot.. %s", time_slot)
        for rec in time_slot:
            _logger.info("update rec... %s", rec)
            _logger.info("update rec[key]... %s", rec['key'])
            if rec['key'] == 'delivery_time':
                delivery_time_slot = rec['value']

                _logger.info("update del_time_slot.. %s", delivery_time_slot)
            if rec['key'] == 'delivery_date':
                delivery_date = rec['value']
        if not partner_id:
            partner_id = request.env['res.partner'].with_user(SUPERUSER_ID).create({'name': customer_name})
        partner_id.with_user(SUPERUSER_ID).update({
            'street': request.jsonrequest['shipping'].get('address_1'),
            'street2': request.jsonrequest['shipping'].get('address_2'),
            'city': request.jsonrequest['shipping'].get('city'),
            'state_id': request.env['res.country.state'].search(
                [('name','=','Kerala')]).id if request.jsonrequest[
                'shipping'].get('state') else False,
            'zip': request.jsonrequest['shipping'].get('postcode'),
            'country_id': request.env['res.country'].search(
                [('code', '=', request.jsonrequest['shipping'].get('country'))]).id if request.jsonrequest[
                'shipping'].get('country') else False,
            'phone': request.jsonrequest['billing'].get('phone'),
            'email': request.jsonrequest['billing'].get('email'),

        })

        try:
            record.with_user(SUPERUSER_ID).write({'partner_id': partner_id})
            record.with_user(SUPERUSER_ID).write({'del_time_slot': delivery_time_slot,
                                                  'deliver_date':delivery_date})
            line_items = request.jsonrequest.get('line_items')
            shipping_lines = request.jsonrequest.get('shipping_lines')
            product_ids = record.order_line.mapped('product_id')
            if line_items:
                for line in line_items:
                    product_id = request.env['product.product'].with_user(SUPERUSER_ID).search(
                        [('woo_var_id', '=', line.get('variation_id'))])
                    if product_id.id not in product_ids.ids:
                        sale_order_line = request.env['sale.order.line'].with_user(SUPERUSER_ID).create({
                            'name': product_id.name,
                            'product_id': product_id.id,
                            'product_uom_qty': line.get('quantity'),
                            'price_unit': line.get('price')+ float(line.get('total_tax')) / line.get('quantity'),
                            'order_id': record.id
                        })
                    else:
                        order_line_id = record.order_line.filtered(lambda l: l.product_id.id == product_id.id)
                        order_line_id.with_user(SUPERUSER_ID).write({
                            'name': product_id.name,
                            'product_id': product_id.id,
                            'product_uom_qty': line.get('quantity'),
                            'price_unit': line.get('price')+ float(line.get('total_tax')) / line.get('quantity'),

                            'order_id': record.id,
                        })
            if shipping_lines:
                _logger.info("soo.. ", )
                for line in shipping_lines:
                    _logger.info("line.. %s", line)
                    deli_product_id = request.env['product.product'].with_user(SUPERUSER_ID).search(
                        [('name', '=', 'Delivery Charges')])

                    _logger.info("deli_product_id....%s", deli_product_id)
                    if deli_product_id.id not in product_ids.ids:
                        request.env['sale.order.line'].with_user(SUPERUSER_ID).create({
                            'name': deli_product_id.name,
                            'product_id': deli_product_id.id,
                            'product_uom_qty': 1,
                            'price_unit': line.get('total') + line.get('total_tax'),
                            'order_id': record.id
                        })
                    else:
                        order_line_id = record.order_line.filtered(lambda l: l.product_id.id == deli_product_id.id)
                        order_line_id.with_user(SUPERUSER_ID).write({
                            'name': deli_product_id.name,
                            'product_id': deli_product_id.id,
                            'product_uom_qty': 1,
                            'price_unit': line.get('total') + line.get('total_tax'),
                            'order_id': record.id,
                        })

            # if request.jsonrequest.get('status') == 'processing' and record.state == 'draft':
            record.action_confirm()

            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/delete_orders', type='json', auth='none', method=['DELETE'],
                csrf=False)
    def get_delete_order_webhook_url__(self, *args, **kwargs):
        ''' deleting order from woocommerce'''

        try:
            record = request.env['sale.order'].with_user(SUPERUSER_ID).search(
                [('woo_id', '=', int(request.jsonrequest['id']))])
            record.action_cancel()
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

