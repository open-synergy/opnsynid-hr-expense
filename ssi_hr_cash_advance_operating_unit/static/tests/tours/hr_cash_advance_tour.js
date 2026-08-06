/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_cash_advance_operating_unit.hr_cash_advance_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_cash_advance/01-create.md (E1 delta — Additional Fields)
    tour.register(
        "ssi_hr_cash_advance_operating_unit_hr_cash_advance_field_ou",
        {
            test: true,
            url: "/web",
        },
        [
            // Base Flow 1 — Open the Human Resource > Expense > Cash
            // Advances menu. "Expense" is a grouping header (menuitem
            // without an action) that nests "Cash Advances", so it has
            // no step of its own (odoo-development-ui-test,
            // patterns.md §A).
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Expense menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_expense.expense_menu"]',
            },
            {
                content: "Open the Cash Advances menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_cash_advance.hr_cash_advance_menu"]',
            },
            {
                // Gate: wait for the Cash Advances action to actually
                // be mounted, not just any list view left over from
                // the landing action (patterns.md §A).
                content: "Cash Advances list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Cash Advances)",
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

            // Additional Fields (docs/hr_cash_advance/01-create.md, delta
            // of ssi_hr_cash_advance_operating_unit) — the Operating Unit
            // field added by mixin.single_operating_unit is rendered on
            // the create form for a user in the multi operating unit
            // group. Delta-only tour: it stops here, it does not fill
            // any field and does not continue to Save (E1 delta-only;
            // the Modified — Record Visibility part of the IK is not
            // covered by a tour, see odoo-development-ui-test
            // scope-and-boundaries.md).
            {
                content: "Operating Unit field is displayed",
                trigger: ".o_field_widget[name='operating_unit_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
