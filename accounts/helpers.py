def get_user_role(user):
    """
    Retourne le rôle principal de l'utilisateur
    """

    if not user.is_authenticated:
        return None

    group = user.groups.first()

    if group:
        return group.name

    return None