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
    
class AgentRentalForm(forms.Form):

    """
    Formulaire location terrain agent
    """

    # CLIENT
    username = forms.CharField(

        max_length=150,

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom du client'
            }
        )
    )

    email = forms.EmailField(

        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )

    password = forms.CharField(

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe client'
            }
        )
    )

    # VEHICULE
    vehicle = forms.ModelChoiceField(

        queryset=None,

        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    # DATES
    date_debut = forms.DateField(

        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    date_fin = forms.DateField(

        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        from vehicles.models import Vehicle

        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            statut='DISPONIBLE'
        )

    def clean(self):

        cleaned_data = super().clean()

        date_debut = cleaned_data.get('date_debut')

        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin:

            if date_fin < date_debut:

                raise ValidationError(
                    "La date de fin doit être après la date de début."
                )

        return cleaned_data