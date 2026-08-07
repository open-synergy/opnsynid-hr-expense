/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_expense_account_reimbursement.hr_reimbursement_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/hr_reimbursement/01-create.md
    // (E1 delta -- Additional Fields). Navigation up to the New
    // form and the "Add a line" step are taken from the base IK
    // (ssi_hr_reimbursement/docs/hr_reimbursement/01-create.md,
    // Flow steps 1-2 and the "Add a line" step); the assertions
    // are the delta added by this module. The tour stops right
    // after the delta assertions -- it does not fill any field,
    // does not Save, and does not continue to confirm
    // (odoo-development-ui-test, scope-and-boundaries.md §3,
    // arketipe E1). There is no tour for
    // docs/hr_reimbursement/04-confirm.md: it only documents
    // additional confirm validation, which is unit test territory.
    tour.register(
        "ssi_hr_expense_account_reimbursement_hr_reimbursement_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Base Flow 1 -- Open the Human Resource > Expense >
            // Reimbursements menu. "Expense" is a section menuitem
            // with its own data-menu-xmlid (not a grouping
            // header), so it is its own step
            // (odoo-development-ui-test, patterns.md §A).
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
                content: "Open the Reimbursements menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_reimbursement.hr_reimbursement_menu"]',
            },
            {
                // Gate: wait for the Reimbursements action to
                // actually be mounted, not just any list view left
                // over from the landing action (patterns.md §A).
                content: "Reimbursements list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Reimbursements)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },

            // Base Flow 2 -- Click the New button. (14.0: "Create")
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },

            // Base Flow "Add a line" (base IK step 5) -- open the
            // Details tab that hosts the line_ids tree before
            // adding a line.
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },

            // Base Flow "Add a line" click -- opens the line as a
            // dialog form (the line_ids tree has no `editable`
            // attribute, so a new line is edited in a dialog).
            {
                content: "Click Add a line",
                trigger:
                    ".o_field_x2many[name='line_ids'] .o_field_x2many_list_row_add a",
            },
            {
                // Dialog form: do not prefix the trigger with
                // `.modal` -- 14.0 already searches inside the
                // modal (odoo-development-ui-test, patterns.md §H).
                content: "The line dialog is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },

            // Additional Fields (delta) -- the Expense Account
            // tab, inserted before the first base page of the
            // line dialog, is rendered as the first (and
            // therefore default active) tab and shows the
            // Required and # Expense Account fields. Both fields
            // are readonly and empty on a brand-new line, so the
            // assertion anchors on the field label text, not on
            // the (zero-width) many2one widget
            // (odoo-development-ui-test, patterns.md §O). The
            // values of both fields are not asserted: they are
            // computed and out of scope for this tour.
            {
                content: "Expense Account tab is displayed in the line dialog",
                trigger: ".o_notebook .nav-link:contains(Expense Account)",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },
            {
                content: "Required field label is displayed",
                trigger: ".o_form_label:contains(Required)",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },
            {
                content: "# Expense Account field label is displayed",
                trigger: ".o_form_label:contains(# Expense Account)",
                run: function () {
                    // Assertion only; do not trigger the default
                    // click.
                },
            },
        ]
    );
});
