from django import forms
from .models import Rental


class RentalForm(forms.ModelForm):

    class Meta:

        model = Rental

        fields = [

            'date_debut',
            'date_fin'

        ]

        widgets = {

            'date_debut': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'date_fin': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

        }