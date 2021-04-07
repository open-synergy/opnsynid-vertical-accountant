# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Quality Control for Accountant Report",
    "version": "8.0.1.0.1",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_report",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/accountant_service_views.xml",
        "views/accountant_service_qc_question_views.xml",
        "views/accountant_report_views.xml",
    ],
    "installable": True,
}
