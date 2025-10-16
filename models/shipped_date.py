from odoo import models, fields, api

class ShippedDate(models.Model):
    _name = 'shipped_date.date'
    _description = 'shipped_date Dates'
    
    name = fields.Char('Description')
    date_value = fields.Date('Date')
    shipped_date_id = fields.Many2one('sale.order.line', string='Parent')