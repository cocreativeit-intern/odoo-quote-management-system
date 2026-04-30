from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    x_msp_response_deadline = fields.Datetime(string="Response Deadline", tracking=True)
    x_msp_resolution_deadline = fields.Datetime(string="Resolution Deadline", tracking=True)
    x_msp_billing_state = fields.Selection(
        [("pending", "Pending"), ("ready", "Ready"), ("invoiced", "Invoiced")],
        string="Billing State",
        default="pending",
        tracking=True,
    )
