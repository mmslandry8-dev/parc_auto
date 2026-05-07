from django import forms
from .models import Maintenance


class MaintenanceForm(forms.ModelForm):

    class Meta:

        model = Maintenance

        fields = [

            'description',
            'cout_reparation'

        ]

        widgets = {

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'cout_reparation': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }