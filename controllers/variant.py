from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

class WebsiteSaleVatinfoVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        kw['context'] = kw.get('context', {})
        kw['context'].update(website_sale_vatinfo=True)
        combination = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)

        # pp_view = request.env['ir.ui.view']._render_template('jt_product_properties_website.website_sale_product_properties', values={
        #     'product_variant': request.env['product.product'].browse(combination['product_id']),
        # })

        # combination['product_properties'] = pp_view

        return combination