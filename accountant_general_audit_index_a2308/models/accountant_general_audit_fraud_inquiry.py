# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditFraudInquiry(models.Model):
    _name = "accountant.general_audit_fraud_inquiry"
    _description = "Accountant General Audit Fraud Inquiry"

    index_a2308_id = fields.Many2one(
        string="Index A.230.8",
        comodel_name="accountant.general_audit_index_a2308",
        ondelete="cascade",
        required=True,
    )
    fraud_inquiry_id = fields.Many2one(
        string="Fraud Inquiry",
        comodel_name="accountant.fraud_inquiry_item",
        required=True,
        ondelete="restrict",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.fraud_inquiry_item_category",
        related="fraud_inquiry_id.category_id",
        readonly=True,
        store=True,
    )
    tcwg_respon = fields.Text(
        string="TCWG Respon",
    )
    management_respon = fields.Text(
        string="Management Respon",
    )
    other_respon = fields.Text(
        string="Other Respon",
    )
    account_type_ids = fields.Many2many(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        relation="rel_relevant_regulation_2_acc_type",
        column1="index_a2308_id",
        column2="account_type_id",
    )
