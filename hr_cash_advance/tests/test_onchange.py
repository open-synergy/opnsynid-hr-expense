# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from .base import BaseCase


class TestOnchange(BaseCase):
    def test_hr_cash_advance_settlement_onchange_journal_id(self):
        self.advance_type.write(
            {
                "journal_id": self.advance_journal.id,
            }
        )
        values = {
            "type_id": self.advance_type.id,
        }
        ca_settlement = self.obj_ca_settlement.new(values)
        ca_settlement.onchange_journal_id()
        self.assertEqual(ca_settlement.journal_id, self.advance_journal)

    def test_hr_cash_advance_settlement_onchange_cash_advance_id(self):
        self.advance_type.write(
            {
                "cash_advance_id": False,
            }
        )
        values = {
            "type_id": self.advance_type.id,
        }
        ca_settlement = self.obj_ca_settlement.new(values)
        ca_settlement.onchange_cash_advance_id()
        self.assertEqual(ca_settlement.cash_advance_id, False)
