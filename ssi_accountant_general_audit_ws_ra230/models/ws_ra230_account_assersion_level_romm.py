# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WS230AccountAssersionLevelRomm(models.Model):
    _name = "ws_ra230.account_assersion_level_romm"
    _description = "General Audit WS RA.230 - Account Assersion Level ROMM"

    worksheet_id = fields.Many2one(
        string="# RA.210",
        comodel_name="ws_ra230",
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
    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        comodel_name="accountant.assersion_type",
        relation="rel_ra230_2_pr_assersion_type",
        column1="standard_detail_id",
        column2="assersion_type_id",
        inverse="_inverse_to_standard_detail",
    )
    romm = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        related="standard_detail_id.romm",
        readonly=False,
        store=True,
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
        related="standard_detail_id.planned_response_analytic_procedure",
        readonly=False,
        store=True,
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
        related="standard_detail_id.planned_response_tod",
        readonly=False,
        store=True,
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
        related="standard_detail_id.planned_response_interim",
        readonly=False,
        store=True,
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
        related="standard_detail_id.planned_response_ye",
        readonly=False,
        store=True,
    )

    def _inverse_to_standard_detail(self):
        for record in self:
            record.standard_detail_id.write(
                {
                    "pr_assersion_type_ids": [(6, 0, record.pr_assersion_type_ids.ids)],
                }
            )
