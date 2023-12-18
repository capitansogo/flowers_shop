from django import forms
from django.forms import inlineformset_factory

from .models import *


class SuppliesForm(forms.ModelForm):
    class Meta:
        model = Supplies
        fields = ['delivery_date', 'filial']


