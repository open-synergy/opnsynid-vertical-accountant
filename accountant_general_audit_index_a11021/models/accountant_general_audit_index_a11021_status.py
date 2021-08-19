# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditIndexA11021Status(models.Model):
    _name = "accountant.general_audit_index_a11021_status"
    _description = "Accountant General Audit Index A.1102.1 Status"
    _order = "sequence, id"

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
    note = fields.Text(
        string="Note",
        required=False,
    )
