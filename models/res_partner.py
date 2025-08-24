from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # New checkbox field
    supplier_rank = fields.Boolean(string="Vendor", help="Check if this partner is a supplier/vendor")
