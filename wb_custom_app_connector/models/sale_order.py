from odoo import models, fields, api
import requests


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def connect_to_api(self, payload=None):
        url = 'http://tr-ecom-be.herokuapp.com/api/v1/erp/order-update-notifications'

        search = self.env['api.backend'].search([('active','=',True)], limit=1)
        print("search", search)
        headers = {
            'X-ERP-JWT': '%s'%(search.token),
            'Content-Type': 'application/json',
        }
        response = requests.request('POST', url, headers=headers,
                                    data=payload)
        print("response", response.text)

    @api.constrains('state')
    def change_of_state(self):
        for rec in self:
            if rec.state == 'sale':
                payload = "{\n\"title\":\"%s placed successfully\",\n\"description\":\"Hi %s, Thank you for ordering. We received your order and will begin processing it soon\",\n\"imageUrl\":\"\",\n\"orderStatus\": \"success\",\n\"userId\": 12,\n\"orderId\": 14\n}"% (rec.name,rec.partner_id.name)

                rec.connect_to_api(payload=payload)
            if rec.state == 'cancel':
                payload = "{\n\"title\":\"%s cancelled successfully\",\n\"description\":\"Hi %s, Your order has been cancelled\",\n\"imageUrl\":\"\",\n\"orderStatus\": \"cancelled\",\n\"userId\": 12,\n\"orderId\": 14\n}"% (rec.name,rec.partner_id.name)

                rec.connect_to_api(payload=payload)

    def _find_delay(self):
        sale_orders = self.env['sale.order'].search([])
        for order in sale_orders:
            for picking in order.picking_ids:
                if picking.picking_type_code == 'outgoing' and picking.state != 'done':
                    expected = picking.sale_id.expected_date
                    print("hh",expected)
                    if expected:
                        if expected.date() < fields.Date.today():
                            delay_days = (fields.Date.today()-expected.date()).days
                            print("delay_days",delay_days)
                            payload = "{\n\"title\":\"%s Order Delayed\",\n\"description\":\"Hi %s, Your order is delayed by %s days\",\n\"imageUrl\":\"\",\n\"orderStatus\": \"delayed\",\n\"userId\": 12,\n\"orderId\": 14\n}" % (
                            order.name, order.partner_id.name,delay_days)
                            order.connect_to_api(payload=payload)



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('state')
    def change_of_del_state(self):
        for rec in self:
            if rec.sale_id and rec.picking_type_code=='outgoing':
                if rec.state == 'done':
                    payload = "{\n\"title\":\"%s delivered successfully\",\n\"description\":\"Hi %s, Your order has been delivered\",\n\"imageUrl\":\"\",\n\"orderStatus\": \"delivered\",\n\"userId\": 12,\n\"orderId\": 14\n}" % (
                    rec.sale_id.name, rec.partner_id.name)

                    rec.sale_id.connect_to_api(payload=payload)
            if rec.sale_id and rec.location_id==self.env.ref('stock.location_pack_zone'):
                if rec.state == 'done':
                    payload = "{\n\"title\":\"%s shipped successfully\",\n\"description\":\"Hi %s, Your order has been shipped\",\n\"imageUrl\":\"\",\n\"orderStatus\": \"shipped\",\n\"userId\": 12,\n\"orderId\": 14\n}" % (
                    rec.sale_id.name, rec.partner_id.name)

                    rec.sale_id.connect_to_api(payload=payload)





