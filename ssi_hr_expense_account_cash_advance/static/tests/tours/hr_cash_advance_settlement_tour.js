/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_hr_expense_account_cash_advance.hr_cash_advance_settlement_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_cash_advance_settlement/01-create.md
        // (E1 delta — Additional Fields). Navigation up to the New form is
        // taken from the base IK
        // (ssi_hr_cash_advance/docs/hr_cash_advance_settlement/01-
        // create.md, Flow steps 1-2 and the "Add a line" step); the
        // assertions are the delta added by this module. The tour stops
        // right after the delta assertions -- it does not fill any field,
        // does not Save, and does not continue to confirm
        // (odoo-development-ui-test, scope-and-boundaries.md §3, arketipe
        // E1).
        tour.register(
            "ssi_hr_expense_account_cash_advance_hr_cash_advance_settlement_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 — Open the Human Resource > Expense > Cash
                // Advance Settlements menu. "Expense" is a section
                // menuitem with its own data-menu-xmlid (not a grouping
                // header), so it is its own step
                // (odoo-development-ui-test, patterns.md §A).
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Expense menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_expense.expense_menu"]',
                },
                {
                    content: "Open the Cash Advance Settlements menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_cash_advance.hr_cash_advance_settlement_menu"]',
                },
                {
                    // Gate: wait for the Cash Advance Settlements action
                    // to actually be mounted, not just any list view left
                    // over from the landing action (patterns.md §A).
                    content: "Cash Advance Settlements list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Cash Advance Settlements)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Base Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Base Flow "Add a line" (base IK step 4) — open the
                // Details tab that hosts the line_ids tree before
                // inspecting its columns.
                {
                    content: "Open the Details tab",
                    trigger: ".o_notebook .nav-link:contains(Details)",
                },

                // Additional Fields (delta) — the Require Expense Account
                // and Expense Account columns are inserted after Account
                // without an `optional` column attribute, so they are
                // visible inline without opening the column picker
                // (Keputusan Desain, issue #134).
                {
                    content:
                        "Require Expense Account column is displayed in the line tree",
                    trigger:
                        ".o_field_x2many[name='line_ids'] th[data-name='require_expense_account']:contains(Require Expense Account)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Expense Account column is displayed in the line tree",
                    trigger:
                        ".o_field_x2many[name='line_ids'] th[data-name='expense_account_id']:contains(Expense Account)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Base Flow "Add a line" click — opens the line as a
                // dialog form (the line_ids tree has no `editable`
                // attribute).
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // Dialog form: do not prefix the trigger with `.modal`
                    // -- 14.0 already searches inside the modal
                    // (odoo-development-ui-test, patterns.md §H).
                    content: "The line dialog is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Additional Fields (delta) — the Expense Account tab,
                // inserted before the first base page of the line dialog,
                // is rendered as the first (and therefore default active)
                // tab and shows the Required and Expense Account fields.
                // Both fields are readonly and empty on a brand-new line,
                // so the assertion anchors on the field label text, not
                // on the (zero-width) many2one widget
                // (odoo-development-ui-test, patterns.md §O).
                {
                    content: "Expense Account tab is displayed in the line dialog",
                    trigger: ".o_notebook .nav-link:contains(Expense Account)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Required field label is displayed",
                    trigger: ".o_form_label:contains(Required)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Expense Account field label is displayed",
                    trigger: ".o_form_label:contains(Expense Account)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
