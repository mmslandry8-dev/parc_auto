from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_CLIENT


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for role in [ROLE_ADMIN, ROLE_AGENT, ROLE_CLIENT]:
            Group.objects.get_or_create(name=role)

        self.stdout.write(self.style.SUCCESS("Rôles créés avec succès"))