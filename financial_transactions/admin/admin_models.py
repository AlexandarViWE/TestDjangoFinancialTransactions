from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from financial_transactions.admin.filters import (CategoryListFilter,
                                                  FilterOnSearchAdminMixin,
                                                  SubcategoryListFilter)
from financial_transactions.models import (Category, Status, Subcategory,
                                           Transaction, TransactionType)
from financial_transactions.forms import TransactionAdminForm

class TransactionTypeAdmin(admin.ModelAdmin):
    search_fields = ['name',]


class CategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['transaction_types',]
    search_fields = ['name',]


class SubcategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['category',]
    search_fields = ['name',]


class TransactionAdmin(admin.ModelAdmin):
    list_select_related = ["status", "transaction_type",
                           "category", "subcategory"]

    autocomplete_fields = ['subcategory', 'category', 'transaction_type']

    form = TransactionAdminForm
    fields = ['status', 'amount', 'transaction_type',
              'category', 'subcategory', 'description', 'created_at']

    list_display = fields

    list_filter = [
        ('created_at', DateRangeFilterBuilder(title="Date range")),
        'status',
        'transaction_type',
        CategoryListFilter,
        SubcategoryListFilter,
    ]

    class Media:
        js = ('financial_transactions/js/search.js', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Status)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
