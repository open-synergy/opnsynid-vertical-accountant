# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class AccountantClientTrialBalanceStandardDetail(models.Model):
    _name = "accountant.client_trial_balance_standard_detail"
    _description = "Accountant Client Trial Balance Standard Detail"
    _order = "sequence, trial_balance_id, id"

    @api.depends(
        "trial_balance_id",
        "trial_balance_id.date_start",
        "trial_balance_id.date_end",
        "trial_balance_id.previous_date_start",
        "trial_balance_id.previous_date_end",
        "trial_balance_id.interim_date_start",
        "trial_balance_id.interim_date_end",
        "type_id",
        "trial_balance_id.detail_ids",
        "trial_balance_id.detail_ids.type_id",
        "trial_balance_id.detail_ids.balance",
    )
    def _compute_balance(self):
        obj_detail = self.env["accountant.client_trial_balance_detail"]
        for document in self:
            balance = 0.0
            if document.trial_balance_id.trial_balance_type == "extrapolation":
                python_code = document.type_id.python_code
                localdict = document._get_localdict()
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    balance = localdict["result"]
                except Exception:
                    balance = 8.0
            else:
                criteria = [
                    ("trial_balance_id", "=", document.trial_balance_id.id),
                    ("type_id", "=", document.type_id.id),
                ]
                for detail in obj_detail.search(criteria):
                    balance += detail.balance
            document.balance = balance

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="trial_balance_id.currency_id",
        store=True,
    )
    balance = fields.Monetary(
        string="Balance",
        required=False,
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )

    def _get_localdict(self):
        self.ensure_one()
        StandardDetail = self.env["accountant.general_audit_standard_detail"]
        criteria = [
            ("general_audit_id", "=", self.trial_balance_id.general_audit_id.id),
            ("type_id", "=", self.type_id.id),
        ]
        standard_detail = False
        standard_details = StandardDetail.search(criteria)
        if len(standard_details) > 0:
            standard_detail = standard_details[0]
        return {
            "env": self.env,
            "document": self,
            "standard_detail": standard_detail,
            "tb": self.trial_balance_id,
        }
