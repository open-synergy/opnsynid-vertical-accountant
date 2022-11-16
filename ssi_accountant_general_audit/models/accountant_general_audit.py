# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountantGeneralAudit(models.Model):
    _name = "accountant.general_audit"
    _description = "Accountant General Audit"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
        "mixin.transaction_done",
    ]

    # Attributes related to multiple approval
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(AccountantGeneralAudit, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(AccountantGeneralAudit, self)
        _super._compute_policy()

    @api.depends(
        "trial_balance_ids",
        "trial_balance_ids.trial_balance_type",
    )
    def _compute_trial_balance_id(self):
        for document in self:
            home = interim = previous = extrapolation = False
            homes = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "home"
            )
            if len(homes) > 0:
                home = homes[0]
            interims = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "interim"
            )
            if len(interims) > 0:
                interim = interims[0]
            extrapolations = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "extrapolation"
            )
            if len(extrapolations) > 0:
                extrapolation = extrapolations[0]
            previouses = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "previous"
            )
            if len(previouses) > 0:
                previous = previouses[0]

            document.home_trial_balance_id = home
            document.interim_trial_balance_id = interim
            document.extrapolation_trial_balance_id = extrapolation
            document.previous_trial_balance_id = previous

    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
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
    interim_date_start = fields.Date(
        string="Interim Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
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
        string="Account Type Set",
        comodel_name="accountant.client_account_type_set",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    financial_accounting_standard_id = fields.Many2one(
        string="Financial Accounting Standard",
        comodel_name="accountant.financial_accounting_standard",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    opinion_id = fields.Many2one(
        string="Opinion",
        comodel_name="accountant.opinion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_firm = fields.Integer(
        string="Num. of Consecutive Audit (Firm)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_accountant = fields.Integer(
        string="Num. of Consecutive Audit (Accountant)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_option = fields.Selection(
        string="Restatement Option",
        selection=[
            ("no", "Not a restatement"),
            ("internal", "Restated audit exist in Odoo"),
            ("external", "Restated audit does not exist in Odoo"),
        ],
        required=True,
        default="no",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit_id = fields.Many2one(
        string="Previous # Audit",
        comodel_name="accountant.general_audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit = fields.Char(
        string="Previous Audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    required_worksheet_type_ids = fields.Many2many(
        string="Required Worksheet Type(s)",
        comodel_name="accountant.general_audit_worksheet_type",
        relation="rel_general_audit_2_required_worksheet_type",
        column1="general_audit_id",
        column2="worksheet_type_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    additional_worksheet_type_ids = fields.Many2many(
        string="Additional Worksheet Type(s)",
        comodel_name="accountant.general_audit_worksheet_type",
        relation="rel_general_audit_2_additional_worksheet_type",
        column1="general_audit_id",
        column2="worksheet_type_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    worksheet_ids = fields.One2many(
        string="Worksheets",
        comodel_name="accountant.general_audit_worksheet",
        inverse_name="general_audit_id",
        readonly=True,
    )
    worksheet_control_ids = fields.One2many(
        string="Controls",
        comodel_name="accountant.general_audit_worksheet_control",
        inverse_name="general_audit_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "On Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    trial_balance_ids = fields.One2many(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        inverse_name="general_audit_id",
        readonly=True,
    )
    home_trial_balance_id = fields.Many2one(
        string="# Home Statement Trial Balance",
        comodel_name="accountant.client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    interim_trial_balance_id = fields.Many2one(
        string="# Interim Trial Balance",
        comodel_name="accountant.client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    extrapolation_trial_balance_id = fields.Many2one(
        string="# Extrapolation Trial Balance",
        comodel_name="accountant.client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    previous_trial_balance_id = fields.Many2one(
        string="# Previous Trial Balance",
        comodel_name="accountant.client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    standard_detail_ids = fields.One2many(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    group_detail_ids = fields.One2many(
        string="Group Detail",
        comodel_name="accountant.general_audit_group_detail",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    computation_ids = fields.One2many(
        string="Computations",
        comodel_name="accountant.general_audit_computation",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    standard_adjustment_ids = fields.One2many(
        string="Standard Adjustment",
        comodel_name="accountant.general_audit_adjustment",
        inverse_name="general_audit_id",
        readonly=True,
    )
    group_adjustment_ids = fields.One2many(
        string="Group Adjustment",
        comodel_name="accountant.general_audit_group_adjustment",
        inverse_name="general_audit_id",
        readonly=True,
    )
    adjustment_entry_ids = fields.One2many(
        string="Adjustment Entri(es)",
        comodel_name="accountant.client_adjustment_entry",
        inverse_name="general_audit_id",
        readonly=True,
    )

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    @api.constrains("interim_date_start", "interim_date_end")
    def _check_interim_date_start_end(self):
        for record in self:
            if record.interim_date_start and record.interim_date_end:
                strWarning = _(
                    "Interim Date end must be greater than Interim Date start"
                )
                if record.interim_date_end < record.interim_date_start:
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

    @api.constrains("interim_date_start", "previous_date_end")
    def _check_previous_interim_date(self):
        for record in self:
            if record.interim_date_start and record.previous_date_end:
                strWarning = _(
                    "Interim Date start must be greater than previous Interim Date end"
                )
                if record.previous_date_end >= record.interim_date_start:
                    raise UserError(strWarning)

    @api.onchange(
        "partner_id",
    )
    def onchange_project_id(self):
        self.project_id = False

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
    def onchange_group_detail_ids(self):
        self.update({"group_detail_ids": [(5, 0, 0)]})
        AccountGroup = self.env["accountant.client_account_group"]
        if self.account_type_set_id:
            result = []
            criteria = []
            for detail in AccountGroup.search(criteria):
                result.append(
                    (
                        0,
                        0,
                        {
                            "sequence": detail.sequence,
                            "group_id": detail.id,
                        },
                    )
                )
            self.update({"group_detail_ids": result})

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

    @api.constrains(
        "state",
    )
    def _constrains_state_confirm(self):
        for record in self.sudo():
            record._check_home_tb_exist()
            record._check_home_tb_done()
            record._check_previous_tb_exist()
            record._check_previous_tb_done()
            record._check_interim_tb_done()
            record._check_required_worksheet()
            record._check_additional_worksheet()

    def _check_home_tb_exist(self):
        self.ensure_one()
        if not self.home_trial_balance_id and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: No home statement trial balance
            Solution: Create home statement trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_home_tb_done(self):
        self.ensure_one()
        if self.state == "confirm" and self.home_trial_balance_id.state != "done":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Home statement trial balance is not finished
            Solution: Finish home statement trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_previous_tb_exist(self):
        self.ensure_one()
        if not self.previous_trial_balance_id and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: No previous trial balance
            Solution: Create previous trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_previous_tb_done(self):
        self.ensure_one()
        if self.state == "confirm" and self.previous_trial_balance_id.state != "done":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Previous trial balance is not finished
            Solution: Finish Previous trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_interim_tb_done(self):
        self.ensure_one()
        if (
            self.interim_trial_balance_id
            and self.interim_trial_balance_id.state != "done"
            and self.state == "confirm"
        ):
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Interim trial balance is not finished
            Solution: Finish interim trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_required_worksheet(self):
        self.ensure_one()
        worksheet_state = True
        for worksheet in self.worksheet_control_ids:
            if worksheet.state != "done" and worksheet.required:
                worksheet_state = False
                break

        if not worksheet_state and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: One of the required worksheet not done
            Solution: Create and finish required worksheet
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_additional_worksheet(self):
        self.ensure_one()
        worksheet_state = True
        for worksheet in self.worksheet_control_ids:
            if (
                worksheet.state not in ["done", "cancel"]
                and not worksheet.required
                and worksheet.worksheet_id
            ):
                worksheet_state = False
                break

        if not worksheet_state and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: One of the additional worksheet not done
            Solution: Finish or cancel additional worksheet
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))
