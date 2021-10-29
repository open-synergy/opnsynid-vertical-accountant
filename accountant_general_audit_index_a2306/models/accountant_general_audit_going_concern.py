# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditGoingConcern(models.Model):
    _name = "accountant.general_audit_going_concern"
    _description = "Accountant General Audit Going Concern"

    index_a2306_id = fields.Many2one(
        string="Index A.230.6",
        comodel_name="accountant.general_audit_index_a2306",
        ondelete="cascade",
        required=True,
    )
    going_concern_id = fields.Many2one(
        string="Going Concern",
        comodel_name="accountant.going_concern",
        ondelete="restrict",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.going_concern_category",
        related="going_concern_id.category_id",
        readonly=True,
        store=True,
    )
    existence = fields.Selection(
        string="Existence",
        selection=[
            ("exist", "Exist"),
            ("not_exist", "Not Exist"),
        ],
        copy=False,
        default="exist",
        required=True,
    )
    consideration = fields.Text(
        string="Consideration",
    )
