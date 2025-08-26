from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cus_po_issue_date = fields.Date(string="PO Issue Date")
    cus_ex_fact_date = fields.Date(string="Vendor Ex-Fact Date")
    cus_proforma_number = fields.Char(string="Proforma Number")
    cus_buyer_order_no = fields.Char(string="Buyer Order No")
    country_origin = fields.Many2one(
        'res.country',
        string='Country of Origin'
    )
    gst_treatment = fields.Char(
    related='partner_id.property_account_position_id.name',
    readonly=True,
    string='GST Treatment'
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
    inspection_count = fields.Integer(
        string="Inspections",
        compute='_compute_inspection_count',
        store=True
    )

    inspection_ids = fields.One2many(
    'inspection.inspection',
    'sale_order_id',
    string='Inspections'
    )

    @api.depends('inspection_ids')
    def _compute_inspection_count(self):
        for order in self:
            order.inspection_count = len(order.inspection_ids)

    def action_view_inspections(self):
        self.ensure_one()
        return {
            'name': 'Inspections',
            'type': 'ir.actions.act_window',
            'res_model': 'inspection.inspection',  # Replace with your model
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'target': 'current',
        }
