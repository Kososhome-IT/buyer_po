from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cus_po_issue_date = fields.Date(string="PO Issue Date")
    cus_ex_fact_date = fields.Date(string="Vendor Ex-Fact Date")
    cus_proforma_number = fields.Char(string="Proforma Number")
    cus_buyer_order_no = fields.Char(string="Buyer Order No")
    cus_po_upload_no = fields.Char(string="PO Upload No")
    country_origin = fields.Many2one('library.country', string='Country of Origin')
    total_qty = fields.Float(
        string="Total Qty",
        compute="_compute_totals",
        store=True
    )

    total_cbm = fields.Float(
        string="Total CBM",
        compute="_compute_totals",
        store=True
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

    @api.depends('order_line.product_uom_qty', 'order_line.cbm')
    def _compute_totals(self):
        for order in self:
            order.total_qty = sum(order.order_line.mapped('product_uom_qty'))
            order.total_cbm = sum(order.order_line.mapped('cbm'))

    def action_view_inspections(self):
        return
   
