from odoo import models, fields, api

class StuffedDate(models.Model):
    _name = 'stuffed_date.date'
    _description = 'Stuffed Dates'
    
    name = fields.Char('Description')
    date_value = fields.Date('Date')
    parent_id = fields.Many2one('sale.order.line', string='Parent') 