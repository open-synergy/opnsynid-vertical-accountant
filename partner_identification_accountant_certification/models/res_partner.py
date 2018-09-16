# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    accountant_cpa_license = fields.Char(
        string="Certified Public Accountant (CPA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cpa_license", "accountant_cpa"),
        search=lambda s, *a: s._search_identification(
            "accountant_cpa", *a),
    )
    accountant_cfa_license = fields.Char(
        string="Certified Financial Analyst (CFA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cfa_license", "accountant_cfa"),
        search=lambda s, *a: s._search_identification(
            "accountant_cfa", *a),
    )
    accountant_cma_license = fields.Char(
        string="Certified Management Accountant (CMA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cma_license", "accountant_cma"),
        search=lambda s, *a: s._search_identification(
            "accountant_cma", *a),
    )
    accountant_ea_license = fields.Char(
        string="Enrolled Agent (EA) License",
        compute=lambda s: s._compute_identification(
            "accountant_ea_license", "accountant_ea"),
        search=lambda s, *a: s._search_identification(
            "accountant_ea", *a),
    )
    accountant_cia_license = fields.Char(
        string="Certified Internal Auditor (CIA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cia_license", "accountant_cia"),
        search=lambda s, *a: s._search_identification(
            "accountant_cia", *a),
    )
    accountant_cisa_license = fields.Char(
        string="Certified Information System Auditor (CISA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cisa_license", "accountant_cisa"),
        search=lambda s, *a: s._search_identification(
            "accountant_cisa", *a),
    )
    accountant_cfe_license = fields.Char(
        string="Certified Fraud Examiner (CFE) License",
        compute=lambda s: s._compute_identification(
            "accountant_cfe_license", "accountant_cfe"),
        search=lambda s, *a: s._search_identification(
            "accountant_cfe", *a),
    )
    accountant_cgap_license = fields.Char(
        string="Certified Government Audition Professional (CGAP) License",
        compute=lambda s: s._compute_identification(
            "accountant_cgap_license", "accountant_cgap"),
        search=lambda s, *a: s._search_identification(
            "accountant_cgap", *a),
    )
    accountant_cba_license = fields.Char(
        string="Certified Bank Auditor (CBA) License",
        compute=lambda s: s._compute_identification(
            "accountant_cba_license", "accountant_cba"),
        search=lambda s, *a: s._search_identification(
            "accountant_cba", *a),
    )
    accountant_ca_license = fields.Char(
        string="Certified Accountant (CA) License",
        compute=lambda s: s._compute_identification(
            "accountant_ca_license", "accountant_ca"),
        search=lambda s, *a: s._search_identification(
            "accountant_ca", *a),
    )
