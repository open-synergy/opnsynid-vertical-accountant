# -*- coding: utf-8 -*-
# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditIndexA2202Detail(models.Model):
    _name = "accountant.general_audit_index_a2202_detail"
    _description = "Accountant General Audit Index A.220.2 Details"
    _order = "sequence, index_a2202_id, id"

    index_a2202_id = fields.Many2one(
        string="# Index A.220.2",
        comodel_name="accountant.general_audit_index_a2202",
        required=True,
        ondelete="cascade",
    )
    computation_id = fields.Many2one(
        string="Computation",
        comodel_name="accountant.client_trial_balance_computation",
        required=True,
    )
    computation_item_id = fields.Many2one(
        string="Item",
        comodel_name="accountant.trial_balance_computation_item",
        related="computation_id.computation_item_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="computation_id.computation_item_id.sequence",
        store=True,
    )
    balance = fields.Float(
        string="Balance",
        related="computation_id.amount",
        store=True,
    )
    extrapolation_balance = fields.Float(
        string="Extrapolation Balance",
        related="computation_id.amount_extrapolation",
        store=True,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        related="computation_id.amount_previous",
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    note = fields.Text(
        string="Note",
    )
