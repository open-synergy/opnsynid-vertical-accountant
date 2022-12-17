# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA2203AccountCycle(models.Model):
    _name = "ws_ra2203.account_cycle"
    _description = "RA.220.3 Account Cycle"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra2203",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )
    rely_on_control = fields.Boolean(
        string="Rely on Control",
        default=False,
        related="standard_detail_id.significant_account_rely_on_control",
        readonly=False,
        store=True,
    )
    toc_analysis = fields.Selection(
        string="ToC Analysis",
        related="standard_detail_id.significant_account_toc_analysis",
        store=True,
        readonly=False,
    )
    toc_result = fields.Selection(
        string="ToC Result",
        related="standard_detail_id.significant_account_toc_result",
        store=True,
        readonly=True,
    )
    control_activity_ids = fields.One2many(
        string="Control Activity",
        comodel_name="ws_ra2203.account_control_activity",
        inverse_name="account_id",
    )

    @api.onchange(
        "rely_on_control",
        "toc_analysis",
    )
    def _onchange_toc_result(self):
        result = "high"
        if self.rely_on_control and self.toc_analysis == "effective":
            result = "low"
        self.toc_result = result
