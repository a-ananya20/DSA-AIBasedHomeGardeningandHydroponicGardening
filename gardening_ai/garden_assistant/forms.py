from django import forms

from django import forms
from .models import HarvestItem

class HarvestItemForm(forms.ModelForm):
    class Meta:
        model = HarvestItem
        fields = '__all__'
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'seller_name': forms.TextInput(attrs={'class': 'form-control'}),
            'seller_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
