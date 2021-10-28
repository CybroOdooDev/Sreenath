from odoo import models, fields
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round
from collections import defaultdict
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall
from re import split as regex_split

from dateutil import relativedelta

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round
from odoo.tools.misc import format_date, OrderedSet


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    trolley_location_id = fields.Many2one("trolley.location", string="Trolley Location")
    move_for_backorder = fields.Boolean(default=False)


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    trolley_location_id = fields.Many2one("trolley.location", string="Trolley Location")
    pack_check = fields.Boolean(default=False)
    is_copy = fields.Boolean(default = False)
    package_id = fields.Many2one(
        'stock.quant.package', 'Source Package', ondelete='restrict',
        check_company=True,copy = False,
        domain="[('location_id', '=', location_id)]")
    result_package_id = fields.Many2one(
        'stock.quant.package', 'Destination Package',
        ondelete='restrict', required=False, check_company=True,copy = False,
        domain="['|', '|', ('location_id', '=', False), ('location_id', '=', location_dest_id), ('id', '=', package_id)]",
        help="If set, the operations are packed into this package")
    location_id = fields.Many2one('stock.location', 'From', check_company=True, required=True, readonly=True)
    location_dest_id = fields.Many2one('stock.location', 'To', check_company=True, required=True, readonly=True)
    picking_name = fields.Char(related='picking_id.picking_type_id.display_name')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=False)





