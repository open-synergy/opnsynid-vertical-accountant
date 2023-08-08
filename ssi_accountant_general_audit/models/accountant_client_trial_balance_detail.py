# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountantClientTrialBalanceDetail(models.Model):
    _name = "accountant.client_trial_balance_detail"
    _description = "Accountant Client Trial Balance Detail"
    _order = "sequence, trial_balance_id, id"

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.client_account",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="account_id.sequence",
        store=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="account_id.type_id",
        store=True,
        readonly=False,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="trial_balance_id.currency_id",
        store=True,
    )
    opening_balance = fields.Monetary(
        string="Opening Balance",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    opening_balance_debit = fields.Monetary(
        string="Debit Opening Balance",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    opening_balance_credit = fields.Monetary(
        string="Credit Opening Balance",
        required=True,
        default=0.0,
        currency_field="currency_id",
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

    @api.depends(
        "debit",
        "credit",
        "account_id",
        "opening_balance_debit",
        "opening_balance_credit",
    )
    def _compute_balance(self):
        for record in self:
            result = (
                opening_balance
            ) = ending_balance_debit = ending_balance_credit = 0.0
            if record.account_id:
                if record.account_id.normal_balance == "dr":
                    # TODO: Refactor
                    result = (
                        (record.opening_balance_debit - record.opening_balance_credit)
                        + record.debit
                        - record.credit
                    )
                    opening_balance = (
                        record.opening_balance_debit - record.opening_balance_credit
                    )
                else:
                    # TODO: Refactor
                    result = (
                        (record.opening_balance_credit - record.opening_balance_debit)
                        - record.debit
                        + record.credit
                    )
                    opening_balance = (
                        record.opening_balance_credit - record.opening_balance_debit
                    )
                balance = (record.opening_balance_debit + record.debit) - (
                    record.opening_balance_credit + record.credit
                )
                ending_balance_debit = balance > 0 and abs(balance) or 0.0
                ending_balance_credit = balance < 0 and abs(balance) or 0.0
            record.balance = result
            record.ending_balance_debit = ending_balance_debit
            record.ending_balance_credit = ending_balance_credit
            record.opening_balance = opening_balance

    ending_balance_debit = fields.Monetary(
        string="Debit Ending Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
    ending_balance_credit = fields.Monetary(
        string="Credit Ending Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
    opening_balance = fields.Monetary(
        string="Opening Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )

    @api.constrains(
        "debit",
        "credit",
        "opening_balance_debit",
        "opening_balance_credit",
    )
    def _constrains_no_negative(self):
        for record in self:
            record._check_debit()
            record._check_credit()
            record._check_opening_debit()
            record._check_opening_credit()

    def _check_debit(self):
        self.ensure_one()
        if self.debit < 0.0:
            error_message = _(
                """
            Context: Input/edit trial balance detail's debit amount
            Database ID: %s
            Problem: Debit amount less than 0.0
            Solution: Change debit amount
            """
                % (self.trial_balance_id.id)
            )
            raise ValidationError(error_message)

    def _check_credit(self):
        self.ensure_one()
        if self.credit < 0.0:
            error_message = _(
                """
            Context: Input/edit trial balance detail's credit amount
            Database ID: %s
            Problem: Credit amount less than 0.0
            Solution: Change credit amount
            """
                % (self.trial_balance_id.id)
            )
            raise ValidationError(error_message)

    def _check_opening_debit(self):
        self.ensure_one()
        if self.opening_balance_debit < 0.0:
            error_message = _(
                """
            Context: Input/edit trial balance detail's opening debit amount
            Database ID: %s
            Problem: Opening debit amount less than 0.0
            Solution: Change opening debit amount
            """
                % (self.trial_balance_id.id)
            )
            raise ValidationError(error_message)

    def _check_opening_credit(self):
        self.ensure_one()
        if self.opening_balance_credit < 0.0:
            error_message = _(
                """
            Context: Input/edit trial balance detail's opening credit amount
            Database ID: %s
            Problem: Opening credit amount less than 0.0
            Solution: Change opening credit amount
            """
                % (self.trial_balance_id.id)
            )
            raise ValidationError(error_message)
