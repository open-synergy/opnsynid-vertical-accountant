# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditIndexA2305(models.Model):
    _name = "accountant.general_audit_index_a2305"
    _description = "Accountant General Audit Index A.230.5"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "accountant_general_audit_index_a2305.worksheet_type_a2305"

    type_id = fields.Many2one(
        related="worksheet_id.parent_type_id",
        store=True,
    )
    date_start = fields.Date(
        related="general_audit_id.date_start",
        store=True,
    )
    date_end = fields.Date(
        related="general_audit_id.date_end",
        store=True,
    )
    interim_date_start = fields.Date(
        related="general_audit_id.interim_date_start",
        store=True,
    )
    interim_date_end = fields.Date(
        related="general_audit_id.interim_date_end",
        store=True,
    )
    previous_date_start = fields.Date(
        related="general_audit_id.previous_date_start",
        store=True,
    )
    previous_date_end = fields.Date(
        related="general_audit_id.previous_date_end",
        store=True,
    )
    account_type_set_id = fields.Many2one(
        related="general_audit_id.account_type_set_id",
        store=True,
    )
    company_id = fields.Many2one(
        related="general_audit_id.company_id",
        store=True,
    )
    partner_id = fields.Many2one(
        related="general_audit_id.partner_id",
        store=True,
    )
    relevant_external_factor_ids = fields.One2many(
        string="External Factor",
        comodel_name="accountant.general_audit_relevant_external_factor",
        inverse_name="index_a2305_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
