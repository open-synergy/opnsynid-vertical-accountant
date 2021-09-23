# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantReportOpinion(models.Model):
    _name = "accountant.report_opinion"
    _description = "Opini Laporan Akhir"

    name = fields.Char(
        string="Opinion",
        required=True,
        translate=False,
        readonly=False,
    )
    description = fields.Text(
        string="Description",
        required=False,
        translate=False,
        readonly=False,
    )
    active = fields.Boolean(
        string="Active",
        required=False,
        translate=False,
        readonly=False,
        default=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
        translate=False,
        readonly=False,
    )
