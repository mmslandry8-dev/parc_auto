from django import forms
from django.core.exceptions import ValidationError

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

    def clean(self):

        """
        Validation intelligente des dates
        """

        cleaned_data = super().clean()

        date_debut = cleaned_data.get('date_debut')

        date_fin = cleaned_data.get('date_fin')

        # Vérification présence dates
        if not date_debut or not date_fin:

            return cleaned_data

        # DATE FIN < DATE DEBUT
        if date_fin < date_debut:

            raise ValidationError(

                "La date de fin ne peut pas être avant la date de début."

            )

        return cleaned_data