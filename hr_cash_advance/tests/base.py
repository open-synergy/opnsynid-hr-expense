# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseCase(TransactionCase):
    def setUp(self, args, *kwargs):
        result = super(BaseCase, self).setUp(*args, **kwargs)
        self.obj_ca_settlement = self.env["hr.cash_advance_settlement"]
        self.advance_journal = self.env.ref(
            "hr_cash_advance.employe_advance_settlement_journal"
        )
        self.advance_type = self.env.ref("hr_cash_advance.example_advance_type")

        self.obj_ca_settlement_line = self.env["hr.cash_advance_settlement_line"]

        return result
