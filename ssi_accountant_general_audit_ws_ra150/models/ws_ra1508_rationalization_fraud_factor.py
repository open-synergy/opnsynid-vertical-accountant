# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1508RationalizationFraudFactor(models.Model):
    _name = "ws_ra1508.rationalization_fraud_factor"
    _description = "RA.150.8 Rationalization Fraud Factor"
    _order = "worksheet_id, category, sequence"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1508",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="fraud_factor_id.sequence",
        store=True,
    )
    category = fields.Selection(
        string="Category",
        related="fraud_factor_id.category",
        store=True,
    )
    fraud_factor_id = fields.Many2one(
        string="Fraud Factor",
        comodel_name="accountant.fraud_factor",
        ondelete="restrict",
    )
    tcwg = fields.Text(string="TCWG", required=True, default="-")
    management = fields.Text(string="Management", required=True, default="-")
    other = fields.Text(string="Other Department", required=True, default="-")
    standard_detail_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        relation="rel_rational_fraud_2_standard_detail",
        column1="fraud_id",
        column2="standard_detail_id",
    )
