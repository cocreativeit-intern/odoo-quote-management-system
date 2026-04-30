{
    "name": "MSP Product",
    "version": "19.0.1.0.0",
    "summary": "Product detail extensions for quote-first MSP workflows",
    "depends": ["product", "stock", "purchase", "sale_management", "msp_base"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
