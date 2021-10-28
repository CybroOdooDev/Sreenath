from odoo import models, fields, api


class WooTlc(models.Model):
    _name = 'product.tlc'

    name = fields.Char("TLC", readonly=False)
    woo_id = fields.Char(string="Woo ID", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)

    def unlink(self):
        """
        For deleting on both instances.
        """
        for recd in self:
            if recd.woo_id:
                wcapi = recd.instance_id.get_api()
                attributes = wcapi.get("products/attributes").json()
                tlc_woo_id = False
                for attrs in attributes:
                    if attrs.get('name') == 'TLC':
                        tlc_woo_id = attrs.get('id')
                wcapi.delete("products/attributes/" + str(tlc_woo_id) + "/terms/" + recd.woo_id, params={"force": True}).json()
        return super(WooTlc, self).unlink()

    @api.model
    def create(self, vals):
        """
         For creating on both instances.
        """
        res = super(WooTlc, self).create(vals)
        if 'woo_id' not in vals.keys() and not res.woo_id:

            instance_id = self.instance_id.search([('active', '=', True)], limit=1)
            wcapi = instance_id.get_api()
            attributes = wcapi.get("products/attributes").json()
            tlc_woo_id = False
            for attrs in attributes:
                if attrs.get('name') == 'TLC':
                    tlc_woo_id = attrs.get('id')
            data = {
                "name": res.name,
            }
            attr_res = wcapi.post("products/attributes/" + str(tlc_woo_id) + "/terms", data).json()

            res.woo_id = str(attr_res.get('id'))
            res.instance_id = instance_id.id
        return res

    def write(self, vals):
        """
            For updating on both instances.
        """
        res = super(WooTlc, self).write(vals)
        instance_id = self.instance_id.search([('active', '=', True)], limit=1)
        wcapi = instance_id.get_api()
        attributes = wcapi.get("products/attributes").json()
        tlc_woo_id = False
        for attrs in attributes:
            if attrs.get('name') == 'TLC':
                tlc_woo_id = attrs.get('id')
        data = {
            "name": self.name,
        }
        attr_res = wcapi.put("products/attributes/" + str(tlc_woo_id) + "/terms/" + str(self.woo_id), data).json()

        return res
