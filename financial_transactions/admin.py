from django.contrib import admin

from .forms import TransactionAdminForm
from .models import Category, Status, Subcategory, Transaction, TransactionType
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
    form = TransactionAdminForm
    autocomplete_fields = ['subcategory', 'transaction_type']

    fields = ['status', 'amount', 'transaction_type',
              'category', 'subcategory', 'description', 'created_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Status)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
