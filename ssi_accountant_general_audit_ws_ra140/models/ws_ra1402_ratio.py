# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1402Ratio(models.Model):
    _name = "ws_ra1402.ratio"
    _description = "WS RA.140.2 Ratio"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1402",
        required=True,
        ondelete="cascade",
    )
    general_audit_computation_item_id = fields.Many2one(
        string="General Audit Computation Item",
        comodel_name="accountant.general_audit_computation",
        required=True,
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        comodel_name="accountant.trial_balance_computation_item",
        related="general_audit_computation_item_id.computation_item_id",
        store=True,
    )
    extrapolation_amount = fields.Float(
        string="Extrapolation Amount",
        related="general_audit_computation_item_id.extrapolation_amount",
        store=True,
    )
    interim_amount = fields.Float(
        string="Interim Amount",
        related="general_audit_computation_item_id.interim_amount",
        store=True,
    )
    previous_amount = fields.Float(
        string="Previous Amount",
        related="general_audit_computation_item_id.previous_amount",
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    analysis = fields.Char(
        string="Analysis",
    )
