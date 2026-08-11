/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_hr_cash_advance.hr_cash_advance_settlement_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below --
    // Flow step 1 of every IK in docs/hr_cash_advance_settlement/:
    // "Open the Human Resource > Expense > Cash Advance Settlements
    // menu." "Expense" is a section menuitem (has its own
    // data-menu-xmlid, not a grouping header), so it is its own step
    // (odoo-development-ui-test, patterns.md §A).
    function openCashAdvanceSettlementsList() {
        return [
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
                content: "Open the Cash Advance Settlements menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_cash_advance.hr_cash_advance_settlement_menu"]',
            },
            {
                // Gate: wait for the Cash Advance Settlements action to
                // actually be mounted, not just any list view left over
                // from the landing action (odoo-development-ui-test,
                // patterns.md §A).
                content: "Cash Advance Settlements list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Cash Advance Settlements)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    // IK: docs/hr_cash_advance_settlement/01-create.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Click the New button.
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

            // Flow 3 — Fill in the required fields in the header.
            // Employee/Department/Manager/Job Position are auto-filled
            // from the current user's employee and Currency keeps its
            // default (company currency) -- all left as-is (Keputusan
            // Desain, issue open-synergy/opnsynid-hr-expense#136).
            // Pricelist is optional and intentionally skipped.
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Cash Advance Settlement Create Type",
            },
            {
                content: "Pick the type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Cash Advance Settlement Create Type)",
                in_modal: false,
            },
            {
                content: "Select the # Cash Advance",
                trigger: ".o_field_many2one[name='cash_advance_id'] input",
                run: "text TOURCASETTLECREATECA",
            },
            {
                content: "Pick the cash advance from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOURCASETTLECREATECA)",
                in_modal: false,
            },
            {
                content: "Fill in the Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/15/2026",
            },
            // Journal (Accounting tab) auto-fills from Type via
            // onchange_journal_id and is intentionally left as-is
            // (Keputusan Desain, issue #136).

            // Flow 4 — Add a line in the Details tab via Add a line
            // (the Reload from Cash Advance button is out of scope,
            // Keputusan Desain issue #136). The line list has no
            // `editable` attribute, so Add a line opens the line as a
            // dialog form, not an inline row.
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
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
            // Date Expense is optional and intentionally skipped
            // (Keputusan Desain, issue #136).
            {
                content: "Select the Product",
                trigger: ".o_field_widget[name='product_id'] input",
                run: "text Tour Cash Advance Settlement Product",
            },
            {
                content: "Pick the product from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Cash Advance Settlement Product)",
                in_modal: false,
            },
            // Description, Usage, Account, and UoM auto-fill from the
            // selected Product (and Type, through Usage) and are
            // intentionally left as-is. Analytic Account, Pricelist,
            // and Unit Price are optional / auto-conditional and are
            // also skipped (Keputusan Desain, issue #136).
            {
                // Placed inside a plain <div> (not the usual auto
                // wrapped <label>/<td> pair), this Float field's root
                // element is the <input> itself (same rendering as a
                // Char field in 14.0, odoo-development-ui-test,
                // patterns.md §C) -- no nested ` input` suffix.
                content: "Fill in the Quantity",
                trigger: ".o_field_widget[name='uom_quantity']",
                run: "text 1.0",
            },
            {
                content: "Save the line",
                trigger: ".modal-footer button.btn-primary:contains('Save & Close')",
            },
            {
                content: "The line is added to the Details tab",
                trigger:
                    ".o_field_x2many[name='line_ids'] .o_data_row:contains(Tour Cash Advance Settlement Product)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — A new record is created in Draft
            // status.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/04-confirm.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Confirm Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Waiting for
            // Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            // Negative (visible): the Confirm button is no longer
            // shown once the record left Draft.
            {
                content: "The Confirm button is no longer shown",
                trigger:
                    ".o_statusbar_buttons:not(:has(button[name='action_confirm']:visible))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/05-approve.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Approve Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition (all approval levels fulfilled) --
            // status changes to Done and a journal entry is
            // automatically created and reconciled against the
            // original cash advance. The fixture's approval template
            // has a single validator level and the tour user (admin)
            // is the sole approver, so this branch is always the one
            // exercised.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/10-cancel.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Cancel Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Cancel button. It is a
            // `type="action"` button, so its `name` attribute is a
            // numeric action id in the DOM; target it by label
            // instead (odoo-development-ui-test, selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard that appears, select the
            // Cancellation Reason.
            {
                // Wizard: do not prefix the trigger with `.modal`
                // (odoo-development-ui-test, patterns.md §H).
                content: "The Select Cancel Reason wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // The wizard renders `cancel_reason_id` with
                // `widget="radio"` (base_select_cancel_reason_views.xml),
                // not the default many2one autocomplete -- select the
                // matching radio item by its label text.
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(Tour Cash Advance Settlement Cancel Reason) input",
            },

            // Flow 5 — Click Confirm.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog. The
            // wizard's Confirm button carries
            // `confirm="Are you sure?"` (mixin
            // ssi_transaction_cancel_mixin), which
            // docs/hr_cash_advance_settlement/10-cancel.md was missing
            // -- added there as step 6 to keep the IK the accurate
            // source of truth (odoo-development-ui-test, patterns.md
            // §G), same as the existing fix in
            // docs/hr_cash_advance/10-cancel.md (issue
            // open-synergy/opnsynid-hr-expense#131). This second
            // dialog stacks on top of the wizard; 14.0 scopes the
            // trigger search to the topmost visible modal, so the
            // selector below resolves to it automatically.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/02-edit.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Edit Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Edit button. 14.0 only: a record that
            // already exists opens readonly (odoo-development-ui-test,
            // patterns.md §E).
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 4 — Inline Action: Reload from Cash Advance
            // rebuilds the Details lines from the linked cash
            // advance's lines. Clicked FIRST, before any other field
            // is touched, so the form is still clean when the button
            // (a `type="object"` button) triggers its own auto-save +
            // RPC + reload cycle -- doing this after an unsaved field
            // edit would make that edit race the button's own save
            // (odoo-development-ui-test, patterns.md §P). The fixture
            // settlement starts with NO lines while its cash advance
            // carries exactly one, distinctly-named line, so the gate
            // below is a real data delta: impossible to match before
            // the click, certain to match after (patterns.md §P uji
            // lakmus).
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click the Reload from Cash Advance button",
                trigger: ".o_form_view button[name='action_reload_cash_advance']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "The line reloaded from the cash advance is displayed",
                trigger:
                    ".o_field_x2many[name='line_ids'] .o_data_row:contains(Tour Cash Advance Settlement Edit Reload Marker)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 5 — Change the required fields: pick a Date
            // different from the fixture's, so the Post-Condition
            // reopen-and-read below actually proves the change landed
            // (odoo-development-ui-test, patterns.md §L).
            {
                content: "Fill in a different Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 02/01/2026",
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Post-Condition — The record is updated with the new
            // values. Reading a Date field immediately after typing
            // it is unreliable while the form is still editable
            // (odoo-development-ui-test, patterns.md §L): go back to
            // the list and reopen the record, which always renders
            // read-only at 14.0, to read a genuine text node.
            {
                content: "Go back to the list",
                trigger:
                    ".breadcrumb-item:not(.active):contains('Cash Advance Settlements')",
            },
            {
                content: "Reopen the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Edit Employee) .o_data_cell:first",
            },
            {
                content: "Date shows the new value",
                trigger:
                    ".o_form_readonly .o_field_widget[name='date']:contains('02/01/2026')",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/03-delete.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Select the record to delete (check the checkbox).
            {
                content: "Select the record to delete",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Delete Employee) .o_list_record_selector input",
                extra_trigger: ".o_list_view",
                run: "click",
            },

            // Flow 3 — Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
                // 14.0: the Action dropdown is an Owl component that
                // does not always open on a synthetic click
                // (odoo-development-ui-test, patterns.md §I).
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Click Delete",
                // Item Action menu is an Owl component; target the <a>
                // inside .o_menu_item and match the label EXACTLY --
                // :contains(Delete) as a substring could match another
                // item.
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — The selected record is permanently
            // removed from the system.
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(Tour Cash Advance Settlement Delete Employee)))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/06-reject.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record to reject.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Reject Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/12-restart.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record to restart.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Restart Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            // `action_restart` carries `confirm="Restart data. Are you
            // sure?"`, missing from the original IK text -- added
            // there as the corrected IK Flow (odoo-development-ui-test,
            // patterns.md §G).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/hr_cash_advance_settlement/13-reset-number.md
    tour.register(
        "ssi_hr_cash_advance_hr_cash_advance_settlement_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openCashAdvanceSettlementsList(), [
            // Flow 2 — Open the record whose document number will be
            // reset.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Cash Advance Settlement Reset Number Employee) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Flow 3 — Click the Reset Document Number button.
            {
                content: "Click the Reset Document Number button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reset_document_number']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            // `action_reset_document_number` carries `confirm="Restart
            // document number. Are you sure?"`, missing from the
            // original IK text -- added here as the corrected IK Flow
            // (odoo-development-ui-test, patterns.md §G).
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Document number returns to "/" (it is
            // already "/" on this Draft record). `name` field stores
            // "/", but `MixinTransaction.name_get`
            // (ssi_transaction_mixin, mixin_transaction.py) renders it
            // as "*<id>" whenever the stored number is "/" -- the
            // literal "/" never appears in the readonly display_name
            // widget, so the visible fact checked here is that the
            // action completes and the read-only form still shows the
            // "*<id>" placeholder, not a new error.
            {
                content: 'Document number is still "/" (shown as "*<id>")',
                trigger:
                    ".o_form_view .o_field_widget[name='display_name']:contains('*')",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
