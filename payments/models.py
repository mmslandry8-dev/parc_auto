from django.db import models

from rentals.models import Rental


class Payment(models.Model):

    """
    Modèle représentant un paiement
    """

    METHOD_CHOICES = [

        ('MTN', 'MTN Mobile Money'),

        ('ORANGE', 'Orange Money'),

        ('ESPECES', 'Espèces'),

    ]

    STATUS_CHOICES = [

        ('EN_ATTENTE', 'En attente'),

        ('PAYE', 'Payé'),

    ]

    # LOCATION
    rental = models.OneToOneField(
        Rental,
        on_delete=models.CASCADE
    )

    # MONTANT
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # METHODE
    methode = models.CharField(
        max_length=50,
        choices=METHOD_CHOICES
    )

    # STATUT
    statut = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='EN_ATTENTE'
    )

    # DATE
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.rental.client.username} - {self.montant}"