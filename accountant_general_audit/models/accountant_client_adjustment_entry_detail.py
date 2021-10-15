# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantClientAdjustmentEntryDetail(models.Model):
    _name = "accountant.client_adjustment_entry_detail"
    _description = "Accountant Client Adjustment Entry Detail"

    @api.depends(
        "entry_id",
        "entry_id.general_audit_id",
        "account_id",
    )
    @api.multi
    def _compute_trial_balance_detail(self):
        obj_detail = self.env["accountant.client_trial_balance_detail"]
        for record in self:
            result = False
            if record.entry_id and record.account_id:
                entry = record.entry_id
                criteria = [
                    ("account_id", "=", record.account_id.id),
                    (
                        "trial_balance_id.general_audit_id.id",
                        "=",
                        entry.general_audit_id.id,
                    ),
                ]
                details = obj_detail.search(criteria)
                if len(details) > 0:
                    result = details[0]
            record.trial_balance_detail_id = result

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
    trial_balance_detail_id = fields.Many2one(
        string="TB Detail",
        comodel_name="accountant.client_trial_balance_detail",
        compute="_compute_trial_balance_detail",
        store=True,
    )
