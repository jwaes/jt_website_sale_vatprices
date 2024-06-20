/** @odoo-module **/

import VariantMixin from "@website_sale/js/variant_mixin";
import { renderToFragment } from "@web/core/utils/render";
import "@website_sale/js/website_sale";
import { markup } from "@odoo/owl";

const originalOnChangeCombination = VariantMixin._onChangeCombination;




VariantMixin._onChangeCombinationVAT = function (ev, $parent, combination) {

    const $pricePerUom = $parent.find(".vatextrainfo .oe_currency_value");

    if ($pricePerUom) {
        if (combination.is_combination_possible !== false && combination.total_excluded != 0) {
            $pricePerUom.parents(".o_base_unit_price_wrapper").removeClass("d-none");
            $pricePerUom.text(this._priceToStr(combination.total_excluded));
            $parent.find(".oe_custom_base_unit:first").text(combination.base_unit_name);
        } else {
            $pricePerUom.parents(".o_base_unit_price_wrapper").addClass("d-none");
        }
    }

    let product_id = 0;
    // needed for list view of variants
    if ($parent.find('input.product_id:checked').length) {
        product_id = $parent.find('input.product_id:checked').val();
    } else {
        product_id = $parent.find('.product_id').val();
    }
    const isMainProduct = combination.product_id &&
        ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
        combination.product_id === parseInt(product_id);

    if (!this.isWebsite || !isMainProduct) {
        return;
    }
    $('span.vatsuffix').html(renderToFragment(
        'jt_website_sale_vatprices.vatsuffix',
        combination
    ));
    if (!combination.hastax) {
        $('div.vatextrainfo').hide();
    }

    originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};

export default VariantMixin;