# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1507FinancialReportPreparation(models.Model):
    _name = "ws_ra1507.financial_report_preparation"
    _description = "RA.150.7 Financial Report Preparation"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1507",
        required=True,
        ondelete="cascade",
    )
    preparation_item_id = fields.Many2one(
        string="Preparation Item",
        comodel_name="accountant.financial_report_preparation",
        ondelete="restrict",
    )
    process_description = fields.Text(
        string="Process Description",
        required=False,
    )
    controlling_activity = fields.Text(
        string="Controlling Activity",
        required=False,
    )
    audit_relevancy = fields.Text(
        string="Relevancy to Audit",
        required=False,
    )
    misstatement_identification = fields.Text(
        string="Misstatement Identificaton",
        required=False,
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        relation="rel_financial_report_prep_2_standard_detail",
        column1="praparation_id",
        column2="standard_detail_id",
    )
