# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditIndexA1101(models.Model):
    _name = "accountant.general_audit_index_a1101"
    _description = "Accountant General Audit Index A.110.1"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "accountant_general_audit_index_a1101.worksheet_type_a1101"

    type_id = fields.Many2one(
        related="worksheet_id.parent_type_id",
    )
    question_1a = fields.Selection(
        string="Question 1a",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_1b = fields.Selection(
        string="Question 1b",
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        readonly=True,
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
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
