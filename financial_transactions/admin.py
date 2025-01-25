from django.contrib import admin

from .forms import TransactionForm
from .models import Category, Status, Transaction, TransactionType
from .utils import is_ajax


class FilterOnSearchAdminMixin:

    def get_search_results(self, request, queryset, search_term):
        if is_ajax(request):
            query = {filter: request.GET.get(filter)
                     for filter in self.list_filter}
            queryset = queryset.filter(**query)
        return super().get_search_results(request, queryset, search_term)


class TransactionTypeAdmin(admin.ModelAdmin):
    search_fields = ['name',]


class CategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['transaction_type',]
    search_fields = ['name',]


class SubcategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['category',]
    search_fields = ['name',]


class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm
    autocomplete_fields = ['category', 'transaction_type']
    chain_select = {
        "transaction_type": "category",
    }

    # class Media:
    #     js = ('autocompletes/js/search.js', )

    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #     field = super().formfield_for_dbfield(db_field, request, **kwargs)
    #     if db_field.name in self.chain_select:
    #         field.widget.attrs.update({
    #             'onchange': 'search(this);',
    #             'data-name': self.chain_select[db_field.name],
    #         })
    #     return field


admin.site.register(Category, CategoryAdmin)
admin.site.register(Status)
# admin.site.register(Subcategory)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
