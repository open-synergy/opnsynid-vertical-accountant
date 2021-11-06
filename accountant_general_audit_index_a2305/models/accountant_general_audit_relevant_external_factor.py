# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditRelevantExternalFactor(models.Model):
    _name = "accountant.general_audit_relevant_external_factor"
    _description = "Accountant General Audit Relevant External Factor"

    index_a2305_id = fields.Many2one(
        string="Index A.230.5",
        comodel_name="accountant.general_audit_index_a2305",
        ondelete="cascade",
        required=True,
    )
    external_factor_id = fields.Many2one(
        string="External Factor",
        comodel_name="accountant.relevant_external_factor",
        ondelete="restrict",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.relevant_external_factor_category",
        related="external_factor_id.category_id",
        readonly=True,
        store=True,
    )
    impact = fields.Text(
        string="Impact",
        required=True,
    )
    account_type_ids = fields.Many2many(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        relation="rel_relevant_external_factor_2_acc_type",
        column1="index_a2305_id",
        column2="account_type_id",
    )
