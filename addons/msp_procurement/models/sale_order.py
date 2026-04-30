from collections import defaultdict

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            order._msp_auto_create_purchase_orders()
        return result

    def _msp_auto_create_purchase_orders(self):
        self.ensure_one()
        vendor_lines = defaultdict(list)
        for line in self.order_line.filtered(
            lambda order_line: not order_line.display_type and order_line.product_id.type in ("product", "consu")
        ):
            seller = line.product_id._select_seller(
                quantity=line.product_uom_qty,
                uom_id=line.product_uom,
                date=self.date_order and fields.Date.to_date(self.date_order),
                partner_id=False,
            )
            if not seller:
                continue
            vendor_lines[seller.partner_id].append((line, seller))

        for vendor, lines in vendor_lines.items():
            po_vals = {
                "partner_id": vendor.id,
                "x_msp_source_sale_order_id": self.id,
                "x_msp_delivery_readiness": "ready",
            }
            po = self.env["purchase.order"].create(po_vals)
            for sale_line, seller in lines:
                self.env["purchase.order.line"].create({
                    "order_id": po.id,
                    "product_id": sale_line.product_id.id,
                    "name": sale_line.name or sale_line.product_id.display_name,
                    "product_qty": sale_line.product_uom_qty,
                    "product_uom": sale_line.product_uom.id,
                    "price_unit": seller.price,
                    "date_planned": fields.Datetime.now(),
                })
