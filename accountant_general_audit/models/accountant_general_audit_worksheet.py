# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditWorksheet(models.Model):
    _name = "accountant.general_audit_worksheet"
    _description = "Accountant General Audit Worksheet"
    _order = "general_audit_id, parent_type_id, id"

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.general_audit_worksheet_type",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="accountant.general_audit_worksheet_conclusion",
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("valid", "Valid"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
