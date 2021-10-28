# -*- coding: utf-8 -*-
import requests

from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
import logging
import base64

_logger = logging.getLogger(__name__)


class WebHook(http.Controller):
    @http.route('/products', type='json', auth='none', methods=['GET', 'POST'], csrf=False)
    def get_create_product_webhook_url__(self, *args, **kwargs):
        brand_obj = request.env['product.brand']
        subtype_obj = request.env['product.subtype']
        tlc_obj = request.env['product.tlc']
        subtype_list = []
        brand_list = []
        tlc_list = []
        attr_info = []
        woo_publish = False
        instance_id = request.env['woo.commerce'].with_user(SUPERUSER_ID).search([('active', '=', True)], limit=1)
        woocommerce_ids = request.env['product.template'].with_user(SUPERUSER_ID).search([])
        woo_ids = woocommerce_ids.mapped('woo_id')
        try:
            if str(request.jsonrequest.get('id')) not in woo_ids:
                if request.jsonrequest['parent_id'] == 0:
                    active_id = instance_id.id
                    if request.jsonrequest.get('status') == 'publish':
                        woo_publish = True
                    elif request.jsonrequest.get('status') == 'private':
                        woo_publish = False
                    def_id = False
                    if request.jsonrequest.get('default_attributes'):
                        default_att = request.jsonrequest.get('default_attributes')[0]
                        def_option = default_att.get('option')
                        def_id = request.env['product.attribute.value'].with_user(SUPERUSER_ID).search([('name', '=', def_option)])
                    for attr in request.jsonrequest.get('attributes'):
                        if attr.get('name') == 'Brand':
                            brand_ids = brand_obj.with_user(SUPERUSER_ID).search([])
                            brand_woo_ids = brand_ids.mapped('brand')
                            for option in attr.get('options'):
                                if option not in brand_woo_ids:
                                    brand_id = brand_obj.with_user(SUPERUSER_ID).create({
                                        'brand': option,
                                        'woo_id': str(attr.get('id')),
                                        'instance_id': instance_id.id,
                                    })
                                else:
                                    brand_id = brand_ids.filtered(lambda b: b.brand == option)
                                brand_list.append(brand_id.id)
                        if attr.get('name') == 'TLC':
                            tlc_ids = tlc_obj.with_user(SUPERUSER_ID).search([])
                            tlc_woo_ids = tlc_ids.mapped('name')
                            for option in attr.get('options'):
                                if option not in tlc_woo_ids:
                                    tlc_id = tlc_obj.with_user(SUPERUSER_ID).create({
                                        'name': option,
                                        'woo_id': str(attr.get('id')),
                                        'instance_id': instance_id.id,
                                    })
                                else:
                                    tlc_id = tlc_ids.filtered(lambda t: t.name == option)
                                tlc_list.append(tlc_id.id)
                        if attr.get('name') == 'Sub Type':
                            sub_type_ids = subtype_obj.with_user(SUPERUSER_ID).search([])
                            sub_type_woo_ids = sub_type_ids.mapped('subtype')
                            for option in attr.get('options'):
                                if option not in sub_type_woo_ids:
                                    sub_id = subtype_obj.with_user(SUPERUSER_ID).create({
                                        'subtype': option,
                                        'slug': option.lower(),
                                        'woo_id': str(attr.get('id')),
                                        'instance_id': instance_id.id,
                                    })
                                else:
                                    sub_id = sub_type_ids.filtered(lambda s: s.subtype == option)
                                subtype_list.append(sub_id.id)
                        var_info = []
                        attr_id = request.env['product.attribute'].with_user(SUPERUSER_ID).search(
                            [('woo_id', '=', attr.get('id')), ('instance_id', '=', active_id)])
                        if not attr_id:
                            vals_attr = {
                                'name': attr.get('name'),
                                'woo_id': attr.get('id'),
                                'instance_id': active_id,
                                'display_type': 'select',
                            }
                            attr_id = request.env['product.attribute'].with_user(SUPERUSER_ID).create(vals_attr)
                        qty_info = []
                        if attr.get('name') == 'Qty':
                            if attr.get('variation'):
                                for var in attr.get('options'):
                                    qty_info.append(var)
                                    if var not in attr_id.value_ids.mapped('name'):
                                        vals_line = (0, 0, {
                                            'name': var
                                        })
                                        var_info.append(vals_line)
                                if var_info:
                                    attr_id.with_user(SUPERUSER_ID).write({
                                        'value_ids': var_info,

                                    })
                                if attr_id.value_ids:
                                    vals_line = (0, 0, {
                                        'attribute_id': attr_id.id,
                                        'value_ids': attr_id.value_ids.filtered(lambda r: r.name in qty_info),
                                        'default_id': def_id.id if def_id else False
                                    })
                                    attr_info.append(vals_line)

                    caty_list = []
                    for caty in request.jsonrequest.get('categories'):
                        categ_id = caty.get('id')
                        caty_list.append(categ_id)
                    category_ids = request.env['woocommerce.category'].with_user(SUPERUSER_ID).search(
                        [('woo_id', 'in', caty_list)])
                    veg_value = False
                    if request.jsonrequest.get('attributes')[0].get(
                            'name') == 'veg':
                        if request.jsonrequest.get('attributes')[0].get('options')[0] == 'Yes':
                            veg_value = 'yes'

                        elif request.jsonrequest.get('attributes')[0].get('options')[0] == 'No':
                            veg_value = 'no'

                    output_img = ""
                    if request.jsonrequest['images']:

                        image_src = requests.get(request.jsonrequest['images'][0].get('src')).content

                        if image_src:

                            output_img = base64.b64encode(image_src)

                    vals = {
                        "name": request.jsonrequest['name'],
                        "woo_id": request.jsonrequest['id'],
                        "instance_id": active_id,
                        "list_price": request.jsonrequest['sale_price'],
                        "standard_price": request.jsonrequest['regular_price'],
                        "brand_ids": brand_list,
                        "type": 'product',
                        "woo_publish": woo_publish,
                        "sub_ids": subtype_list,
                        "tlc_ids": tlc_list,
                        "veg": veg_value,
                        'image_1920': output_img,
                        "woo_categ_ids": category_ids.ids,
                        'attribute_line_ids': attr_info if attr_info else False,
                    }

                    prd_id = request.env['product.template'].with_user(SUPERUSER_ID).create(vals)

                    for var_id in prd_id.product_variant_ids:
                        prd_opt = var_id.product_template_attribute_value_ids.mapped('name')
                        wcapi = instance_id.get_api()
                        result = wcapi.get("products/" + str(request.jsonrequest['id']) + "/variations").json()

                        for dit in result:
                            reg_price = float(dit.get('regular_price')) if dit.get('regular_price') else 0
                            woo_price = float(dit.get('price'))
                            options = [i['option'] for i in dit.get('attributes')]

                            if set(prd_opt) == set(options):
                                prd_id.with_user(SUPERUSER_ID).write({
                                    'woo_variant_check': True
                                })

                                var_id.with_user(SUPERUSER_ID).write({
                                    'woo_var_id': dit.get('id'),
                                    'lst_price': woo_price,
                                    'barcode': dit.get('sku') if dit.get('sku') else "",
                                    'regular_price': reg_price,
                                })
                else:
                    prd_woo_id = request.jsonrequest['parent_id']
                    prd_id = request.env['product.template'].with_user(SUPERUSER_ID).search([('woo_id', '=', int(prd_woo_id))])
                    for var_id in prd_id.product_variant_ids:
                        prd_opt = var_id.product_template_attribute_value_ids.mapped('name')
                        dit = request.jsonrequest
                        reg_price = float(dit.get('regular_price')) if dit.get('regular_price') else 0
                        woo_price = float(dit.get('price'))
                        options = [i['option'] for i in dit.get('attributes')]

                        if set(prd_opt) == set(options):
                            prd_id.with_user(SUPERUSER_ID).write({
                                'woo_variant_check': True
                            })

                            var_id.with_user(SUPERUSER_ID).write({
                                'woo_var_id': dit.get('id'),
                                'lst_price': woo_price,
                                'barcode': dit.get('sku') if dit.get('sku') else "",
                                'regular_price': reg_price,

                            })
                return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/update_products', type='json', auth='none', method=['PUT'], csrf=False)
    def get_update_product_webhook_url__(self, *args, **kwargs):

        record = request.env['product.template'].with_user(SUPERUSER_ID).search(
            [('woo_id', '=', int(request.jsonrequest['id']))])

        brand_obj = request.env['product.brand']
        subtype_obj = request.env['product.subtype']
        tlc_obj = request.env['product.tlc']
        subtype_list = []
        brand_list = []
        tlc_list = []
        caty_list = []
        attr_info = []
        veg_value = False
        woo_publish = False
        def_id = False
        instance_id = request.env['woo.commerce'].with_user(SUPERUSER_ID).search([('active', '=', True)], limit=1)

        try:
            active_id = instance_id.id
            if request.jsonrequest.get('status') == 'publish':
                woo_publish = True
            elif request.jsonrequest.get('status') == 'private':
                woo_publish = False

            for caty in request.jsonrequest.get('categories'):
                categ_id = caty.get('id')
                caty_list.append(categ_id)
            category_ids = request.env['woocommerce.category'].with_user(SUPERUSER_ID).search(
                [('woo_id', 'in', caty_list)])
            if request.jsonrequest.get('default_attributes'):
                default_att = request.jsonrequest.get('default_attributes')[0]

                def_option = default_att.get('option')

                def_id = request.env['product.attribute.value'].with_user(SUPERUSER_ID).search([('name', '=', def_option)])

            for attr in request.jsonrequest.get('attributes'):

                if attr.get('name') == 'Brand':
                    brand_ids = brand_obj.with_user(SUPERUSER_ID).search([])
                    brand_woo_ids = brand_ids.mapped('brand')
                    for option in attr.get('options'):
                        if option not in brand_woo_ids:
                            brand_id = brand_obj.with_user(SUPERUSER_ID).create({
                                'brand': option,
                                'woo_id': str(attr.get('id')),
                                'instance_id': instance_id.id,
                            })
                        else:
                            brand_id = brand_ids.filtered(lambda b: b.brand == option)

                        brand_list.append(brand_id.id)

                elif attr.get('name') == 'TLC':
                    tlc_ids = tlc_obj.with_user(SUPERUSER_ID).search([])
                    tlc_woo_ids = tlc_ids.mapped('name')
                    for option in attr.get('options'):
                        if option not in tlc_woo_ids:
                            tlc_id = tlc_obj.with_user(SUPERUSER_ID).create({
                                'name': option,
                                'woo_id': str(attr.get('id')),
                                'instance_id': instance_id.id,
                            })
                        else:
                            tlc_id = tlc_ids.filtered(lambda t: t.name == option)

                        tlc_list.append(tlc_id.id)

                elif attr.get('name') == 'Sub Type':
                    sub_type_ids = subtype_obj.with_user(SUPERUSER_ID).search([])
                    sub_type_woo_ids = sub_type_ids.mapped('subtype')
                    for option in attr.get('options'):
                        if option not in sub_type_woo_ids:
                            sub_id = subtype_obj.with_user(SUPERUSER_ID).create({
                                'subtype': option,
                                'slug': option.lower(),
                                'woo_id': str(attr.get('id')),
                                'instance_id': instance_id.id,
                            })
                        else:
                            sub_id = sub_type_ids.filtered(lambda s: s.subtype == option)

                        subtype_list.append(sub_id.id)

                elif attr.get('name') == 'veg':
                    veg_val = attr.get('options')[0]
                    if veg_val == "Yes":
                        veg_value = 'yes'
                    elif veg_val == "No":
                        veg_value = 'no'

                elif attr.get('name') == 'Qty':
                    var_info = []
                    attr_info = []
                    attr_id = request.env['product.attribute'].with_user(SUPERUSER_ID).search(
                        [('woo_id', '=', attr.get('id')), ('instance_id', '=', active_id)])

                    qty_info = []

                    if attr.get('variation'):

                        for var in attr.get('options'):

                            qty_info.append(var)

                            if var not in attr_id.value_ids.mapped('name'):
                                vals_line = (0, 0, {
                                    'name': var
                                })
                                var_info.append(vals_line)

                        if var_info:

                            attr_id.with_user(SUPERUSER_ID).write({
                                'value_ids': var_info
                            })

                        if attr_id.value_ids:
                            vals_line = (0, 0, {
                                'attribute_id': attr_id.id,
                                'value_ids': attr_id.value_ids.filtered(lambda r: r.name in qty_info),
                                'default_id': def_id.id if def_id else False
                            })
                            attr_info.append(vals_line)

            output_img = ""
            if request.jsonrequest['images']:
                image_src = requests.get(request.jsonrequest['images'][0].get('src')).content
                output_img = ""
                if image_src:
                    output_img = base64.b64encode(image_src)
            record.with_user(SUPERUSER_ID).with_context({'webhook': True}).write({
                'name': request.jsonrequest.get('name'),
                'image_1920': output_img,
                'list_price': request.jsonrequest.get('sale_price'),
                'standard_price': request.jsonrequest.get('regular_price'),
                'brand_ids': [(6, 0, brand_list)],
                'sub_ids': [(6, 0, subtype_list)],
                'woo_publish': woo_publish,
                'tlc_ids': [(6, 0, tlc_list)],
                'woo_categ_ids': [(6, 0, category_ids.ids)],
                'veg': veg_value,
                'attribute_line_ids': [(6, 0, attr_info)],
            })

            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/delete_products', type='json', auth='none', method=['DELETE'], csrf=False)
    def get_delete_product_webhook_url__(self, *args, **kwargs):
        try:
            record = request.env['product.template'].with_user(SUPERUSER_ID).search(
                [('woo_id', '=', int(request.jsonrequest['id']))])
            record.active = False
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/coupons', type='json', auth='none', methods=['GET', 'POST'], csrf=False)
    def get_create_coupon_webhook_url__(self, *args, **kwargs):

        try:
            request.env['coupon.coupon'].with_user(SUPERUSER_ID).create({
                "woo_id": request.jsonrequest['id'],
                "code": request.jsonrequest['code'],
                "expiration_date": request.jsonrequest['date_expires'],
            })
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/update_coupons', type='json', auth='none', method=['PUT'], csrf=False)
    def get_update_coupon_webhook_url__(self, *args, **kwargs):

        record = request.env['coupon.coupon'].with_user(SUPERUSER_ID).search(
            [('woo_id', '=', int(request.jsonrequest['id']))])
        try:
            record.with_user(SUPERUSER_ID).write({'code': request.jsonrequest['code']})
            record.with_user(SUPERUSER_ID).write({'expiration_date': request.jsonrequest['date_expires']})
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/delete_coupons', type='json', auth='none', method=['DELETE'], csrf=False)
    def get_delete_coupon_webhook_url__(self, *args, **kwargs):

        try:
            record = request.env['coupon.coupon'].with_user(SUPERUSER_ID).search(
                [('woo_id', '=', int(request.jsonrequest['id']))])
            record.unlink()
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/customers', type='json', auth='none', method=['GET', 'POST'],
                csrf=False)
    def get_create_customer_webhook_url__(self, *args, **kwargs):

        try:
            vals = {}
            vals["woo_id"] = request.jsonrequest.get('id')
            vals["name"] = request.jsonrequest.get('first_name') + ' ' + request.jsonrequest.get('last_name')
            vals["email"] = request.jsonrequest.get('email')
            vals["company_type"] = "person"
            vals["l10n_in_gst_treatment"] = "consumer"
            request.env['res.partner'].with_user(SUPERUSER_ID).create(vals)

            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/update_customers', type='json', auth='none', method=['PUT'],
                csrf=False)
    def get_update_customer_webhook_url__(self, *args, **kwargs):

        record = request.env['res.partner'].with_user(SUPERUSER_ID).search(
            [('woo_id', '=', int(request.jsonrequest['id']))])

        billing_country = request.env['res.country'].with_user(SUPERUSER_ID).search(
            [('name', '=', request.jsonrequest['billing'].get('country'))], limit=1)
        shipping_country = request.env['res.country'].with_user(SUPERUSER_ID).search(
            [('name', '=', request.jsonrequest['shipping'].get('country'))], limit=1)
        shipping_state = request.env['res.country.state'].with_user(SUPERUSER_ID).search(
            [('name', '=', request.jsonrequest['shipping'].get('state'))], limit=1)
        billing_state = request.env['res.country.state'].with_user(SUPERUSER_ID).search(
            [('name', '=', request.jsonrequest['billing'].get('state'))], limit=1)
        bill_name = request.jsonrequest['billing']['first_name'] + request.jsonrequest['billing']['last_name'] if \
            request.jsonrequest['billing']['first_name'] else ""
        bill_email = request.jsonrequest['billing']['email'] if request.jsonrequest['billing']['email'] else ""
        bill_street = request.jsonrequest['billing']['address_1'] if request.jsonrequest['billing']['address_1'] else ""
        bill_street2 = request.jsonrequest['billing']['address_2'] if request.jsonrequest['billing'][
            'address_2'] else ""
        bill_city = request.jsonrequest['billing']['city'] if request.jsonrequest['billing']['city'] else ""
        bill_zip = request.jsonrequest['billing']['postcode'] if request.jsonrequest['billing']['postcode'] else ""
        bill_phone = request.jsonrequest['billing']['phone'] if request.jsonrequest['billing']['phone'] else ""
        bill_values = {}
        if bill_name != "":
            bill_values = {
                'type': 'invoice',
                'parent_id': record.id,
                'name': bill_name,
                'email': bill_email,
                'street': bill_street,
                'street2': bill_street2,
                'city': bill_city,
                'zip': bill_zip,
                'country_id': billing_country.id if billing_country else False,
                'state_id': billing_state.id if billing_state else False,
                'phone': bill_phone,
            }

        ship_name = request.jsonrequest['shipping']['first_name'] + request.jsonrequest['shipping']['last_name'] if \
            request.jsonrequest['shipping']['first_name'] else ""
        ship_street = request.jsonrequest['shipping']['address_1'] if request.jsonrequest['shipping'][
            'address_1'] else ""
        ship_street2 = request.jsonrequest['shipping']['address_2'] if request.jsonrequest['shipping'][
            'address_2'] else ""
        ship_city = request.jsonrequest['shipping']['city'] if request.jsonrequest['shipping']['city'] else ""
        ship_zip = request.jsonrequest['shipping']['postcode'] if request.jsonrequest['shipping']['postcode'] else ""
        ship_values = {}
        if ship_name != "":
            ship_values = {
                'type': 'delivery',
                'parent_id': record.id,
                'name': ship_name,
                'street': ship_street,
                'street2': ship_street2,
                'city': ship_city,
                'zip': ship_zip,
                'country_id': shipping_country.id if shipping_country else False,
                'state_id': shipping_state.id if shipping_state else False,

            }

        try:
            record.with_user(SUPERUSER_ID).write(
                {'name': request.jsonrequest['first_name'] + ' ' + request.jsonrequest['last_name']})
            record.with_user(SUPERUSER_ID).write({'email': request.jsonrequest['email']})
            if bill_values and 'invoice' not in record.child_ids.mapped('type'):
                request.env['res.partner'].with_user(SUPERUSER_ID).create(bill_values)
            if ship_values and 'delivery' not in record.child_ids.mapped('type'):
                request.env['res.partner'].with_user(SUPERUSER_ID).create(ship_values)
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}

    @http.route('/delete_customers', type='json', auth='none', method=['DELETE'],
                csrf=False)
    def get_delete_customer_webhook_url__(self, *args, **kwargs):

        try:
            record = request.env['res.partner'].with_user(SUPERUSER_ID).search(
                [('woo_id', '=', int(request.jsonrequest['id']))])
            record.active = False
            return {"Message": "Success"}
        except Exception as e:
            return {"Message": "Something went wrong"}
