# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1505TrendBusinessEnvironment(models.Model):
    _name = "ws_ra1505.trend_business_environment"
    _description = "RA.150.5 Similar Business Trend Understanding"
    _order = "worksheet_id, sequence"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1505",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    understanding = fields.Text(
        string="Undertanding",
        required=True,
    )
    impact_to_financial_report = fields.Text(
        string="Impact to Financial report",
        required=True,
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        relation="rel_trend_2_general_audit_standard_detail",
        column1="business_environment_id",
        column2="standard_detail_id",
    )
