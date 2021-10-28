# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditOpinion(models.Model):
    _name = "accountant.general_audit_opinion"
    _description = "General Audit Opinion"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
