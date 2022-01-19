# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountantReportStakeholderReport(models.Model):
    _name = "accountant.report_stakeholder_report"
    _description = "Accounting Report Stakeholder Report"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]

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

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
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

    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.report_stakeholder_report_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    accountant_report_ids = fields.Many2many(
        string="Accountant Reports",
        comodel_name="accountant.report",
        relation="rel_stakeholder_report_2_accountant_report",
        column1="stakeholder_report_id",
        column2="accountant_report_id",
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
    )

    confirm_ok = fields.Boolean(
        string="Can Confirmed",
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

    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )

    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
    )

    valid_date = fields.Datetime(
        string="Validation Date",
        readonly=True,
    )
    valid_user_id = fields.Many2one(
        string="Valid By",
        comodel_name="res.users",
    )

    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
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

    @api.depends(
        "type_id",
    )
    @api.multi
    def _compute_policy(self):
        _super = super(AccountantReportStakeholderReport, self)
        _super._compute_policy()

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

    @api.multi
    def unlink(self):
        strWarning1 = _("You can only delete data on draft state")
        strWarning2 = _("You can not delete data with document number")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning1)
            if document.name != "/":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning2)
        _super = super(AccountantReportStakeholderReport, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(AccountantReportStakeholderReport, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantReportStakeholderReport, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

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

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Start Date cannot be greater than End Date")
                if record.date_start < record.date_end:
                    raise UserError(strWarning)
