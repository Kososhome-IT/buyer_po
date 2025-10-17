from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_image = fields.Image(
        related="product_id.image_128", 
        store=False,
        readonly=True
    )
    buyer_style_no = fields.Char(
        string="Buyer Style No",
        related="product_id.buyer_style_no",
        store=True,
        readonly=True
    )
    head_wood = fields.Boolean(string="Wood")
    head_upholstery = fields.Boolean(string="Upholstery")
    head_metal = fields.Boolean(string="Metal")
    head_glass = fields.Boolean(string="Glass")
    head_marble = fields.Boolean(string="Marble / Stone / Agate / Concrete")
    head_construction = fields.Boolean(string="Construction")
    head_finish = fields.Boolean(string="Finish")
    head_assembly = fields.Boolean(string="Assembly")
    head_paper = fields.Boolean(string="Paper")
    head_plastic = fields.Boolean(string="Plastic")
    head_resin = fields.Boolean(string="Resin")
    head_outdoor = fields.Boolean(string="Outdoor")
    head_handling_damage = fields.Boolean(string="Handling Damage")
    head_packaging_labeling = fields.Boolean(string="Packaging / Labeling")
    head_hardware = fields.Boolean(string="Hardware")
    head_lighting = fields.Boolean(string="Is Lighting")
    head_functionality = fields.Boolean(string="Functionality / Stability")
    head_wax = fields.Boolean(string="Wax")
    head_quality = fields.Boolean(string="Quality")
    head_testing = fields.Boolean(string="Testing")
    head_jute = fields.Boolean(string="Jute")
    head_mirrors = fields.Boolean(string="Mirrors")
    head_leather = fields.Boolean(string="Leather/Fabric")
    head_bone_horn_mop = fields.Boolean(string="Bone/Horn/MOP")
    head_cane_rattan = fields.Boolean(string="Cane/Rattan")

    vendor_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        store=True,
        readonly=True,  # keep False if you want to allow editing
    )
    item_description = fields.Char(
        string="Description",
        related='product_id.item_description',
        store=True
    )
    country_id = fields.Many2one(
        'library.country',
        string="Country Of Origin",
        related='product_id.country_id',
        store=True,
        readonly=True,
        tracking=True,
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string="Customer",
        domain=[('customer_rank', '>', 0)],
        tracking=True,
    )
    container_no = fields.Char(string="Container No")
    stuffed_date = fields.Char(string="Stuffed Dates")
    shipped_date = fields.Char(string="Shipped Dates")
    vendor_Ex_Fact_date = fields.Date(string="Vendor Ex-Fact Date" ,related='order_id.cus_ex_fact_date')
    cus_buyer_order_no = fields.Char(string="Buyer Order No",related='order_id.cus_buyer_order_no')
    vendor_product_code = fields.Char(string='Vendor Product Code', related='product_id.vendor_product_code',store=True, tracking=True)
    inner_Qty = fields.Char(string="Inner Qty")
    shipped_Qty = fields.Char(string="Shipped Qty")
    master_Qty = fields.Char(string="Master Qty")
    invoiced_Qty = fields.Char(string="Invoiced Quantity")
    discount_Qty = fields.Char(string="Discount (%)")
    # product_uom = fields.Selection([
    # ('pcs', 'PCS'),
    # ('dozen', 'Dozen')
    # ], string="Unit of Measure",related='product_id.product_uom', tracking=True)
    unit_CBM = fields.Float(string="Unit CBM")
    total_cbm = fields.Float(string="Total CBM", help="total cbm is unit cbm multiply with total quantity",store=True)
   
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
        help="Company owning this product",
    )
    # Pricing fields
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        related='order_id.currency_id',
        store=True,
        readonly=True,
    )        

    inline_insp_quantity = fields.Float(string="Inline Insp. Qty")
    midline_insp_quantity = fields.Float(string="Midline Insp. Qty")
    final_insp_quantity = fields.Float(string="Final Insp. Qty")
    oca_insp_quantity = fields.Float(string="OCA Insp. Qty")
    inline_bal_quantity = fields.Float(string="Inline Bal. Qty")
    midline_bal_quantity = fields.Float(string="Midline Bal Qty")
    final_bal_quantity = fields.Float(string="Final Bal Qty")
    OCA_bal_quantity = fields.Float(string="OCA Bal Qty")
    inspection = fields.Char(string="Inspection")
    order_state = fields.Selection(
        related='order_id.state',
        string="Order Status",
        store=True,
        readonly=True,
    )
    inspection_state = fields.Char(string="Inspection state")
    # order quotation feilds
    cus_po_issue_date = fields.Date(string="PO Issue Date" ,related='order_id.cus_po_issue_date')
    cus_ex_fact_date = fields.Date(string="Vendor Ex-Fact Date",related='order_id.cus_ex_fact_date')
    cus_buyer_order_no = fields.Char(string="Buyer Order No",related='order_id.cus_buyer_order_no')
    # conatainer
    stuffed_date = fields.Date(string="Stuffed Date")
    @api.onchange('order_id')
    def _onchange_vendor_product_domain(self):
        for line in self:
            vendor = line.order_id.vendor_id  # safe to access here
            if vendor:
                line.product_id = False  # reset product if vendor changes
                return {'domain': {'product_id': [('vendor_id', '=', vendor.id)]}}
            else:
                return {'domain': {'product_id': []}}  # show all products if no vendor
    @api.depends('product_id')
    def _compute_vendor_id(self):
        for line in self:
            if line.product_id and hasattr(line.product_id, 'vendor_id'):
                line.vendor_id = line.product_id.vendor_id.id
            else:
                line.vendor_id = False


    @api.onchange('product_id')
    def _onchange_product_id_set_heads(self):
        if self.product_id:
            self.head_wood = self.product_id.head_wood
            self.head_upholstery = self.product_id.head_upholstery
            self.head_metal = self.product_id.head_metal
            self.head_glass = self.product_id.head_glass
            self.head_marble = self.product_id.head_marble
            self.head_construction = self.product_id.head_construction
            self.head_finish = self.product_id.head_finish
            self.head_assembly = self.product_id.head_assembly
            self.head_paper = self.product_id.head_paper
            self.head_plastic = self.product_id.head_plastic
            self.head_resin = self.product_id.head_resin
            self.head_outdoor = self.product_id.head_outdoor
            self.head_handling_damage = self.product_id.head_handling_damage
            self.head_packaging_labeling = self.product_id.head_packaging_labeling
            self.head_hardware = self.product_id.head_hardware
            self.head_lighting = self.product_id.head_lighting
            self.head_functionality = self.product_id.head_functionality
            self.head_wax = self.product_id.head_wax
            self.head_quality = self.product_id.head_quality
            self.head_testing = self.product_id.head_testing
            self.head_jute = self.product_id.head_jute
            self.head_mirrors = self.product_id.head_mirrors
            self.head_leather = self.product_id.head_leather
            self.head_bone_horn_mop = self.product_id.head_bone_horn_mop
            self.head_cane_rattan = self.product_id.head_cane_rattan

     

          

