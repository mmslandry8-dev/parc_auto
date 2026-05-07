from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):

    class Meta:

        model = Vehicle

        fields = '__all__'

        widgets = {

            'marque': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'modele': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'annee': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'immatriculation': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'type_vehicule': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'prix_location': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'prix_vente': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'statut': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

        }