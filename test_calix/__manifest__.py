{
    "name": "Test Calix",
    "author": "Franco",
    "website": "-",
    "support": "frankofe1997@gmail.com",
    "category": "Sales",
    "summary": "Manage sales channels",
    "license": "LGPL-3",
    "version": "15.0.0",
    "depends": ['account', 'sale_management', 'stock'],
    "data": [
        "security/ir.model.access.csv", 
        "views/sales_channels.xml",
        "views/sale_order.xml",
        "data/sales_channels_sequence.xml",
    ],
    "installable": True,
    "application": True,
}