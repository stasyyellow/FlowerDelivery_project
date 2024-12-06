from django import forms
from .models import Order
from catalog.models import Product

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите адрес доставки'}),
        label="Адрес доставки"
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Дополнительные комментарии'}),
        label="Комментарий",
    )
    add_card = forms.BooleanField(
        required=False,
        label="Добавить открытку",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    card_text = forms.CharField(
        required=False,
        label="Текст открытки",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите текст открытки...'}),
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'comment', 'add_card', 'card_text']

