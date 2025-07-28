from django import forms
from . import models

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['quantity_to_buy', 'price_per_unit_at_purchase', 'total']
        field_order = [ 'price_per_unit_at_purchase', 'quantity_to_buy', 'total']
        labels = {
            'price_per_unit_at_purchase': 'Precio Unitario',
            'quantity_to_buy': 'Cantidad',
            'total': 'Total a Pagar'
        }

        widgets = {
            'price_per_unit_at_purchase': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'quantity_to_buy': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'total': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            })
        }

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)

        if item:
            self.fields['price_per_unit_at_purchase'].initial = item.price

        self.fields['price_per_unit_at_purchase'].disabled = True
        self.fields['total'].disabled = True
    

    

class ShippingForm(forms.ModelForm):
    class Meta:
        model = models.ShippingInfo
        fields = ['address', 'city', 'postal_code']
        labels = {
            'address': 'Direccion',
            'city': 'Ciudad',
            'postal_code': 'Codigo Postal'
        }

        widgets = {
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'city': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'postal_code': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            })
        }

class PaymentForm(forms.ModelForm):
    card_num = forms.CharField(label='Numero de Tarjeta',
                               widget=forms.NumberInput(attrs={'class': INPUT_CLASSES}))
    
    security_code = forms.CharField(label="Codigo de Seguridad",
                                    widget=forms.NumberInput(attrs={'class': INPUT_CLASSES}))

    expiration_month = forms.CharField(label='Mes de Vencimiento',
                               widget=forms.NumberInput(attrs={'class': INPUT_CLASSES}))
    
    expiration_year = forms.CharField(label="Ano de Vencimiento",
                                    widget=forms.NumberInput(attrs={'class': INPUT_CLASSES}))
    class Meta:
        model = models.Payment
        fields = ['provider', 'payment_method']
        field_order = ['provider', 'payment_method', 'card_num', 'expiration_month', 'expiration_year', 'security_code']
        labels = {
            'provider': 'Proveedor',
            'payment_method': 'Tarjeta',
        }

        widgets = {
            'provider': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'payment_method': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }

