from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

class WebsiteSaleVatinfoVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        kw['context'] = kw.get('context', {})
        kw['context'].update(website_sale_vatinfo=True)
        combination = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)

        return combination