# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountantClientTrialBalance(models.Model):
    _name = "accountant.client_trial_balance"
    _description = "Accountant Client Trial Balance"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "ir.needaction_mixin",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.multi
    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(AccountantClientTrialBalance, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    balance_date_start = fields.Date(
        string="Balance Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    balance_date_end = fields.Date(
        string="Balance End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "account_type_set_id",
    )
    def _compute_account_type_ids(self):
        obj_type_set = self.env["accountant.client_account_type_set"]
        for document in self:
            result = []
            criteria = []
            if document.account_type_set_id:
                criteria.append(
                    ("detail_ids", "in", document.account_type_set_id.id),
                )
                result = obj_type_set.search(criteria).detail_ids
        document.allowed_type_ids = result

    allowed_type_ids = fields.Many2many(
        string="Allowed Account Type",
        comodel_name="accountant.client_account_type",
        compute="_compute_account_type_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="accountant.client_trial_balance_detail",
        inverse_name="trial_balance_id",
        copy=True,
    )
    standard_detail_ids = fields.One2many(
        string="Standard Detail",
        comodel_name="accountant.client_trial_balance_standard_detail",
        inverse_name="trial_balance_id",
        readonly=True,
        copy=True,
    )
    computation_ids = fields.One2many(
        string="Computation",
        comodel_name="accountant.client_trial_balance_computation",
        inverse_name="trial_balance_id",
        readonly=True,
        copy=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("valid", "Valid"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    valid_ok = fields.Boolean(
        string="Can Valid",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    valid_date = fields.Datetime(
        string="Validation Date",
        readonly=True,
        copy=False,
    )
    valid_user_id = fields.Many2one(
        string="Valid By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_valid(self):
        for record in self:
            record.write(record._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "valid",
            "name": sequence,
            "valid_date": fields.Datetime.now(),
            "valid_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "valid_date": False,
            "valid_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.onchange("account_type_set_id")
    def onchange_standard_detail_ids(self):
        self.update({"standard_detail_ids": [(5, 0, 0)]})
        if self.account_type_set_id:
            result = []
            for detail in self.account_type_set_id.detail_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "sequence": detail.sequence,
                            "type_id": detail.id,
                        },
                    )
                )
            self.update({"standard_detail_ids": result})

    @api.onchange("account_type_set_id")
    def onchange_computation_ids(self):
        self.update({"computation_ids": [(5, 0, 0)]})
        if self.account_type_set_id:
            result = []
            for detail in self.account_type_set_id.computation_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "computation_item_id": detail.computation_id.id,
                        },
                    )
                )
            self.update({"computation_ids": result})

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountantClientTrialBalance, self)
        _super.unlink()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.multi
    def validate_tier(self):
        _super = super(AccountantClientTrialBalance, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantClientTrialBalance, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    @api.constrains("balance_date_start", "balance_date_end")
    def _check_balance_date_start_end(self):
        for record in self:
            if record.balance_date_start and record.balance_date_end:
                strWarning = _(
                    "Balance Date end must be greater than Balance date start"
                )
                if record.balance_date_end < record.balance_date_start:
                    raise UserError(strWarning)

    @api.constrains("previous_date_start", "previous_date_end")
    def _check_previous_date_start_end(self):
        for record in self:
            if record.previous_date_start and record.previous_date_end:
                strWarning = _(
                    "Previous Date end must be greater than Previous date start"
                )
                if record.previous_date_end < record.previous_date_start:
                    raise UserError(strWarning)

    @api.constrains("balance_date_start", "previous_date_end")
    def _check_previous_balance_date(self):
        for record in self:
            if record.balance_date_start and record.previous_date_end:
                strWarning = _(
                    "Balance date start must be greater than previous balance date end"
                )
                if record.previous_date_end >= record.balance_date_start:
                    raise UserError(strWarning)
