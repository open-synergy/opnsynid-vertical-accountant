# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
    likelihood_risk_occuring = fields.Selection(
        string="Likelihood of Risk Occuring",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    impact_of_risk = fields.Selection(
        string="Magnitude/Impact of Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    other_significant_risk_factor = fields.Boolean(
        string="Other Significant Risk Factor",
        default=False,
    )
    note = fields.Char(
        string="Note",
    )
