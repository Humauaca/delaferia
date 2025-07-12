from django import forms
from . import models

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['category', 'name', 'description', 'price', 'image', 'quantity_in_stock']
        labels = {
            'category': 'Categoria',
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'image': 'Imagen',
            'quantity_in_stock': 'Cantidad en Stock'
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'quantity_in_stock': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name', 'description', 'price', 'image', 'quantity_in_stock']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'image': 'Imagen',
            'quantity_in_stock': 'Cantidad en Stock'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'quantity_in_stock': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
            })
        }