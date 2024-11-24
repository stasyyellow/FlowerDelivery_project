from django import forms
from .models import Order
from catalog.models import Product

class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Товар",
        empty_label="Выберите товар",
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Количество",
        widget=forms.NumberInput(attrs={'placeholder': 'Введите количество'}),
    )
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите адрес доставки'}),
        label="Адрес доставки"
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Дополнительные комментарии'}),
        label="Комментарий",
    )

    class Meta:
        model = Order
        fields = ['product', 'quantity', 'delivery_address', 'comment']  # Поля для заполнения
