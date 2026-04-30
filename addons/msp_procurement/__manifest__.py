{
    "name": "MSP Procurement",
    "version": "19.0.1.0.0",
    "summary": "Purchase-side linkage and controls for MSP workflow",
    "depends": ["purchase", "sale_management", "msp_quote"],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
