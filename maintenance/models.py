from django.db import models

from vehicles.models import Vehicle


class Maintenance(models.Model):

    """
    Gestion des pannes et réparations
    """

    STATUS_CHOICES = [

        ('EN_COURS', 'En cours'),

        ('TERMINEE', 'Terminée'),

    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    cout_reparation = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    date_signalement = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EN_COURS'
    )

    def __str__(self):

        return f"{self.vehicle} - {self.statut}"