# -*- coding: utf-8 -*-


from odoo import models, api, fields


class WhatsappSendMessage(models.TransientModel):

    _name = 'whatsapp.message.wizard'
    _description = "Whatsapp Wizard"

    sale_order = fields.Many2one('sale.order', string="Recipient")
    user_id = fields.Many2one('sale_order.partner_id', string="Recipient")
    # mobile = fields.Char(related='user_id.mobile', required=True)
    message = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message and self.mobile:
            # message_string = "Hello *{}*, your Invoice *{}* with amount *{} {}* is ready. \nYour invoice contains following items:\n {}".format(str(self.user_id.name),str(self.sale_order.sequence),str(self.sale_order.currency_id.symbol),str(self.amount_total))
            message_string = ""
            media_url = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'

            message_string = message_string[:(len(message_string) - 3)]
            document = {
                "link": "/home/cybrosys/Downloads/python_tutorial.pdf",
                "provider": {
                    "name": "tut"
                },
                "caption": "Check the pdf doc"
            }

            return {
                'type': 'ir.actions.act_url',
                # 'url': "https://api.whatsapp.com/send?phone="+self.user_id.mobile+"&text=" + message_string,
                'url': "https://api.whatsapp.com/send?phone="+self.user_id.mobile+"&text=" + document,

                'target': 'new',
                'res_id': self.id,
            }
