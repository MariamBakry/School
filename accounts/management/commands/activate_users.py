# your_project/your_app/management/commands/activate_users.py
from django.core.management.base import BaseCommand
from ...models import CustomUser

class Command(BaseCommand):
    help = 'Activates specified user(s)'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str, help='List of usernames to activate')

    def handle(self, *args, **kwargs):
        usernames = kwargs['usernames']
        for username in usernames:
            try:
                user = CustomUser.objects.get(username=username)
                user.is_active = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{username}" has been activated'))
            except CustomUser.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'User "{username}" does not exist'))
