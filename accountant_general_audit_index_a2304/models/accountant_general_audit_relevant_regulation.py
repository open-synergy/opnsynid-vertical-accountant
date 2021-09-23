# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditRelevantRegulation(models.Model):
    _name = "accountant.general_audit_relevant_regulation"
    _description = "Accountant General Audit Relevant Regulation"

    index_a2304_id = fields.Many2one(
        string="Index A.230.4",
        comodel_name="accountant.general_audit_index_a2304",
        ondelete="cascade",
        required=True,
    )
    regulation_id = fields.Many2one(
        string="Regulation",
        comodel_name="accountant.relevant_regulation",
        required=True,
        ondelete="restrict",
    )
    effect = fields.Text(
        string="Effect",
    )
    related_accountant_type_ids = fields.Many2many(
        string="Related Account Type",
        comodel_name="accountant.client_account_type",
        relation="rel_relevant_regulation_2_acc_type",
        column1="index_a2304_id",
        column2="account_type_id",
    )
    compliance = fields.Selection(
        string="Compliance",
        selection=[
            ("comply", "Comply"),
            ("not_comply", "Not Comply"),
        ],
        required=True,
    )
