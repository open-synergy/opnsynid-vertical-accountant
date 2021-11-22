# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditIndexF010102(models.Model):
    _name = "accountant.general_audit_index_f010102"
    _description = "Accountant General Audit Index F.01.01.02"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "accountant_general_audit_index_f010102.worksheet_type_f010102"

    # Related
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

    # Worksheet fields
    question_1 = fields.Selection(
        string="Question 1",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_2 = fields.Selection(
        string="Question 2",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_3 = fields.Selection(
        string="Question 3",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_4 = fields.Selection(
        string="Question 4",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_5 = fields.Selection(
        string="Question 5",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_6 = fields.Selection(
        string="Question 6",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_7 = fields.Selection(
        string="Question 7",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_8 = fields.Selection(
        string="Question 8",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_9 = fields.Selection(
        string="Question 9",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
