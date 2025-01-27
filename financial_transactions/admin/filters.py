from django.contrib import admin

from financial_transactions.models import Category, Subcategory
from django.contrib.admin.utils import get_fields_from_path
from django.db.models import ForeignKey


def is_ajax(request) -> bool:
    """True, если запрос был отправлен через ajax."""
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class FilterOnSearchAdminMixin:
    """Фильтрация результатов поиска при автодополнении. 

    Использовать совместно с `django.contrib.admin.ModelAdmin`.
    """

    def get_search_results(self, request, queryset, search_term):
        """"""
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


class NameFieldListFilter(admin.SimpleListFilter):
    """Фильтр для поиска по текстовому полю связанной 
    модели в зависимости от другого фильтра.
    """
    # Связанное текстовое поле с model_admin.
    field = None

    # Название параметра запроса, значение которого влияет на варианты выбора.
    depends_on = None

    # Описание того, как отфильтровать варианты выбора.
    # TODO: Наверное есть способ объединить эти 2 поля в одно.
    filtered_field = None
    filtered_field_type = int

    def lookups(self, request, model_admin):
        # Получаем поле модели для фильтрации.
        fields = get_fields_from_path(model_admin.model, self.field)
        foreign_field = next(
            (i for i in reversed(fields) if isinstance(i, ForeignKey)),
            None
        )
        if not foreign_field:
            print(self)
            raise ValueError  # FIXME: Дописать ошибку.
        related_model = foreign_field.related_model

        queryset = related_model.objects.all()

        # Если есть фильтр от которого зависим, то фильтруем варианты выбора.
        chained_field_value = request.GET.get(self.depends_on, None)
        if chained_field_value:
            try:
                chained_field_value = self.filtered_field_type(
                    chained_field_value)
                queryset = queryset.filter(
                    **{self.filtered_field: chained_field_value}
                )
            except ValueError:
                # TODO: Значение фильтра может быть списком.
                pass

        # Возвращаем список строк для выбора.
        field_name = fields[-1].name
        queryset = queryset.values(field_name).values_list(
            field_name, flat=True).distinct()
        return [(item, str(item)) for item in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.field: self.value()})
        return queryset.all()


class CategoryListFilter(NameFieldListFilter):
    """Фильтр для категории."""
    title = 'Category'
    parameter_name = 'category_name'

    field = 'subcategory__category__name'
    
    depends_on = "transaction_type__id__exact"
    filtered_field = 'transaction_type_id'


class SubcategoryListFilter(NameFieldListFilter):
    """Фильтр для категории."""

    title = 'Subcategory'
    parameter_name = 'subcategory_name'

    field = 'subcategory__name'

    depends_on = 'category_name'
    filtered_field = 'category__name'
    filtered_field_type = str
