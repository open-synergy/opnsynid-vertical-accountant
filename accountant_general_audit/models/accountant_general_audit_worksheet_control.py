# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditWorksheetControl(models.Model):
    _name = "accountant.general_audit_worksheet_control"
    _description = "Accountant General Audit Worksheet Control"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.general_audit_worksheet_type",
        required=False,
    )
    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="accountant.general_audit_worksheet",
    )
    required = fields.Boolean(
        string="Required",
        default=True,
    )
