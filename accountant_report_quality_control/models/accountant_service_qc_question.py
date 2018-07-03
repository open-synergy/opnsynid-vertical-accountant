# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountantServiceQcQuestion(models.Model):
    _name = "accountant.service_qc_question"
    _description = "Accountant Service QC Question"

    accountant_service_id = fields.Many2one(
        string="Accountant Service",
        comodel_name="accountant.service",
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
    type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    qc_value_ids = fields.One2many(
        string="Value",
        comodel_name="accountant.service_qc_question_value",
        inverse_name="question_id",
        copy=True,
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
    notes = fields.Text(
        string="Notes",
    )

    @api.multi
    def _prepare_qc_question(self):
        self.ensure_one()
        qc_value_ids = self.qc_value_ids.mapped(lambda r: r.id)
        return {
            "sequence": self.sequence,
            "name": self.name,
            "question_type": self.type,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "possible_qc_value_ids": [(6, 0, qc_value_ids)],
        }
