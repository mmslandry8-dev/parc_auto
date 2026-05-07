from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = [

            'methode'

        ]

        widgets = {

            'methode': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            )

        }