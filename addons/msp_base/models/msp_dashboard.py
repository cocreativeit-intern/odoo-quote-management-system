from odoo import api, fields, models


class MspDashboard(models.Model):
    _name = "msp.dashboard"
    _description = "MSP Dashboard"

    name = fields.Char(default="MSP Overview", required=True)
    currency_id = fields.Many2one("res.currency", compute="_compute_currency")
    quote_count = fields.Integer(compute="_compute_metrics")
    sales_count = fields.Integer(compute="_compute_metrics")
    purchase_count = fields.Integer(compute="_compute_metrics")
    customer_count = fields.Integer(compute="_compute_metrics")
    task_open_count = fields.Integer(compute="_compute_metrics")
    quote_total = fields.Monetary(currency_field="currency_id", compute="_compute_metrics")
    sales_total = fields.Monetary(currency_field="currency_id", compute="_compute_metrics")

    @api.depends_context("uid")
    def _compute_currency(self):
        for record in self:
            record.currency_id = self.env.company.currency_id

    @api.depends_context("uid")
    def _compute_metrics(self):
        sale_order = self.env["sale.order"]
        purchase_order = self.env["purchase.order"]
        partner = self.env["res.partner"]
        task = self.env["project.task"]
        quote_domain = [("state", "in", ["draft", "sent", "tech_review", "finance_review"])]
        sales_domain = [("state", "in", ["sale", "done"])]
        for record in self:
            quote_records = sale_order.search(quote_domain)
            sales_records = sale_order.search(sales_domain)
            record.quote_count = len(quote_records)
            record.sales_count = len(sales_records)
            record.purchase_count = purchase_order.search_count([])
            record.customer_count = partner.search_count([("customer_rank", ">", 0), ("is_company", "=", True)])
            record.task_open_count = task.search_count([("stage_id.fold", "=", False)])
            record.quote_total = sum(quote_records.mapped("amount_total"))
            record.sales_total = sum(sales_records.mapped("amount_total"))
