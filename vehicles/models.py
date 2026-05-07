from django.db import models


class Vehicle(models.Model):

    """
    Modèle représentant un véhicule
    """

    STATUS_CHOICES = [

        ('DISPONIBLE', 'Disponible'),

        ('LOUE', 'Loué'),

        ('MAINTENANCE', 'Maintenance'),

        ('VENDU', 'Vendu'),

    ]

    TYPE_CHOICES = [

        ('SUV', 'SUV'),

        ('BERLINE', 'Berline'),

        ('4X4', '4X4'),

        ('SPORT', 'Sport'),

        ('UTILITAIRE', 'Utilitaire'),

    ]

    # INFORMATIONS
    marque = models.CharField(max_length=100)

    modele = models.CharField(max_length=100)

    annee = models.PositiveIntegerField()

    immatriculation = models.CharField(
        max_length=100,
        unique=True
    )

    type_vehicule = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    # PRIX
    prix_location = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    prix_vente = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # STATUT
    statut = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='DISPONIBLE'
    )

    # IMAGE
    image = models.ImageField(
        upload_to='vehicles/'
    )

    # DESCRIPTION
    description = models.TextField()

    # DATES
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.marque} {self.modele}"