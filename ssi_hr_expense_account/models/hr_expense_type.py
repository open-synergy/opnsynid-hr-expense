# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrExpenseType(models.Model):
    """
    Extends hr.expense_type with expense account filtering helpers.
    Provides a method to retrieve all products or categories that
    require an employee expense account for expense submission.
    """

    _inherit = "hr.expense_type"

    def _get_require_expense_products(self):
        """Return products requiring an employee expense account.

        Collects products belonging to a category flagged
        ``require_expense_account`` on this expense type, plus
        products directly flagged the same way.

        :return: ``product.product`` recordset
        """
        Product = self.env["product.product"]
        for record in self:
            categ_ids = (
                record.mapped("product_category_ids")
                .filtered(lambda x: x.require_expense_account)
                .mapped("categ_id")
            )
            all_products = Product.search([("categ_id", "in", categ_ids.ids)])
            all_products |= (
                record.mapped("product_ids")
                .filtered(lambda x: x.require_expense_account)
                .mapped("product_id")
            )
            return all_products
