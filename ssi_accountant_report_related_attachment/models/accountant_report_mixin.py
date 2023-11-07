# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class AccountantReportMixin(models.AbstractModel):
    _name = "accountant.report_mixin"
    _inherit = [
        "accountant.report_mixin",
        "mixin.related_attachment",
    ]
    _related_attachment_create_page = True
