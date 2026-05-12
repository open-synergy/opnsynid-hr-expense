# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EmployeeBusinessTrip(models.Model):
    _name = "employee_business_trip"
    _inherit = [
        "employee_business_trip",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
