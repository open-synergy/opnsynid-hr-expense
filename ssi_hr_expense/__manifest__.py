# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Employee Expense",
    "version": "14.0.1.2.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "product",
        "ssi_hr",
        "ssi_master_data_mixin",
        "ssi_product_usage_account_type",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "views/hr_expense_type_views.xml",
        "views/hr_expense_type_product_views.xml",
        "views/hr_expense_type_product_category_views.xml",
    ],
    "demo": [
        "demo/product_category_demo.xml",
        "demo/product_product_demo.xml",
        "demo/hr_expense_type_demo.xml",
    ],
}
