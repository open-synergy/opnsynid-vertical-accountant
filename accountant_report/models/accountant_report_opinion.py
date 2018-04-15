# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp.tools.translate import _


class AccountantReportOpinion(models.Model):
    _name = "accountant.report_opinion"
    _description = "Opini Laporan Akhir"

    name = fields.Char(
        string=_("Opinion"),
        required=True,
        translate=False,
        readonly=False,
    )
    description = fields.Text(
        string=_("Description"),
        required=False,
        translate=False,
        readonly=False,
    )
    active = fields.Boolean(
        string=_("Active"),
        required=False,
        translate=False,
        readonly=False,
        default=True,
    )
    code = fields.Char(
        string=_("Code"),
        required=True,
        translate=False,
        readonly=False,
    )
