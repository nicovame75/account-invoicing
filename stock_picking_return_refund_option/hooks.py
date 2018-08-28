# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, SUPERUSER_ID, tools


def _install_module_hook(cr, registry):
    if not tools.config.options.get('without_demo', False):
        env = api.Environment(cr, SUPERUSER_ID, {})
        modules = env['ir.module.module'].search([
            ('name', 'in', ['purchase', 'sale_stock']),
            ('state', '!=', 'installed'),
        ]).write({'to_install': True})
        modules.button_immediate_install()
