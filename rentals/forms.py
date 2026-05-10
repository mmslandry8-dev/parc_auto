from django import forms
from django.core.exceptions import ValidationError

from .models import Rental

from django.contrib.auth.models import User


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

    # =====================================
    # CLIENT EXISTANT
    # =====================================

    existing_client = forms.ModelChoiceField(

        queryset=User.objects.filter(
            groups__name='CLIENT'
        ),

        required=False,

        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    # =====================================
    # NOUVEAU CLIENT
    # =====================================

    username = forms.CharField(

        required=False,

        max_length=150,

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom du client'
            }
        )
    )

    email = forms.EmailField(

        required=False,

        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )

    password = forms.CharField(

        required=False,

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe'
            }
        )
    )

    # =====================================
    # VEHICULE
    # =====================================

    vehicle = forms.ModelChoiceField(

        queryset=None,

        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    # =====================================
    # DATES
    # =====================================

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

        existing_client = cleaned_data.get(
            'existing_client'
        )

        username = cleaned_data.get('username')

        email = cleaned_data.get('email')

        password = cleaned_data.get('password')

        date_debut = cleaned_data.get('date_debut')

        date_fin = cleaned_data.get('date_fin')

        # =====================================
        # CLIENT VALIDATION
        # =====================================

        if not existing_client:

            if not username:

                raise ValidationError(
                    "Nom client obligatoire."
                )

            if not email:

                raise ValidationError(
                    "Email obligatoire."
                )

            if not password:

                raise ValidationError(
                    "Mot de passe obligatoire."
                )

        # =====================================
        # DATES VALIDATION
        # =====================================

        if date_debut and date_fin:

            if date_fin < date_debut:

                raise ValidationError(
                    "La date de fin doit être après la date de début."
                )

        return cleaned_data