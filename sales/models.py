from django.db import models
from django.contrib.auth.models import User

from vehicles.models import Vehicle


class Sale(models.Model):

    """
    Gestion des ventes de véhicules
    """

    STATUS_CHOICES = [

        ('EN_ATTENTE', 'En attente'),

        ('VALIDEE', 'Validée'),

        ('PAYEE', 'Payée'),

        ('REFUSEE', 'Refusée'),

    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date_demande = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EN_ATTENTE'
    )

    prix_vente = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):

        return f"{self.vehicle} - {self.client}"