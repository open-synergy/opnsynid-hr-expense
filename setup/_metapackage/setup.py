import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-hr-expense",
    description="Meta package for open-synergy-opnsynid-hr-expense Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_employee_business_trip',
        'odoo14-addon-ssi_hr_cash_advance',
        'odoo14-addon-ssi_hr_expense',
        'odoo14-addon-ssi_hr_expense_account',
        'odoo14-addon-ssi_hr_expense_account_cash_advance',
        'odoo14-addon-ssi_hr_expense_account_reimbursement',
        'odoo14-addon-ssi_hr_reimbursement',
        'odoo14-addon-ssi_hr_reimbursement_work_log',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
