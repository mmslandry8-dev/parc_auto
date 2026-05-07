from django.db import models
from django.contrib.auth.models import User

from vehicles.models import Vehicle


class Rental(models.Model):

    """
    Modèle représentant une location
    """

    STATUS_CHOICES = [

        ('EN_ATTENTE', 'En attente'),

        ('VALIDEE', 'Validée'),

        ('REFUSEE', 'Refusée'),

        ('TERMINEE', 'Terminée'),

    ]

    # CLIENT
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # VEHICULE
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    # DATES
    date_debut = models.DateField()

    date_fin = models.DateField()

    # PRIX TOTAL
    prix_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # STATUT
    statut = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='EN_ATTENTE'
    )

    # DATES SYSTEME
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.client.username} - {self.vehicle}"