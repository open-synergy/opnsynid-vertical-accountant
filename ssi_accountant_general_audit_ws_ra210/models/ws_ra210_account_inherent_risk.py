# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS210AccountInherentRisk(models.Model):
    _name = "ws_ra210.account_inherent_risk"
    _description = "General Audit WS RA.210 Account Inherent Risk"

    worksheet_id = fields.Many2one(
        string="# RA.210",
        comodel_name="ws_ra210",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )

    inherent_risk_factor_a = fields.Boolean(
        string="Inherent Risk Factor A",
        default=False,
    )
    inherent_risk_factor_b = fields.Boolean(
        string="Inherent Risk Factor B",
        default=False,
    )
    inherent_risk_factor_c = fields.Boolean(
        string="Inherent Risk Factor C",
        default=False,
    )
    inherent_risk_factor_d = fields.Boolean(
        string="Inherent Risk Factor D",
        default=False,
    )
    inherent_risk_factor_e = fields.Boolean(
        string="Inherent Risk Factor E",
        default=False,
    )
    inherent_risk_factor_f = fields.Boolean(
        string="Inherent Risk Factor F",
        default=False,
    )
    inherent_risk_factor_g = fields.Boolean(
        string="Inherent Risk Factor G",
        default=False,
    )
    inherent_risk_factor_h = fields.Boolean(
        string="Inherent Risk Factor H",
        default=False,
    )
    inherent_risk_factor_i = fields.Boolean(
        string="Inherent Risk Factor I",
        default=False,
    )
    inherent_risk_factor_j = fields.Boolean(
        string="Inherent Risk Factor J",
        default=False,
    )

    @api.depends(
        "standard_detail_id",
        "standard_detail_id.preassure_ok",
        "standard_detail_id.opportunity_ok",
        "standard_detail_id.rationalization_ok",
    )
    def _compute_fraud_risk(self):
        for record in self:
            result = False
            std = record.standard_detail_id
            if std.preassure_ok or std.opportunity_ok or std.rationalization_ok:
                result = True
            record.fraud_risk = result

    fraud_risk = fields.Boolean(
        string="Fraud Risk", store=True, compute="_compute_fraud_risk"
    )
    likelihood_risk_occuring = fields.Selection(
        string="Likelihood of Risk Occuring",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
    )
    impact_of_risk = fields.Selection(
        string="Magnitude/Impact of Risk",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
    )

    @api.depends(
        "likelihood_risk_occuring",
        "impact_of_risk",
        "inherent_risk_factor_f",
        "inherent_risk_factor_g",
        "inherent_risk_factor_h",
        "inherent_risk_factor_i",
        "inherent_risk_factor_j",
        "fraud_risk",
        "other_significant_risk_factor",
    )
    def _compute_risk(self):
        for record in self:
            inherent_risk = significant_risk = False
            if record.likelihood_risk_occuring == "high":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                    if (
                        record.inherent_risk_factor_f
                        or record.inherent_risk_factor_g
                        or record.inherent_risk_factor_h
                        or record.inherent_risk_factor_i
                        or record.inherent_risk_factor_j
                        or record.fraud_risk
                    ) or record.other_significant_risk_factor:
                        significant_risk = True
                elif record.impact_of_risk == "low":
                    inherent_risk = "medium"
            elif record.likelihood_risk_occuring == "low":
                if record.impact_of_risk == "high":
                    inherent_risk = "high"
                elif record.impact_of_risk == "low":
                    inherent_risk = "low"
            record.inherent_risk = inherent_risk
            record.significant_risk = significant_risk

    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        compute="_compute_risk",
        store=True,
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
        compute="_compute_risk",
        store=True,
    )

    other_significant_risk_factor = fields.Boolean(
        string="Other Significant Risk Factor",
        default=False,
    )
    note = fields.Char(
        string="Note",
    )
