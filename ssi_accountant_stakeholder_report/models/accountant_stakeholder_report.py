# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class AccountantStakeholderReport(models.Model):
    _name = "accountant_stakeholder_report"
    _description = "Accountant Stakeholder Report"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]
    _order = "date desc, id"

    # Attribute related to multiple approval
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attribute related to sequence
    _create_sequence_state = "done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    type_id = fields.Many2one(
        string="Type",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="accountant_stakeholder_report_type",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        translate=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_service_ids = fields.Many2many(
        comodel_name="accountant.service",
        string="Allowed Services",
        compute="_compute_allowed_service_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_creditor_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Allowed Creditors",
        compute="_compute_allowed_creditor_ids",
        store=False,
        compute_sudo=True,
    )
    assurance_report_ids = fields.Many2many(
        string="Assurance Reports",
        comodel_name="accountant.assurance_report",
        relation="rel_stakeholder_2_assurance_report",
        column1="stakeholder_report_id",
        column2="assurance_report_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    nonassurance_report_ids = fields.Many2many(
        string="Non-Assurance Reports",
        comodel_name="accountant.nonassurance_report",
        relation="rel_stakeholder_2_nonassurance_report",
        column1="stakeholder_report_id",
        column2="nonassurance_report_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _get_policy_field(self):
        res = super(AccountantStakeholderReport, self)._get_policy_field()
        policy_field = [
            "done_ok",
            "confirm_ok",
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

    @api.depends(
        "type_id",
    )
    def _compute_allowed_service_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="accountant.service",
                    method_selection=record.type_id.accountant_service_selection_method,
                    manual_recordset=record.type_id.accountant_service_ids,
                    domain=record.type_id.accountant_service_domain,
                    python_code=record.type_id.accountant_service_python_code,
                )
            record.allowed_service_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_creditor_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.partner",
                    method_selection=record.type_id.creditor_selection_method,
                    manual_recordset=record.type_id.creditor_ids,
                    domain=record.type_id.creditor_domain,
                    python_code=record.type_id.creditor_python_code,
                )
            record.allowed_creditor_ids = result

    def action_populate_assurance_report(self):
        for record in self.sudo():
            record._populate_assurance_report()

    def action_populate_nonassurance_report(self):
        for record in self.sudo():
            record._populate_nonassurance_report()

    def _prepare_report_domain(self):
        self.ensure_one()
        result = [
            ("primary_creditor_id", "in", self.allowed_creditor_ids.ids),
            ("service_id", "in", self.allowed_service_ids.ids),
            ("state", "=", "done"),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
        ]
        return result

    def _populate_assurance_report(self):
        self.ensure_one()
        criteria = self._prepare_report_domain()
        criteria += [
            (
                "service_id.assurance",
                "=",
                True,
            )
        ]
        Report = self.env["accountant.assurance_report"]
        reports = Report.search(criteria)
        self.write({"assurance_report_ids": [(6, 0, reports.ids)]})

    def _populate_nonassurance_report(self):
        self.ensure_one()
        criteria = self._prepare_report_domain()
        criteria += [
            (
                "service_id.assurance",
                "=",
                False,
            )
        ]
        Report = self.env["accountant.nonassurance_report"]
        reports = Report.search(criteria)
        self.write({"nonassurance_report_ids": [(6, 0, reports.ids)]})

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
