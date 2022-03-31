# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantReportOpinion(models.Model):
    _name = "accountant.report_opinion"
    _description = "Accountant Report Opinion"
    _order = "id"

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
