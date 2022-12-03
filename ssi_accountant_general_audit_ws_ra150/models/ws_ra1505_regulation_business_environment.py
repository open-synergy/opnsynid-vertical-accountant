# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1505RegulationBusinessEnvironment(models.Model):
    _name = "ws_ra1505.regulation_business_environment"
    _description = "RA.150.5 Regulation Change Understanding"
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
        relation="rel_regulation_2_general_audit_standard_detail",
        column1="business_environment_id",
        column2="standard_detail_id",
        required=False,
    )
