/** @odoo-module **/

import VariantMixin from "@website_sale/js/variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToFragment } from "@web/core/utils/render";
import "@website_sale/js/website_sale";

// const originalOnChangeCombination = VariantMixin._onChangeCombination;

VariantMixin._onChangeCombinationVAT = function (ev, $parent, combination) {
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


    const $vatExcl = $parent.find(".exclvat .oe_currency_value")
    // console.log('changing')
    // console.log($vatExcl)
    // console.log(combination)

    if ($vatExcl) {
        $vatExcl.text(combination.total_excluded)
    }

    const $appliedTax = $parent.find("#applied_tax")
    if ($appliedTax){
        $appliedTax.text(combination.applied_tax)
    }

    if (!combination.hastax) {
        $('div.vatextrainfo').hide();
    }

    // originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};


publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the vat to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationVAT.apply(this, arguments);
    },
});

export default VariantMixin;