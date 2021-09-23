# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def _load_partner_identification_data(cr):
    try:
        from openupgradelib import load_data

        load_data(
            cr,
            "partner_identification_cpa_firm_license",
            "/data/res_partner_id_category_data.xml",
        )
    except Exception:
        return
