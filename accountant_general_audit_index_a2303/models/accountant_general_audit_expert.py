# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditExpert(models.Model):
    _name = "accountant.general_audit_expert"
    _description = "Accountant General Audit Expert"

    index_a2303_id = fields.Many2one(
        string="Index A.230.3",
        comodel_name="accountant.general_audit_index_a2303",
        ondelete="cascade",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        # related="general_audit_id.partner_id",
        required=True,
        ondelete="restrict",
    )
    expertise = fields.Char(
        string="Expertise",
        required=True,
    )
    related_account_type_ids = fields.Many2many(
        string="Related Account Type",
        comodel_name="accountant.client_account_type",
        relation="rel_index_a2303_exprert_2_acc_type",
        column1="expert_id",
        column2="account_type_id",
    )
