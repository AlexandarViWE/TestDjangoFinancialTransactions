from django import forms

from financial_transactions.models import (Category, Subcategory, Transaction,
                                           TransactionType)


class TransactionAdminForm(forms.ModelForm):
    """Форма для создания/редактирования денежной транзакции."""

    class Meta:
        model = Transaction
        fields = '__all__'

    def clean(self):
        transaction_type: TransactionType = self.cleaned_data['transaction_type']
        category: Category = self.cleaned_data['category']
        subcategory: Subcategory = self.cleaned_data['subcategory']
        if not category.transaction_types.contains(transaction_type):
            raise forms.ValidationError(
                "Category must match the transaction type!")
        if subcategory.category_id != category.id:
            raise forms.ValidationError(
                "Subcategory must match the category!")
        return super().clean()
