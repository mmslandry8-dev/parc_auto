from django import forms

from vehicles.models import Vehicle

from payments.models import Payment


class AgentSaleForm(forms.Form):

    """
    Formulaire vente terrain agent
    """

    # CLIENT
    username = forms.CharField(

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom client'
            }
        )

    )

    email = forms.EmailField(

        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email client'
            }
        )

    )

    password = forms.CharField(

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe'
            }
        )

    )

    # VEHICULE
    vehicle = forms.ModelChoiceField(

        queryset=Vehicle.objects.filter(
            statut='DISPONIBLE'
        ),

        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )

    )

    # METHODE PAIEMENT
    methode = forms.ChoiceField(

        choices=Payment.METHOD_CHOICES,

        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )

    )