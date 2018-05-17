# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accountant Firm Partner Arrangement",
    "version": "8.0.1.5.0",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "license": "AGPL-3",
    "depends": [
        "accountant_app",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/accountant_config_setting_views.xml",
        "views/accountant_partner_arrangement_views.xml",
    ],
    "installable": True,
}
