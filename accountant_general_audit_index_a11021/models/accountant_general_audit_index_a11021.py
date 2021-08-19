# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountantGeneralAuditIndexA11021(models.Model):
    _name = "accountant.general_audit_index_a11021"
    _description = "Accountant General Audit Index A.1102.1"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(AccountantGeneralAuditIndexA11021, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "general_audit_ids",
    )
    def _compute_general_audit_id(self):
        for document in self:
            document.general_audit_id = False
            if len(document.general_audit_ids) > 0:
                document.general_audit_id = document.general_audit_ids[0]

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _inverse_general_audit(self):
        for document in self:
            if not document.general_audit_id:
                continue
            document.general_audit_ids = [(6, 0, [document.general_audit_id.id])]

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
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        store=True,
        compute="_compute_general_audit_id",
        inverse="_inverse_general_audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    general_audit_ids = fields.Many2many(
        string="General Audits",
        comodel_name="accountant.general_audit",
        relation="rel_general_audit_2_index_a11021",
        column1="index_a11021_id",
        column2="general_audit_id",
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        readonly=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        store=True,
        related="general_audit_id.company_id",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        readonly=True,
        store=True,
    )
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_1 = fields.Selection(
        string="Question 1A1",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_2 = fields.Selection(
        string="Question 1A2",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_2 = fields.Selection(
        string="Question 1A2",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_3 = fields.Selection(
        string="Question 1A3",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_4 = fields.Selection(
        string="Question 1A4",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_a_5 = fields.Selection(
        string="Question 1A5",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_b_1 = fields.Selection(
        string="Question 1B1",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_b_2 = fields.Selection(
        string="Question 1B2",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_b_3 = fields.Selection(
        string="Question 1B3",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_c = fields.Selection(
        string="Question 1C",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_d = fields.Selection(
        string="Question 1D",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_e = fields.Selection(
        string="Question 1E",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_f = fields.Selection(
        string="Question 1F",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1_g = fields.Selection(
        string="Question 1G",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_1_a = fields.Selection(
        string="Question 21A",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_1_b = fields.Selection(
        string="Question 21B",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_1_c = fields.Selection(
        string="Question 21C",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_1_d = fields.Selection(
        string="Question 21D",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_1_e = fields.Selection(
        string="Question 21E",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2_2 = fields.Selection(
        string="Question 22",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_a = fields.Selection(
        string="Question 3a",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_b = fields.Selection(
        string="Question 3b",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_c = fields.Selection(
        string="Question 3c",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_d = fields.Selection(
        string="Question 3d",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_e = fields.Selection(
        string="Question 3e",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_f = fields.Selection(
        string="Question 3f",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_g = fields.Selection(
        string="Question 3g",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_h = fields.Selection(
        string="Question 3h",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_i = fields.Selection(
        string="Question 3i",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_j = fields.Selection(
        string="Question 3j",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_k = fields.Selection(
        string="Question 3k",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_l = fields.Selection(
        string="Question 3l",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3_m = fields.Selection(
        string="Question 3m",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_a = fields.Selection(
        string="Question 4a",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_b = fields.Selection(
        string="Question 4b",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_c = fields.Selection(
        string="Question 4c",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_d = fields.Selection(
        string="Question 4d",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_e = fields.Selection(
        string="Question 4e",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_f = fields.Selection(
        string="Question 4f",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_g = fields.Selection(
        string="Question 4g",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_h = fields.Selection(
        string="Question 4h",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_i = fields.Selection(
        string="Question 4i",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_j = fields.Selection(
        string="Question 4j",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_k = fields.Selection(
        string="Question 4k",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_l = fields.Selection(
        string="Question 4l",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4_m = fields.Selection(
        string="Question 4m",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    status_id = fields.Many2one(
        string="Status",
        comodel_name="accountant.general_audit_index_a11021_status",
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
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

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountantGeneralAuditIndexA11021, self)
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
        _super = super(AccountantGeneralAuditIndexA11021, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantGeneralAuditIndexA11021, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()
