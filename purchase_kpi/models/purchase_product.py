# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID

from datetime import datetime
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
import datetime
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = "product.template"

    one_month = fields.Float('-1 Month')
    two_months = fields.Float('-2 Month')
    three_months = fields.Float('-3 Month')

    one_unit_sold = fields.Float('Unit Sold')
    two_unit_sold = fields.Float('Unit Sold')
    three_unit_sold = fields.Float('Unit Sold')

    one_sum_of_sales = fields.Float('Sum of Sales')
    two_sum_of_sales = fields.Float('Sum of Sales')
    three_sum_of_sales = fields.Float('Sum of Sales')

    one_diif_sales_cost = fields.Float('Sales Price - Cost ')
    two_diif_sales_cost = fields.Float('Sales Price - Cost ')
    three_diif_sales_cost = fields.Float('Sales Price - Cost ')

    last_year_one_month = fields.Float('-1 Month')
    last_year_two_months = fields.Float('-2 Month')
    last_year_three_months = fields.Float('-3 Month')

    last_year_one_unit_sold = fields.Float('Unit Sold')
    last_year_two_unit_sold = fields.Float('Unit Sold')
    last_year_three_unit_sold = fields.Float('Unit Sold')

    last_year_one_sum_of_sales = fields.Float('Sum of Sales')
    last_year_two_sum_of_sales = fields.Float('Sum of Sales')
    last_year_three_sum_of_sales = fields.Float('Sum of Sales')

    last_year_one_diif_sales_cost = fields.Float('Sales Price - Cost ')
    last_year_two_diif_sales_cost = fields.Float('Sales Price - Cost ')
    last_year_three_diif_sales_cost = fields.Float('Sales Price - Cost ')

    @api.model
    def get_values(self, a, b):
        for prods in self.search([]):
            one_month_ago = (datetime.datetime.now() - relativedelta(months=1)).month
            two_month_ago = (datetime.datetime.now() - relativedelta(months=2)).month
            three_month_ago = (datetime.datetime.now() - relativedelta(months=3)).month
            last_year = datetime.datetime.now().year - 1
            this_year = datetime.datetime.now().year

            self._cr.execute('''select product.id, product.name, sum(product_uom_qty) as quantity from
                                sale_order_line, product_template as product, sale_order where
                                sale_order_line.product_id = product.id AND
                                sale_order_line.order_id = sale_order.id AND
                                Extract(month FROM sale_order.date_order) = ''' + str(one_month_ago) + ''' AND
                                Extract(year FROM sale_order.date_order) = ''' + str(last_year) + '''
                                group by product.name , product.id
                                order by product.name''')

            last_year_one_month_result = self._cr.dictfetchall()
            for last_one_mo in last_year_one_month_result:
                if prods.id == last_one_mo['id']:
                    prods.write({'last_year_one_month': last_one_mo['quantity']})
                    prods.update({'last_year_one_month': last_one_mo['quantity']})

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity from sale_order,
                               sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(two_month_ago) + '''AND
                               Extract(year FROM sale_order.date_order) = ''' + str(last_year) + ''' AND
                               sale_order_line.order_id = sale_order.id
                               group by product.name , product.id
                               order by product.name
                            ''')

            last_year_two_month_result = self._cr.dictfetchall()
            for last_two_mo in last_year_two_month_result:
                if prods.id == last_two_mo['id']:
                    prods.write({'last_year_two_months': last_two_mo['quantity']})
                    prods.update({'last_year_two_months': last_two_mo['quantity']})

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity from sale_order,
                               sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(three_month_ago) + ''' AND
                               Extract(year FROM sale_order.date_order) = ''' + str(last_year) + ''' AND
                               sale_order_line.order_id = sale_order.id
                               group by product.name , product.id
                               order by product.name
                            ''')

            last_year_three_month_result = self._cr.dictfetchall()
            for last_three_mo in last_year_three_month_result:
                if prods.id == last_three_mo['id']:
                    prods.write({'last_year_three_months': last_three_mo['quantity']})
                    prods.update({'last_year_three_months': last_three_mo['quantity']})

            # ----------------------------------------------------------------------------------------------------------------------

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(one_month_ago) + ''' AND
                               Extract(year FROM sale_order.date_order) = ''' + str(last_year) + ''' AND
                               sale_order_line.order_id = sale_order.id AND
                               sale_order.state = 'sale'
                               group by product.name , product.id
                               order by product.name
                            ''')

            last_year_one_unit_solds = self._cr.dictfetchall()
            for last_year_one_uni in last_year_one_unit_solds:
                if prods.id == last_year_one_uni['id']:
                    # print('-------------------------------------------------', last_year_one_uni)
                    prods.write({'last_year_one_unit_sold': last_year_one_uni['quantity'],
                                 'last_year_one_sum_of_sales': last_year_one_uni['price'],
                                 'last_year_one_diif_sales_cost': last_year_one_uni['diff_sale'],
                                 })

                    prods.update({'last_year_one_unit_sold': last_year_one_uni['quantity'],
                                  'last_year_one_sum_of_sales': last_year_one_uni['price'],
                                  'last_year_one_diif_sales_cost': last_year_one_uni['diff_sale'],
                                  })

            self._cr.execute('''
                                select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                                sale_order_line.product_id = product.id AND
                                Extract(month FROM sale_order.date_order) = ''' + str(one_month_ago) + ''' AND
                                Extract(year FROM sale_order.date_order) = ''' + str(last_year) + ''' AND
                                sale_order_line.order_id = sale_order.id AND
                                sale_order.state = 'sale'
                                group by product.name , product.id
                                order by product.name
                            ''')

            last_year_two_unit_solds = self._cr.dictfetchall()

            for last_year_two_uni in last_year_two_unit_solds:
                if prods.id == last_year_two_uni['id']:
                    prods.write({'last_year_two_unit_sold': last_year_two_uni['quantity'],
                                 'last_year_two_sum_of_sales': last_year_two_uni['price'],
                                 'last_year_two_diif_sales_cost': last_year_two_uni['diff_sale'], })

                    prods.update({'last_year_two_unit_sold': last_year_two_uni['quantity'],
                                  'last_year_two_sum_of_sales': last_year_two_uni['price'],
                                  'last_year_two_diif_sales_cost': last_year_two_uni['diff_sale'], })

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(three_month_ago) + ''' AND
                               Extract(year FROM sale_order.date_order) = ''' + str(last_year) + ''' AND
                               sale_order_line.order_id = sale_order.id AND
                               sale_order.state = 'sale'
                               group by product.name , product.id
                               order by product.name
                            ''')

            last_year_three_unit_solds = self._cr.dictfetchall()
            # print('last_year_three_unit_solds', last_year_three_unit_solds)

            for last_year_three_uni in last_year_three_unit_solds:
                if prods.id == last_year_three_uni['id']:
                    prods.write({'last_year_three_unit_sold': last_year_three_uni['quantity'],
                                 'last_year_three_sum_of_sales': last_year_three_uni['price'],
                                 'last_year_three_diif_sales_cost': last_year_three_uni['diff_sale'],
                                 })

                    prods.update({'last_year_three_unit_sold': last_year_three_uni['quantity'],
                                  'last_year_three_sum_of_sales': last_year_three_uni['price'],
                                  'last_year_three_diif_sales_cost': last_year_three_uni['diff_sale'],
                                  })

        return self.env.ref('purchase_kpi.last_year_view_product_template_form_inherited').id

    @api.model
    def compute_one_month(self):
        for prods in self.search([]):
            one_month_ago = (datetime.datetime.now() - relativedelta(months=1)).month
            two_month_ago = (datetime.datetime.now() - relativedelta(months=2)).month
            three_month_ago = (datetime.datetime.now() - relativedelta(months=3)).month
            last_year = datetime.datetime.now().year - 1
            this_year = datetime.datetime.now().year
            # print('this_year', this_year)

            self._cr.execute('''select product.id, product.name, sum(product_uom_qty) as quantity from
                                sale_order_line, product_template as product, sale_order where
                                sale_order_line.product_id = product.id AND
                                sale_order_line.order_id = sale_order.id AND
                                Extract(month FROM sale_order.date_order) = ''' + str(one_month_ago) + '''   
                                                             
                                group by product.name , product.id
                                order by product.name''')

            one_month_result = self._cr.dictfetchall()
            for one_mo in one_month_result:
                if prods.id == one_mo['id']:
                    prods.write({'one_month': one_mo['quantity']})
                    prods.update({'one_month': one_mo['quantity']})

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity from sale_order,
                               sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(two_month_ago) + '''AND
                               sale_order_line.order_id = sale_order.id
                               group by product.name , product.id
                               order by product.name
                            ''')

            two_month_result = self._cr.dictfetchall()
            for two_mo in two_month_result:
                if prods.id == two_mo['id']:
                    prods.write({'two_months': two_mo['quantity']})
                    prods.update({'two_months': two_mo['quantity']})

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity from sale_order,
                               sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(three_month_ago) + ''' AND
                               sale_order_line.order_id = sale_order.id
                               group by product.name , product.id
                               order by product.name
                            ''')

            three_month_result = self._cr.dictfetchall()
            for three_mo in three_month_result:
                if prods.id == three_mo['id']:
                    prods.write({'three_months': three_mo['quantity']})
                    prods.update({'three_months': three_mo['quantity']})

            # ----------------------------------------------------------------------------------------------------------------------

            self._cr.execute('''
                              select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(one_month_ago) + ''' AND
                               Extract(year FROM sale_order.date_order) = ''' + str(this_year) + ''' AND
                               sale_order_line.order_id = sale_order.id AND
                               sale_order.state = 'sale' 
                               group by product.name , product.id
                               order by product.name
                            ''')

            one_unit_solds = self._cr.dictfetchall()
            for one_uni in one_unit_solds:
                if prods.id == one_uni['id']:
                    prods.write({'one_unit_sold': one_uni['quantity'],
                                 'one_sum_of_sales': one_uni['price'],
                                 'one_diif_sales_cost': one_uni['diff_sale'],
                                 })

                    prods.update({'one_unit_sold': one_uni['quantity'],
                                  'one_sum_of_sales': one_uni['price'],
                                  'one_diif_sales_cost': one_uni['diff_sale'],
                                  })

            self._cr.execute('''
                                select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                                sale_order_line.product_id = product.id AND
                                Extract(month FROM sale_order.date_order) = ''' + str(two_month_ago) + ''' AND
                                Extract(year FROM sale_order.date_order) = ''' + str(this_year) + ''' AND
                                sale_order_line.order_id = sale_order.id AND
                                sale_order.state = 'sale' 
                                group by product.name , product.id
                                order by product.name
                            ''')

            two_unit_solds = self._cr.dictfetchall()
            for two_uni in two_unit_solds:
                if prods.id == two_uni['id']:
                    prods.write({'two_unit_sold': two_uni['quantity'],
                                 'two_sum_of_sales': two_uni['price'],
                                 'two_diif_sales_cost': two_uni['diff_sale'], })

                    prods.update({'two_unit_sold': two_uni['quantity'],
                                  'two_sum_of_sales': two_uni['price'],
                                  'two_diif_sales_cost': two_uni['diff_sale'], })

            self._cr.execute('''
                               select product.id, product.name, sum(product_uom_qty) as quantity,
                                sum(sale_order_line.price_total - sale_order_line.purchase_price) as diff_sale,
                                sum(sale_order_line.price_total)as price from sale_order,
                                sale_order_line, product_template as product where
                               sale_order_line.product_id = product.id AND
                               Extract(month FROM sale_order.date_order) = ''' + str(three_month_ago) + ''' AND
                               Extract(year FROM sale_order.date_order) = ''' + str(this_year) + ''' AND
                               sale_order_line.order_id = sale_order.id AND
                               sale_order.state = 'sale' 
                               group by product.name , product.id
                               order by product.name
                            ''')

            three_unit_solds = self._cr.dictfetchall()
            for three_uni in three_unit_solds:
                if prods.id == three_uni['id']:
                    prods.write({'three_unit_sold': three_uni['quantity'],
                                 'three_sum_of_sales': three_uni['price'],
                                 'three_diif_sales_cost': three_uni['diff_sale'],
                                 })

                    prods.update({'three_unit_sold': three_uni['quantity'],
                                  'three_sum_of_sales': three_uni['price'],
                                  'three_diif_sales_cost': three_uni['diff_sale'],
                                  })


            self.get_values(self.env.user, self.env.uid)
