# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAudit1508(models.Model):
    _name = "ws_ra1508"
    _description = "General Audit WS RA.150.8"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra150.worksheet_type_ra1508"

    preassure_ids = fields.One2many(
        string="Opportunity Fraud Factor",
        comodel_name="ws_ra1508.preassure_fraud_factor",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    opportunity_ids = fields.One2many(
        string="Opportunity Fraud Factor",
        comodel_name="ws_ra1508.opportunity_fraud_factor",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    rationalization_ids = fields.One2many(
        string="Rationalization Fraud Factor",
        comodel_name="ws_ra1508.rationalization_fraud_factor",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_preassure_ids(self):
        self.update({"preassure_ids": [(5, 0, 0)]})
        FraudFactor = self.env["accountant.fraud_factor"]
        if self.general_audit_id:
            result = []
            for fraud_factor in FraudFactor.search([("category", "=", "preassure")]):
                result.append(
                    (
                        0,
                        0,
                        {
                            "fraud_factor_id": fraud_factor.id,
                        },
                    )
                )
            self.update({"preassure_ids": result})

    @api.onchange("general_audit_id")
    def onchange_opportunity_ids(self):
        self.update({"opportunity_ids": [(5, 0, 0)]})
        FraudFactor = self.env["accountant.fraud_factor"]
        if self.general_audit_id:
            result = []
            for fraud_factor in FraudFactor.search([("category", "=", "opportunity")]):
                result.append(
                    (
                        0,
                        0,
                        {
                            "fraud_factor_id": fraud_factor.id,
                        },
                    )
                )
            self.update({"opportunity_ids": result})

    @api.onchange("general_audit_id")
    def onchange_rationalization_ids(self):
        self.update({"rationalization_ids": [(5, 0, 0)]})
        FraudFactor = self.env["accountant.fraud_factor"]
        if self.general_audit_id:
            result = []
            for fraud_factor in FraudFactor.search(
                [("category", "=", "rationalization")]
            ):
                result.append(
                    (
                        0,
                        0,
                        {
                            "fraud_factor_id": fraud_factor.id,
                        },
                    )
                )
            self.update({"rationalization_ids": result})
