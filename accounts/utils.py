from django.contrib.auth.models import Group
from .constants import ROLE_ADMIN, ROLE_AGENT, ROLE_CLIENT


def assign_user_role(user, role):
    """
    Assigne un rôle utilisateur et synchronise les groupes Django
    """

    # sécurité : uniquement rôles valides
    allowed_roles = [ROLE_ADMIN, ROLE_AGENT, ROLE_CLIENT]

    if role not in allowed_roles:
        role = ROLE_CLIENT

    # reset groupes
    user.groups.clear()

    # récupérer ou créer groupe
    group, created = Group.objects.get_or_create(name=role)

    # assignation
    user.groups.add(group)

    user.save()