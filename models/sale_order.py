from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cus_po_issue_date = fields.Date(string="PO Issue Date")
    cus_ex_fact_date = fields.Date(string="Vendor Ex-Fact Date")
    cus_proforma_number = fields.Char(string="Proforma Number")
    cus_buyer_order_no = fields.Char(string="Buyer Order No")
    cus_po_upload_no = fields.Char(string="PO Upload No")
    country_origin = fields.Many2one(
        'res.country',
        string='Country of Origin'
    )
    gst_treatment = fields.Char(
    related='partner_id.property_account_position_id.name',
    readonly=True,
    string='GST Treatment'
    )
    inspection_count = fields.Integer(
        string="Inspections",
        store=True
    )
    date_order = fields.Datetime(
        string='Order Date',     
        readonly=False,            
        required=True
    )
    planning_days = fields.Integer(string='Planning Days')
    rev_vendor_ex_date = fields.Date(string='Rev. Vendor Ex Date')
    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('supplier_rank', '>', 0)]
    )

    def action_view_inspections(self):
        return
   
