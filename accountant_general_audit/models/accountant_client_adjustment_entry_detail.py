# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAdjustmentEntryDetail(models.Model):
    _name = "accountant.client_adjustment_entry_detail"
    _description = "Accountant Client Adjustment Entry Detail"

    entry_id = fields.Many2one(
        string="# Adjustment Entry",
        comodel_name="accountant.client_adjustment_entry",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.client_account",
        required=True,
        ondelete="restrict",
    )
    debit = fields.Float(
        string="Debit",
        required=True,
    )
    credit = fields.Float(
        string="Credit",
        required=True,
    )
