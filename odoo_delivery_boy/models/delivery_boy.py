"""Delivery Boy"""
import base64
import io
from PIL import Image

# -*- coding: utf-8 -*-

# 1 : imports of odoo
from odoo import models, fields, api ,_

class DeliveryBoyPickings(models.Model):
    _name = 'delivery.boy'

    name = fields.Char('Name')
    assigned_date = fields.Datetime(string='Delivery Date')
    commission_date = fields.Datetime(string='Commission Date')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    stock_picking_id = fields.Many2one('stock.picking', string='Pickings')
    partner_id = fields.Many2one('res.partner', string='Delivery Boy')
    commission_amount = fields.Float('Commission Amount')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancelled'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid')], string='state', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'delivery.boy') or _('New')
        res = super(DeliveryBoyPickings, self).create(vals)
        return res


    def action_delivery_pickings(self):
        for record in self:
            if record.stock_picking_id.state not in ['done', 'cancel']:
                record.stock_picking_id.action_set_quantities_to_reservation()
                record.stock_picking_id.button_validate()
                record.write({
                    'state': 'delivered',
                })

            # record.stock_picking_id.button_validate()
        # return

class DeliveryBoyCommission(models.Model):
    _name = 'delivery.boy.commission'

    name = fields.Char('Name')
    commission_type = fields.Selection([('order', 'Pay Per Order'), ('product', 'Pay Per Product'), ('product_category', 'Pay Per Product Category'),], string="Commission Type", default='order')
    commission_mode = fields.Selection([('fixed', 'Fixed'),('percentage', 'Percentage')], string="Commission Mode", default='fixed')
    partner_id = fields.Many2many('res.partner', string='Delivery Boy')
    product_id = fields.Many2one('product.product', string='Product')
    product_categ_id = fields.Many2one('product.category', string='Product Category')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        compute='_compute_company_id', inverse='_inverse_company_id', store=True, readonly=False, precompute=True,
        index=True,
    )

    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )
    commission_amount = fields.Monetary('Commission Amount', currency_field='company_currency_id', tracking=True)

    def _compute_company_id(self):
        for rec in self:
            rec.company_id = self.env.company

    @api.onchange('company_id')
    def _inverse_company_id(self):
        for rec in self:
            rec.company_id = self.env.company
