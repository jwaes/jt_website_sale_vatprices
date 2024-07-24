from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

class WebsiteSaleVatinfoVariantController(WebsiteSaleVariantController):

    @http.route()
    def get_combination_info_website(self, *args, **kwargs):
        request.update_context(website_sale_vatinfo=True)
        return super().get_combination_info_website(*args, **kwargs)