# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1503PreviousSignificantInformation(models.Model):
    _name = "ws_ra1503.previous_significant_information"
    _description = "RA.150.3 Previous Audit Significant Information"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1503",
        required=True,
        ondelete="cascade",
    )
    summary = fields.Char(
        string="Summary",
        required=True,
    )
    documentation = fields.Char(
        string="Documentation",
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        relation="rel_prev_sig_info_2_general_audit_standard_detail",
        column1="information_id",
        column2="standard_detail_id",
        required=False,
    )
