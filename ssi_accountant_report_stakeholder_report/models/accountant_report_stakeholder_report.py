# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval as eval


class AccountantReportStakeholderReport(models.Model):
    _name = "accountant.report_stakeholder_report"
    _description = "Accounting Report Stakeholder Report"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
    ]
    _order = "general_audit_id, parent_type_id, id"

    _approval_from_state = "draft"
    _approval_to_state = "valid"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "done"

    _done_state = "valid"

    @api.model
    def _get_policy_field(self):
        res = super(AccountantReportStakeholderReport, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
        ]
        res += policy_field
        return res

    @api.model
    def _default_type_id(self):
        return False

    @api.depends(
        "type_id",
    )
    def _compute_policy(self):
        _super = super(AccountantReportStakeholderReport, self)
        _super._compute_policy()

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
        default=lambda self: self._default_type_id(),
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
        copy=False,
        readonly=True,
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
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    # Policy Field
    done_ok = fields.Boolean(
        string="Can Valid",
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaulate_domain_stakeholder_type(self):
        self.ensure_one()
        localdict = self._get_localdict()
        try:
            eval(self.type_id.domain, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception:
            res = False
        return res

    def _prepare_criteria_accountant_report(self):
        self.ensure_one()
        criteria = [
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
        ]
        domain = self._evaulate_domain_stakeholder_type()
        if domain:
            criteria += domain
        return criteria

    def get_accountant_report_ids(self):
        self.ensure_one()
        result = []
        obj_accountant_report = self.env["accountant.report"]
        criteria = self._prepare_criteria_accountant_report()
        accountant_report_ids = obj_accountant_report.search(criteria)
        if accountant_report_ids:
            result = accountant_report_ids.ids
        return result

    def action_populate_accountant_report(self):
        for record in self:
            accountant_report_ids = record.get_accountant_report_ids()
            record.accountant_report_ids = [(6, 0, accountant_report_ids)]

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Start Date cannot be greater than End Date")
                if record.date_start > record.date_end:
                    raise UserError(strWarning)
