from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_msp_mpn = fields.Char(string="MPN", tracking=True)
    x_msp_brand = fields.Char(string="Brand", tracking=True)
    x_msp_supplier_sku = fields.Char(string="Supplier SKU", tracking=True)
    x_msp_is_serialized = fields.Boolean(string="Serialized", tracking=True)
    x_msp_is_recurring = fields.Boolean(string="Recurring", tracking=True)
    x_msp_is_recommended = fields.Boolean(string="Recommended", tracking=True)
    x_msp_margin_pct = fields.Float(string="Margin %", compute="_compute_msp_metrics", store=True)
    x_msp_profit = fields.Float(string="Profit", compute="_compute_msp_metrics", store=True)

    @api.depends("list_price", "standard_price")
    def _compute_msp_metrics(self):
        for template in self:
            profit = template.list_price - template.standard_price
            template.x_msp_profit = profit
            if template.list_price:
                template.x_msp_margin_pct = (profit / template.list_price) * 100
            else:
                template.x_msp_margin_pct = 0.0
