from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    """
    Client du système (digital ou walk-in)
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nom = models.CharField(max_length=100)

    email = models.EmailField(blank=True, null=True)

    telephone = models.CharField(max_length=20, blank=True, null=True)

    is_walk_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom