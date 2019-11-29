# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class AccountantReport(models.Model):
    _name = "accountant.report"
    _inherit = [
        "accountant.report",
        "base.qr_document",
    ]
