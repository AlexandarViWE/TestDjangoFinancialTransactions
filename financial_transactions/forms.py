from django import forms

from financial_transactions.models import (Category, Subcategory, Transaction,
                                           TransactionType)


class TransactionForm(forms.ModelForm):

    # subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all())

    class Media:
        js = ('autocompletes/js/search.js', )

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'transaction_type': forms.Select(attrs={
                'onchange': 'search(this);',
                'data-name': 'category',
            }),
            # 'category': forms.Select(attrs={
            #     'onchange': 'search(this);',
            #     'data-name': 'subcategory',
            # }),
        }

    def clean(self):
        transaction_type: TransactionType = self.cleaned_data['transaction_type']
        category: Category = self.cleaned_data['category']
        # subcategory: Category = self.cleaned_data['subcategory']

        if category.transaction_type_id != transaction_type.id:
            raise forms.ValidationError(
                "Category must match the transaction type!")
            
        # if subcategory.category_id != category.id:
        #     raise forms.ValidationError(
        #         "Subcategory must match the category!")

        return super().clean()
