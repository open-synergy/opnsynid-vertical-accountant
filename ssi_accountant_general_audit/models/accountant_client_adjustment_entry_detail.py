# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantClientAdjustmentEntryDetail(models.Model):
    _name = "accountant.client_adjustment_entry_detail"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Adjustment Entry Detail"

    @api.depends(
        "entry_id",
        "entry_id.general_audit_id",
        "account_id",
    )
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

    name = fields.Char(
        string="Description",
    )
    code = fields.Char(
        required=False,
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
