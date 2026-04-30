from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_msp_source_sale_order_id = fields.Many2one("sale.order", string="Source Sale Order", tracking=True)
    x_msp_delivery_readiness = fields.Selection(
        [("blocked", "Blocked"), ("partial", "Partial"), ("ready", "Ready")],
        string="Delivery Readiness",
        default="blocked",
        tracking=True,
    )
