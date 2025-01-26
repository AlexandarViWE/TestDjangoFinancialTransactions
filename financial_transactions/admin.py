from django.contrib import admin

from .forms import TransactionAdminForm
from .models import Category, Status, Subcategory, Transaction, TransactionType
from .utils import is_ajax
from rangefilter.filters import DateRangeFilterBuilder


class FilterOnSearchAdminMixin:

    def get_search_results(self, request, queryset, search_term):
        if is_ajax(request):
            query = {}
            for field_filter in self.list_filter:
                value = request.GET.get(field_filter)
                if value == '':
                    field_filter = f"{field_filter}__isnull"
                    value = True
                query[field_filter] = value
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


class NameFieldListFilter(admin.SimpleListFilter):
    depends_on = "transaction_type__id__exact"

    model = None
    filtered_field = None
    filtered_field_type = int
    field_name = 'name'


    def lookups(self, request, model_admin):
        chained_field_value = request.GET.get(self.depends_on, None)
        if chained_field_value:
            chained_field_value = self.filtered_field_type(chained_field_value)
            queryset = self.model.objects.filter(
                **{self.filtered_field: chained_field_value}
            )
        else:
            queryset = self.model.objects.all()

        queryset = queryset.values(
            self.field_name
        ).values_list(self.field_name, flat=True).distinct()
        return [(item, str(item)) for item in queryset]


class CategoryListFilter(NameFieldListFilter):
    title = 'Category'
    parameter_name = 'category_name'

    model = Category
    filtered_field = 'transaction_type_id'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__category__name=self.value())
        return queryset.all()


class SubcategoryListFilter(NameFieldListFilter):
    title = 'Subcategory'
    parameter_name = 'subcategory_name'

    depends_on = 'category_name'
    filtered_field_type = str
    model = Subcategory
    filtered_field = 'category__name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__subcategory__name=self.value())
        return queryset.all()


class TransactionAdmin(admin.ModelAdmin):
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
