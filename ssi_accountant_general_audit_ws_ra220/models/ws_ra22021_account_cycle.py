# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA22021AccountCycle(models.Model):
    _name = "ws_ra22021.account_cycle"
    _description = "RA.220.2.1 Account Cycle"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra22021",
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
        related="standard_detail_id.rely_on_control",
        readonly=False,
        store=True,
    )
    toc_analysis = fields.Selection(
        string="ToC Analysis",
        related="standard_detail_id.toc_analysis",
        store=True,
        readonly=False,
    )
    toc_result = fields.Selection(
        string="ToC Result",
        related="standard_detail_id.toc_result",
        store=True,
        readonly=True,
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
