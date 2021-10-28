from odoo import api, fields, models, _
import json



class RouteMapping(models.Model):
    _name = 'route.mapping'
    _description = 'Route Mapping'

    name = fields.Char(string='Name',required=True)
    vehicle_id = fields.Many2one('fleet.vehicle',string='Vehicle Type')
    active = fields.Boolean(string="Active")

    del_date = fields.Date(string='Date')
    slot = fields.Selection([
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
        ('s4', 'S4')
    ], string='Slot')
    sale_order_ids = fields.Many2many('sale.order', string = 'Sale Orders')
    driver_code = fields.Char(string="Employee Code")
    driver_id = fields.Many2one('hr.employee',string='Delivery Boy')


    @api.model
    def _default_route(self):
        res = self.env.ref('wagon_basket_route_mapping.unassigned_route')
        orders = self.env['sale.order'].search([])
        for order in orders:
            if not order.route_id:
                order.route_id = res.id

    @api.onchange('driver_code')
    def _onchange_employee_code(self):
        if self.driver_code:
            employee = self.env['hr.employee'].search([('identification_id', '=', self.driver_code)])
            self.driver_id = employee.id if employee else False


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    last_assigned = fields.Boolean()
    driver_id = fields.Many2one('hr.employee')
    sequence = fields.Integer(string="Sequence",default=0)
    package_count = fields.Integer(string='Crates',compute='_compute_package_count')
    payment_state = fields.Selection([
        ('not-paid', 'Not Paid'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),

        ],string='State',compute='_compute_payment_state')

    def _compute_package_count(self):
        for rec in self:
            crate = self.env['stock.quant.package'].search([('sale_id','=',rec.id)])
            if crate:
                rec.package_count = len(crate)
            else:
                rec.package_count=0

    def _compute_payment_state(self):
        print('hii')
        for rec in self:
            if rec.invoice_status == 'invoiced' or  rec.invoice_status == 'to invoice' :
                inv_lst = []
                for inv in rec.invoice_ids:
                    inv_lst.append(inv)
                if any(i.payment_state == 'paid' or i.payment_state=='in_payment' for i in inv):
                    rec.payment_state = 'paid'
                elif any(i.payment_state == 'partial' for i in inv):
                    rec.payment_state = 'partial'
                else:
                    rec.payment_state = 'not-paid'
            else:
                rec.payment_state = 'not-paid'

    def find_route(self):
        domain = []
        routes = self.env['route.mapping'].search([])
        if routes:
            for route in routes:
                lst = []
                lst.append(route.name)
                lst.append(route.id)
                domain.append(lst)

        return domain

    is_deliver_map = fields.Boolean(default=False)

    # @api.depends('route_id')
    def _compute_route(self):
        print("hiiiiiiiiiiii",self)
        try:

            route = self.env.ref('wagon_basket_route_mapping.unassigned_route')
            #     print("kkkk",route)
            #     rec.route_id = route.id
            return route
        except:
            return False

    route_id = fields.Many2one('route.mapping',default =_compute_route ,store=True,copy=False)
    shift = fields.Selection([
        ('shift1', 'Shift 1'),
        ('shift2', 'ShiftT 2'),
        ], string='Shift', compute = 'find_Shift',store=True)
    slot = fields.Selection([
            ('s1', 'S1'),
            ('s2', 'S2'),
            ('s3', 'S3'),
            ('s4', 'S4')
        ], string = 'Slot',compute='find_Shift',store=True
    )
    del_date = fields.Date("Delivery",compute='_compute_del_date',store=True)

    @api.depends("date_order")
    def _compute_del_date(self):
        for rec in self:
            rec.del_date = rec.date_order


    @api.depends('del_time_slot')
    def find_Shift(self):
        for rec in self:
            if rec.del_time_slot:
                print("rec timeslot split",rec.del_time_slot.split(' - '))
                time = []
                for i in rec.del_time_slot.split(' - '):
                    print("li",i.split(":"))


                    time.append(i.split(":")[0])
                print("time",time)
                if int(time[0])>=7 and int(time[1])<=10:
                    rec.shift = 'shift1'
                    rec.slot = 's1'
                if int(time[0])>=10 and int(time[1])<=13:
                    rec.shift = 'shift1'
                    rec.slot = 's2'
                if int(time[0])>=15 and int(time[1])<=18:
                    rec.shift = 'shift2'
                    rec.slot = 's3'
                if int(time[0])>=18 and int(time[1])<=21:
                    rec.shift = 'shift2'
                    rec.slot = 's4'



    @api.model
    def get_route(self,vals):
        order = self.env['sale.order'].search([('id','=',int(vals['order_id']))])
        order.last_assigned = True
        orders = self.env['sale.order'].search([])

        prev_order_seq = 0
        for o in orders:
            if o.last_assigned == True and o.id != order.id:
                o.last_assigned = False
                prev_order_seq = o.sequence

        order.sequence=prev_order_seq+1
        route = self.env['route.mapping'].search([('id','=',int(vals['r_id']))])
        order.route_id = route.id
        del_order = self.env['stock.picking'].search([('sale_id','=',order.id),('picking_type_code','=','outgoing')])
        del_order.sudo().route_id = route.id
        del_order.sudo().employee_code = route.driver_code
        del_order.sudo().employee_id = route.driver_id.id
        order.driver_id = route.driver_id if route.driver_id else False

    @api.model
    def find_last_assigned(self):
        orders= self.env['sale.order'].search([])
        for order in orders:
            if order.last_assigned == True:
                return order


class ResPartner(models.Model):
    _inherit = 'res.partner'

    route_ids = fields.Many2many('route.mapping')









