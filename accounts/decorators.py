from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Autorise uniquement les ADMIN
    """

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name='ADMIN').exists():

            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Accès réservé aux administrateurs."
        )

        return redirect('home')

    return wrapper


def agent_required(view_func):
    """
    Autorise uniquement les AGENT
    """

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name='AGENT').exists():

            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Accès réservé aux agents."
        )

        return redirect('home')

    return wrapper


def client_required(view_func):
    """
    Autorise uniquement les CLIENT
    """

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name='CLIENT').exists():

            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Accès réservé aux clients."
        )

        return redirect('home')

    return wrapper

def admin_or_agent_required(view_func):
    """
    Autorise ADMIN et AGENT
    """

    def wrapper(request, *args, **kwargs):

        if (
            request.user.groups.filter(name='ADMIN').exists()
            or
            request.user.groups.filter(name='AGENT').exists()
        ):

            return view_func(
                request,
                *args,
                **kwargs
            )

        messages.error(
            request,
            "Accès réservé aux gestionnaires."
        )

        return redirect('home')

    return wrapper