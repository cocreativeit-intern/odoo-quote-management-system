{
    "name": "MSP Quotes",
    "version": "19.0.1.0.0",
    "summary": "Approval workflow and metrics for quote lifecycle",
    "depends": ["sale_management", "project", "msp_organization"],
    "data": [
        "security/msp_quote_groups.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
