from django.contrib.auth.models import Group


def assign_user_role(user, role):
    """
    Assigne un rôle utilisateur
    et met automatiquement à jour les groupes.
    """

    # Supprimer anciens groupes
    user.groups.clear()

    # Récupérer ou créer groupe
    group, created = Group.objects.get_or_create(
        name=role
    )

    # Ajouter utilisateur au groupe
    user.groups.add(group)

    # Sauvegarder
    user.save()