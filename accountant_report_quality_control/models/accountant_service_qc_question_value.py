# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountantServiceQcQuestionValue(models.Model):
    _name = "accountant.service_qc_question_value"
    _description = "Accountant Service QC Question Value"

    name = fields.Char(
        string="Value",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    ok = fields.Boolean(
        string="Correct Answer",
    )
    description = fields.Text(
        string="Description",
    )
    question_id = fields.Many2one(
        string="Question",
        comodel_name="accountant.service_qc_question_value",
        required=True,
    )
