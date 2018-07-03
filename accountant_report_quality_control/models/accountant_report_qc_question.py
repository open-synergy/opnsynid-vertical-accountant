# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountantReportQcQuestion(models.Model):
    _name = "accountant.report_qc_question"
    _description = "Accountant Report QC Question"

    @api.multi
    @api.depends(
        "possible_qc_value_ids", "min_value", "max_value",
        "question_type")
    def _get_valid_values(self):
        for qc in self:
            if qc.question_type == "qualitative":
                qc.valid_values = ", ".join(
                    [x.name for x in qc.possible_qc_value_ids if x.ok])
            elif qc.question_type == "quantitative":
                qc.valid_values = "%s-%s" % (qc.min_value, qc.max_value)

    @api.multi
    @api.depends(
        "question_type", "max_value", "min_value",
        "quantitative_value", "qualitative_value_id",
        "possible_qc_value_ids")
    def _get_result(self):
        for qc in self:
            if qc.question_type == "qualitative":
                qc.success = qc.qualitative_value_id.ok
            else:
                qc.success = qc.max_value >= \
                    qc.quantitative_value >= qc.min_value

    accountant_report_id = fields.Many2one(
        string="Accountant Report",
        comodel_name="accountant.report",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    name = fields.Char(
        string="Question",
        required=True,
    )
    question_type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    possible_qc_value_ids = fields.Many2many(
        string="Posible Values",
        comodel_name="accountant.service_qc_question_value",
        relation="rel_account_report_2_qc_value",
        column1="report_id",
        column2="value_id",
    )
    qualitative_value_id = fields.Many2one(
        string="Qualitative Value",
        comodel_name="accountant.service_qc_question_value",
        domain="[('id', 'in', possible_qc_value_ids[0][2])]",
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
    )
    min_value = fields.Float(
        string="Min. Value",
    )
    max_value = fields.Float(
        string="Max. Value",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    valid_values = fields.Char(
        string="Valid Values",
        compute="_get_valid_values",
        store=True,
    )
    success = fields.Boolean(
        string="Success?",
        compute="_get_result",
        store=True,
    )
    notes = fields.Text(
        string="Notes",
    )
