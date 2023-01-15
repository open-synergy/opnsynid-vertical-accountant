# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WSRR110Account(models.Model):
    _name = "ws_rr110.account"
    _description = "General Audit WS RR.110 Account"

    worksheet_id = fields.Many2one(
        string="# RR.110",
        comodel_name="ws_rr110",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    r1101_id = fields.Many2one(
        string="# RR.110",
        comodel_name="ws_rr1101",
        compute="_compute_r1101_id",
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="accountant.general_audit_worksheet_conclusion",
        related="r1101_id.conclusion_id",
        store=True,
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
        related="r1101_id.conclusion",
        store=True,
    )
    result = fields.Selection(
        string="Result",
        related="r1101_id.result",
        store=True,
    )

    @api.depends(
        "standard_detail_id",
    )
    def _compute_r1101_id(self):
        Worksheet = self.env["ws_rr110"]
        for record in self:
            result = False
            criteria = [
                ("standard_detail_id", "=", record.standard_detail_id.id),
                ("balance_type", "=", record.worksheet_id.balance_type.id),
            ]
            worksheets = Worksheet.search(criteria)
            if len(worksheets) > 0:
                result = worksheets[0]
            record.r1101_id = result
