# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Employee Cash Advance",
    "version": "8.0.1.3.2",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_terminate_reason",
        "base_print_policy",
        "base_multiple_approval",
        "account_accountant",
        "hr",
        "web_readonly_bypass",
        "base_ir_filters_active",
        "base_action_rule",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "security/ir_rule_data.xml",
        "security/ir.model.access.csv",
        "data/ir_filter_data.xml",
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_terminate_reason_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "wizards/hr_approve_cash_advance.xml",
        "wizards/hr_approve_cash_advance_settlement.xml",
        "views/hr_employee_views.xml",
        "views/hr_cash_advance_type_views.xml",
        "views/hr_cash_advance_views.xml",
        "views/hr_cash_advance_settlement_views.xml",
    ],
    "demo": [
        "demo/account_journal_demo.xml",
        "demo/account_account_demo.xml",
        "demo/hr_advance_type_demo.xml",
    ],
    "installable": True,
    "application": True,
}
