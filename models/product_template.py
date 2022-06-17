import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        self.ensure_one()

        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if self.env.context.get('website_id'):
            context = dict(self.env.context, ** {
                'quantity': self.env.context.get('quantity', add_qty),
                'pricelist': pricelist and pricelist.id
            })

            product = (self.env['product.product'].browse(combination_info['product_id']) or self).with_context(context)
            partner = self.env.user.partner_id
            company_id = current_website.company_id

            tax_display = self.user_has_groups('account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
            fpos = self.env['account.fiscal.position'].sudo().get_fiscal_position(partner.id)
            product_taxes = product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id)
            taxes = fpos.map_tax(product_taxes)

            # The list_price is always the price of one.
            quantity_1 = 1
            list_price = product.price_compute('list_price')[product.id]
            price = product.price if pricelist else list_price
            all_prices = taxes.compute_all(price, pricelist.currency_id, quantity_1, product, partner)

            total_excluded = all_prices['total_excluded']
            total_included = all_prices['total_included']

            applied_tax = ""
            if all_prices['taxes'] and all_prices['taxes'][0]:
                applied_tax = all_prices['taxes'][0]['name']

            hastax = False
            if product.taxes_id:
                hastax = True            

            combination_info.update({
                'hastax': hastax,
                'tax': product.taxes_id.display_name,
                'total_excluded': total_excluded,
                'total_included': total_included,
                'tax_display': tax_display,
                'applied_tax': applied_tax,
            })

        return combination_info