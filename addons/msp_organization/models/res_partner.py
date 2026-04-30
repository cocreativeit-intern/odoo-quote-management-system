from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_msp_tenant_code = fields.Char(string="Tenant Code", tracking=True)
    x_msp_sla_tier = fields.Selection(
        [("gold", "Gold"), ("silver", "Silver"), ("bronze", "Bronze")],
        string="SLA Tier",
        tracking=True,
    )
    x_msp_contract_status = fields.Selection(
        [("active", "Active"), ("pending", "Pending"), ("expired", "Expired")],
        string="Contract Status",
        default="pending",
        tracking=True,
    )
    x_msp_quote_count = fields.Integer(string="Quote Count", compute="_compute_msp_related_counts")
    x_msp_task_count = fields.Integer(string="Task Count", compute="_compute_msp_related_counts")
    x_msp_open_task_count = fields.Integer(string="Open Tasks", compute="_compute_msp_related_counts")
    x_msp_quote_total = fields.Monetary(string="Quote Value", currency_field="currency_id", compute="_compute_msp_financials")
    x_msp_confirmed_total = fields.Monetary(
        string="Confirmed Sales",
        currency_field="currency_id",
        compute="_compute_msp_financials",
    )
    currency_id = fields.Many2one("res.currency", compute="_compute_currency_id")

    def _compute_msp_related_counts(self):
        quote_model = self.env["sale.order"]
        task_model = self.env["project.task"]
        for partner in self:
            root_partner = partner.commercial_partner_id
            partner_ids = root_partner.child_ids.ids + [root_partner.id]
            partner.x_msp_quote_count = quote_model.search_count([("partner_id", "in", partner_ids)])
            task_domain = [("partner_id", "child_of", root_partner.id)]
            partner.x_msp_task_count = task_model.search_count(task_domain)
            partner.x_msp_open_task_count = task_model.search_count(task_domain + [("stage_id.fold", "=", False)])

    def _compute_msp_financials(self):
        quote_model = self.env["sale.order"]
        for partner in self:
            root_partner = partner.commercial_partner_id
            partner_ids = root_partner.child_ids.ids + [root_partner.id]
            quote_domain = [("partner_id", "in", partner_ids)]
            confirmed_domain = quote_domain + [("state", "in", ["sale", "done"])]
            partner.x_msp_quote_total = sum(quote_model.search(quote_domain).mapped("amount_total"))
            partner.x_msp_confirmed_total = sum(quote_model.search(confirmed_domain).mapped("amount_total"))

    def _compute_currency_id(self):
        company_currency = self.env.company.currency_id
        for partner in self:
            partner.currency_id = partner.property_product_pricelist.currency_id or company_currency

    def action_msp_view_quotes(self):
        self.ensure_one()
        root_partner = self.commercial_partner_id
        return {
            "name": "Quotes",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("partner_id", "in", root_partner.child_ids.ids + [root_partner.id])],
        }

    def action_msp_view_tasks(self):
        self.ensure_one()
        root_partner = self.commercial_partner_id
        return {
            "name": "Tasks",
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [("partner_id", "child_of", root_partner.id)],
        }
