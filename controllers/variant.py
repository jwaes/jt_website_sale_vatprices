import logging
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.tools.misc import get_lang

_logger = logging.getLogger(__name__)

class WebsiteSaleNowVatVariantController(WebsiteSaleVariantController):

    @http.route()
    def get_combination_info_website(self, *args, **kwargs):
        request.update_context(website_sale_vatinfo=True)
        _logger.debug('ENTERING WebsiteSaleNowVatVariantController')
        return super().get_combination_info_website(*args, **kwargs)