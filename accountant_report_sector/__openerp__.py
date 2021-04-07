# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sector Information on Accountant Report",
    "version": "8.0.1.1.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_report",
        "partner_sector",
    ],
    "data": [
        "views/accountant_report_views.xml",
        "views/res_partner_sector_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
