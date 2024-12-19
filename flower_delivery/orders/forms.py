from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите адрес доставки'}),
        label="Адрес доставки"
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
        fields = ['delivery_address', 'add_card', 'card_text']

    def clean(self):
        cleaned_data = super().clean()
        add_card = cleaned_data.get('add_card')
        card_text = cleaned_data.get('card_text', '')

        if not add_card:
            cleaned_data['card_text'] = ''
        return cleaned_data



