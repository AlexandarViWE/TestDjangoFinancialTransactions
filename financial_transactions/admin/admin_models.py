from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from financial_transactions.admin.filters import (CategoryListFilter,
                                                  FilterOnSearchAdminMixin,
                                                  SubcategoryListFilter)
from financial_transactions.forms import TransactionAdminForm
from financial_transactions.models import (Category, Status, Subcategory,
                                           Transaction, TransactionType)


class TransactionTypeAdmin(admin.ModelAdmin):
    search_fields = ['name',]


class CategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['transaction_type',]
    search_fields = ['name',]


class SubcategoryAdmin(FilterOnSearchAdminMixin, admin.ModelAdmin):
    list_filter = ['category',]
    search_fields = ['name',]


class TransactionAdmin(admin.ModelAdmin):
    list_select_related = ["status", "transaction_type",
                           "subcategory", "subcategory__category"]

    form = TransactionAdminForm

    autocomplete_fields = ['subcategory', 'transaction_type']

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Status)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
