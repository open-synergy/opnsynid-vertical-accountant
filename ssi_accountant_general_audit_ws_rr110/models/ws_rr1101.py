# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA1101(models.Model):
    _name = "ws_rr1101"
    _description = "General Audit WS RA.110.1"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_rr110.worksheet_type_rr1101"

    balance_type = fields.Selection(
        string="Balance Type",
        selection=[
            ("interim", "Interim"),
            ("home", "Home Statement"),
        ],
        default="home",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
        currency_field="currency_id",
    )
    result = fields.Selection(
        string="Result",
        selection=[
            ("high", "High"),
            ("moderate", "Moderate"),
        ],
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    account_ids = fields.One2many(
        string="Accounts",
        comodel_name="ws_rr1101.account",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    account_comparison_ids = fields.One2many(
        string="Account Comparisons",
        comodel_name="ws_rr1101.account_comparison",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    computation_comparison_ids = fields.One2many(
        string="Computation Comparisons",
        comodel_name="ws_rr1101.computation_comparison",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "balance_type",
        "standard_detail_id",
        "standard_detail_id.interim_balance",
        "standard_detail_id.home_statement_balance",
    )
    def _compute_balance(self):
        for record in self:
            result = 0.0
            if record.balance_type == "interim":
                result = record.standard_detail_id.interim_balance
            else:
                result = record.standard_detail_id.home_statement_balance
            record.balance = result

    @api.onchange("general_audit_id")
    def onchange_standard_detail_id(self):
        self.standard_detail_id = False

    @api.onchange("general_audit_id", "standard_detail_id")
    def onchange_account_ids(self):
        Detail = self.env["accountant.general_audit_detail"]
        self.update({"account_ids": [(5, 0, 0)]})
        if self.general_audit_id and self.standard_detail_id:
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
                ("type_id", "=", self.standard_detail_id.type_id.id),
            ]
            result = []
            for detail in Detail.search(criteria):
                result.append(
                    (
                        0,
                        0,
                        {
                            "detail_id": detail.id,
                        },
                    )
                )
            self.update({"account_ids": result})
