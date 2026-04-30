{
    "name": "MSP Base",
    "version": "19.0.1.0.0",
    "summary": "Shared foundation for MSP modules",
    "depends": ["base", "mail", "product", "sale_management", "purchase", "project", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/msp_dashboard_data.xml",
        "views/msp_dashboard_views.xml",
        "views/msp_navigation_views.xml",
        "views/msp_workspace_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
