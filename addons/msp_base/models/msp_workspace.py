from odoo import fields, models


class MspWorkspace(models.Model):
    _name = "msp.workspace"
    _description = "MSP Workspace"
    _inherit = ["mail.thread"]

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
