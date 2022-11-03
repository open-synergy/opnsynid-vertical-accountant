# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantClientAdjustmentEntryDetail(models.Model):
    _name = "accountant.client_adjustment_entry_detail"
    _description = "Accountant Client Adjustment Entry Detail"

    name = fields.Char(
        string="Description",
        required=True,
    )
    entry_id = fields.Many2one(
        string="# Adjustment Entry",
        comodel_name="accountant.client_adjustment_entry",
        required=True,
        ondelete="cascade",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.client_account",
        required=True,
        ondelete="restrict",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="entry_id.currency_id",
        store=True,
    )
    debit = fields.Monetary(
        string="Debit",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    credit = fields.Monetary(
        string="Credit",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )

    @api.constrains(
        "credit",
    )
    def constrains_credit(self):
        for record in self:
            if record.credit:
                if record.credit < 0:
                    msg = _("Credit has to be greater or equal than 0")
                    raise UserError(msg)

    @api.constrains(
        "debit",
    )
    def constrains_debit(self):
        for record in self:
            if record.debit:
                if record.debit < 0:
                    msg = _("Debit has to be greater or equal than 0")
                    raise UserError(msg)
