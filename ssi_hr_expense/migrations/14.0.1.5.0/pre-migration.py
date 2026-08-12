# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.4.2 -> 14.0.1.5.0
#
# Changes: hr.expense_type replaced its hand-rolled analytic account
#          selection fields with the standard SSI m2o configurator
#          pattern (manual/domain/code):
#
#            analytic_account_method (fixed/python) is renamed to
#            analytic_account_selection_method (manual/domain/code),
#            and its stored values are remapped: "fixed" -> "manual"
#            (the manual m2m analytic_account_ids column and its
#            junction table rel_expense_type_2_analytic_account are
#            untouched, so a "fixed" row keeps selecting exactly the
#            same analytic accounts it did before), "python" ->
#            "code" (same Python snippet, same semantics, only the
#            selection value changes), and NULL -> "manual" (a row
#            that predates analytic_account_method entirely had no
#            selection method and, per the old compute, resolved to
#            "no analytic account is selectable"; "manual" combined
#            with an empty analytic_account_ids m2m preserves that
#            outcome).
#
#            python_code is renamed to analytic_account_python_code
#            (same column content, only the name changes to match
#            the new field name introduced alongside the new
#            analytic_account_domain column).
#
#            analytic_account_domain is a brand new column and is
#            NOT backfilled here: it is left at its Odoo column
#            default ("[]") applied by _init_column when the ORM
#            creates the field, which is the correct value for every
#            pre-existing row (none of them used to have a domain).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_TABLE = "hr_expense_type"


def _rename_columns(cr):
    """Rename the two analytic account configurator columns.

    Renames ``analytic_account_method`` to
    ``analytic_account_selection_method`` and ``python_code`` to
    ``analytic_account_python_code`` on ``hr_expense_type``, guarded
    so re-running the script (or running it after the ORM already
    created the new columns) is a no-op.

    :param cr: database cursor
    :return: nothing; renames columns on ``hr_expense_type``
    """
    renames = []
    if openupgrade.column_exists(
        cr, _TABLE, "analytic_account_method"
    ) and not openupgrade.column_exists(
        cr, _TABLE, "analytic_account_selection_method"
    ):
        renames.append(("analytic_account_method", "analytic_account_selection_method"))
    if openupgrade.column_exists(
        cr, _TABLE, "python_code"
    ) and not openupgrade.column_exists(cr, _TABLE, "analytic_account_python_code"):
        renames.append(("python_code", "analytic_account_python_code"))
    if renames:
        openupgrade.rename_columns(cr, {_TABLE: renames})
        _logger.info(
            "Renamed column(s) %s on %s.",
            ", ".join("%s -> %s" % pair for pair in renames),
            _TABLE,
        )


def _remap_selection_values(cr):
    """Remap the old selection values to their new equivalents.

    Runs after :func:`_rename_columns`, so the column already carries
    its new name (``analytic_account_selection_method``) but still
    holds the old values (``fixed``/``python``/``NULL``). Maps
    ``fixed`` -> ``manual``, ``python`` -> ``code``, and any other
    value (including ``NULL``, the pre-configurator default) ->
    ``manual``, which combined with an untouched (and, for NULL rows,
    typically empty) ``analytic_account_ids`` m2m preserves the
    "no analytic account selectable" outcome those rows had before.

    :param cr: database cursor
    :return: nothing; updates rows of ``hr_expense_type``
    """
    openupgrade.logged_query(
        cr,
        """
        UPDATE hr_expense_type
        SET analytic_account_selection_method = 'manual'
        WHERE analytic_account_selection_method = 'fixed'
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE hr_expense_type
        SET analytic_account_selection_method = 'code'
        WHERE analytic_account_selection_method = 'python'
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE hr_expense_type
        SET analytic_account_selection_method = 'manual'
        WHERE analytic_account_selection_method IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    """Rename and remap the analytic account configurator columns.

    Post-migration verification (run against the live DB after
    updating the module): every row of ``hr_expense_type`` must have
    ``analytic_account_selection_method IN ('manual', 'domain',
    'code')`` (no ``NULL``, no leftover ``fixed``/``python``)::

        SELECT id, analytic_account_selection_method,
               analytic_account_domain, analytic_account_python_code
        FROM hr_expense_type
        WHERE analytic_account_selection_method NOT IN
              ('manual', 'domain', 'code')
           OR analytic_account_selection_method IS NULL;
        -- expected: 0 rows

    ``analytic_account_domain`` must read ``[]`` on every row (the
    new column's default, never backfilled by this script)::

        SELECT id FROM hr_expense_type
        WHERE analytic_account_domain IS DISTINCT FROM '[]';
        -- expected: 0 rows

    The junction table row count must be unchanged by this migration
    (it is never touched)::

        SELECT count(*) FROM rel_expense_type_2_analytic_account;
        -- expected: same count as before the update

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; renames and remaps ``hr_expense_type`` columns
    """
    _rename_columns(env.cr)
    _remap_selection_values(env.cr)
    _logger.info(
        "Remapped analytic_account_selection_method values on %s "
        "row(s) of %s (fixed->manual, python->code, NULL->manual).",
        env.cr.rowcount,
        _TABLE,
    )
