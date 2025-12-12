from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    buyer_style_no = fields.Char(
        related="product_tmpl_id.buyer_style_no",
        store=True,
        readonly=True
    )

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Search by SKU, Internal Reference, Name"""
        args = args or []

        if name:
            domain = ['|', '|',
                      ('buyer_style_no', operator, name),
                      ('default_code', operator, name),
                      ('name', operator, name)]

            products = self.search(domain + args, limit=limit)
            if products:
                return products.name_get()

        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    def name_get(self):
        result = []
        for product in self:
            if product.buyer_style_no:
                name = f"[{product.buyer_style_no}] {product.name}"
            else:
                name = product.name
            result.append((product.id, name))
        return result
