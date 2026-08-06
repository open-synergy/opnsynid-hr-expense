# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=C8101
{
    "name": "HR Reimbursement - Documenso Signing Integration",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_reimbursement",
        "ssi_connector_documenso_signing",
        "web_tour",
    ],
    "data": [
        "views/assets.xml",
    ],
    "demo": [],
    "images": [],
}
