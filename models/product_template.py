import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, parent_combination=False, only_template=False):


        current_website = self.env['website'].get_current_website().with_context(self.env.context)
        pricelist = current_website._get_current_pricelist()
        _logger.info("website pricelist is " + pricelist.name)

        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, 
            product_id=product_id, 
            add_qty=add_qty, 
            parent_combination=parent_combination,
            only_template=only_template)



        if self.env.context.get('website_id'):
            context = dict(self.env.context, ** {
                'quantity': self.env.context.get('quantity', add_qty),
                'pricelist': pricelist.id
            })

            product = (self.env['product.product'].browse(combination_info['product_id']) or self).with_context(context)
            partner = self.env.user.partner_id
            company_id = current_website.company_id

            tax_display = self.user_has_groups('account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
            _logger.info('tax_display  ' + tax_display)
            _logger.info('partner '+ partner.name)
            fpos = self.env['account.fiscal.position'].sudo()._get_fiscal_position(partner)
            if fpos:
                _logger.info('fiscal position ' + fpos.name)
            else:
                _logger.info('fiscal position: false')
            product_taxes = product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id)
            _logger.info('product_taxes ' + product_taxes.name)
            taxes = fpos.map_tax(product_taxes)
            _logger.info('taxes ' + taxes.name)

            # The list_price is always the price of one.
            quantity_1 = 1.0
            # list_price = product._price_compute('list_price')[product.id]
            product_price_unit = product.with_company(company_id).lst_price
            # price = product.price if pricelist else list_price
            all_prices = taxes.compute_all(product_price_unit, currency=pricelist.currency_id, quantity=quantity_1, product=product, partner=partner)

            price_untaxed = taxes.compute_all(
                                lst_price,
                                currency,
                                1,
                                handle_price_include=True,
                            )['total_excluded']
            price_taxed = taxes.compute_all(
                                price_untaxed,
                                currency,
                                1,
                                handle_price_include=False,
                            )['total_included']                            


            total_excluded = all_prices['total_excluded']
            total_included = all_prices['total_included']

            _logger.info('total_excluded ' + str(total_excluded))
            _logger.info('total_included ' + str(total_included))

            total_excluded = price_untaxed
            total_included = price_taxed    

            _logger.info('total_excluded ' + str(total_excluded))
            _logger.info('total_included ' + str(total_included))

            applied_tax = ""
            if all_prices['taxes'] and all_prices['taxes'][0]:
                applied_tax = all_prices['taxes'][0]['name']

            hastax = False
            if product.taxes_id:
                hastax = True     
                _logger.info('hastax !')                  

            combination_info.update({
                'hastax': hastax,
                'tax': product.taxes_id.display_name,
                'total_excluded': total_excluded,
                'total_included': total_included,
                'tax_display': tax_display,
                'applied_tax': applied_tax,
            })

        return combination_info