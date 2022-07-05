odoo.define('jt_website_sale_vatprices.VariantMixin', function (require) {
    'use strict';
    
    const {Markup} = require('web.utils');
    var VariantMixin = require('sale.VariantMixin');
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var QWeb = core.qweb;
    
    const loadXml = async () => {
        return ajax.loadXML('/jt_website_sale_vatprices/static/src/xml/website_sale_vatprices.xml', QWeb);
    };
    
    require('website_sale.website_sale');
    
    /**
     * Addition to the variant_mixin._onChangeCombination
     *
     * This will prevent the user from selecting a quantity that is not available in the
     * stock for that product.
     *
     * It will also display various info/warning messages regarding the select product's stock.
     *
     * This behavior is only applied for the web shop (and not on the SO form)
     * and only for the main product.
     *
     * @param {MouseEvent} ev
     * @param {$.Element} $parent
     * @param {Array} combination
     */
    VariantMixin._onChangeCombinationVAT = function (ev, $parent, combination) {

        const $pricePerUom = $parent.find(".vatextrainfo .oe_currency_value");
        console.log("here")
        console.log($pricePerUom)
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
        
        console.log('vatinfo ready')

        loadXml().then(function (result) {
            const $vatsuffix = $(QWeb.render(
                'jt_website_sale_vatprices.vatsuffix',
                combination
            ));
            $('span.vatsuffix').html($vatsuffix);
            // const $exclvat = $(QWeb.render(
            //     'jt_website_sale_vatprices.exclvat',
            //     combination
            // ));
            // $('span.exclvat').html($exclvat);
            if(!combination.hastax){
                $('div.vatextrainfo').hide();
            }
        });
    };
    
    publicWidget.registry.WebsiteSale.include({
        /**
         * Adds the stock checking to the regular _onChangeCombination method
         * @override
         */
        _onChangeCombination: function () {
            this._super.apply(this, arguments);
            VariantMixin._onChangeCombinationVAT.apply(this, arguments);
        },

    });
    
    return VariantMixin;
    
    });