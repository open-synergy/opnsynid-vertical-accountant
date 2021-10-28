# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditWorksheetType(models.Model):
    _name = "accountant.general_audit_worksheet_type"
    _description = "General Audit Worksheet Type"
    _order = "sequence, code"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    parent_id = fields.Many2one(
        string="Parent Worksheet",
        comodel_name="accountant.general_audit_worksheet_type",
    )
    max_number_allowed = fields.Integer(
        string="Max. Number Allowed Per Audit",
        required=True,
        default=1,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
    )
