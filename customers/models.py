from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    """
    Client global (web + agence)
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nom = models.CharField(
        max_length=100
    )

    telephone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    adresse = models.TextField(
        null=True,
        blank=True
    )

    is_blocked = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.nom