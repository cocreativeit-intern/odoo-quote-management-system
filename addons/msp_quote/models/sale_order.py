from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection_add=[
            ("tech_review", "Tech Review"),
            ("finance_review", "Finance Review"),
        ],
    )
    x_msp_approved_by = fields.Many2one("res.users", string="Approved By", tracking=True)
    x_msp_approved_at = fields.Datetime(string="Approved At", tracking=True)
    x_msp_rejected_reason = fields.Text(string="Rejected Reason", tracking=True)
    x_msp_rejected_by = fields.Many2one("res.users", string="Rejected By", tracking=True)
    x_msp_rejected_at = fields.Datetime(string="Rejected At", tracking=True)
    x_msp_margin_pct = fields.Float(string="Margin %", compute="_compute_msp_margin", store=True)
    x_msp_task_count = fields.Integer(string="Delivery Tasks", compute="_compute_msp_task_count")

    @api.depends("amount_total", "amount_untaxed")
    def _compute_msp_margin(self):
        for order in self:
            if order.amount_total:
                order.x_msp_margin_pct = ((order.amount_total - order.amount_untaxed) / order.amount_total) * 100
            else:
                order.x_msp_margin_pct = 0.0

    def action_msp_submit_tech_review(self):
        if not self.env.user.has_group("msp_quote.group_msp_quote_tech_reviewer"):
            raise UserError(_("You do not have permission to submit quotes to tech review."))
        self.write({"state": "tech_review"})

    def action_msp_submit_finance_review(self):
        if not self.env.user.has_group("msp_quote.group_msp_quote_finance_reviewer"):
            raise UserError(_("You do not have permission to submit quotes to finance review."))
        self.write({"state": "finance_review"})

    def action_msp_approve_quote(self):
        if not self.env.user.has_group("msp_quote.group_msp_quote_finance_reviewer"):
            raise UserError(_("You do not have permission to approve quotes."))
        now = fields.Datetime.now()
        self.write({
            "x_msp_approved_by": self.env.user.id,
            "x_msp_approved_at": now,
            "x_msp_rejected_reason": False,
            "x_msp_rejected_by": False,
            "x_msp_rejected_at": False,
        })

    def action_msp_reject_quote(self):
        if not self.env.user.has_group("msp_quote.group_msp_quote_finance_reviewer"):
            raise UserError(_("You do not have permission to reject quotes."))
        now = fields.Datetime.now()
        self.write({
            "x_msp_rejected_by": self.env.user.id,
            "x_msp_rejected_at": now,
        })

    def action_confirm(self):
        result = super().action_confirm()
        project = self.env["project.project"].search([], limit=1)
        if not project:
            project = self.env["project.project"].create({"name": "MSP Delivery"})
        for order in self:
            self.env["project.task"].create({
                "name": f"Delivery - {order.name}",
                "project_id": project.id,
                "partner_id": order.partner_id.id,
                "description": f"Auto-generated from confirmed quote {order.name}.",
            })
        return result

    def action_msp_view_tasks(self):
        self.ensure_one()
        tasks = self.env["project.task"].search([("partner_id", "=", self.partner_id.id)])
        return {
            "name": "Delivery Tasks",
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [("id", "in", tasks.ids)],
        }

    @api.depends("partner_id")
    def _compute_msp_task_count(self):
        task_model = self.env["project.task"]
        for order in self:
            order.x_msp_task_count = task_model.search_count([("partner_id", "=", order.partner_id.id)])
