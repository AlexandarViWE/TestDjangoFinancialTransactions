'use strict'

function search(obj) {
    if (obj.form.elements[obj.dataset.relatedfieldname]) {
        patch_url(obj.form.elements[obj.dataset.relatedfieldname], { [obj.dataset.searchparamname]: obj.value })
    };
}

function patch_url(item, search) {
    django.jQuery.each(Object.keys(item), function (idx, key) {
        if (item[key].select2) {
            return patch_data(search, item[key].select2.dataAdapter.ajaxOptions, item[key].select2.dataAdapter.ajaxOptions.data)
        }
    })
}

function patch_data(search, ajaxOptions, baseData) {
    ajaxOptions.data = function (params) {
        return { ...baseData(params), ...search }
    }
}

window.addEventListener("load", function () {
    django.jQuery("select[name=category]")
        .attr("onchange", "search(this);")
        .attr("data-relatedFieldName", "subcategory")
        .attr("data-searchParamName", "category")
        .trigger("change");

    django.jQuery("select[name=transaction_type]")
        .attr("onchange", "search(this);")
        .attr("data-relatedFieldName", "category")
        .attr("data-searchParamName", "transaction_types")
        .trigger("change");
});
