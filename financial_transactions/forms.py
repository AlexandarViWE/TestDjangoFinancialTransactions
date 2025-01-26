from django import forms
from django.contrib import admin
from django.contrib.admin import widgets

from financial_transactions.models import (Category, Subcategory, Transaction,
                                           TransactionType)


class TransactionAdminForm(forms.ModelForm):
    """Форма для создания/редактирования денежной транзакции.
    
    Для работы в html должны быть включены javascript из django admin.   
    """

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=widgets.AutocompleteSelect(
            Subcategory.category.field,
            admin.site,
            attrs={
                'onchange': 'search(this);',
                'data-name': 'subcategory',
            })
    )

    class Media:
        js = ('financial_transactions/js/search.js', )

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'transaction_type': forms.Select(attrs={
                'onchange': 'search(this);',
                'data-name': 'category',
            }),
        }

    def clean(self):
        transaction_type: TransactionType = self.cleaned_data['transaction_type']
        category: Category = self.cleaned_data['category']
        subcategory: Category = self.cleaned_data['subcategory']
        if category.transaction_type_id != transaction_type.id:
            raise forms.ValidationError(
                "Category must match the transaction type!")
        if subcategory.category_id != category.id:
            raise forms.ValidationError(
                "Subcategory must match the category!")
        return super().clean()

    # Django admin игнорирует это.
    # field_order  = (
    #     'status', 'amount', 'transaction_type', 'category', 'subcategory'
    # )
