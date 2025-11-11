from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un utente demo per testing'

    def handle(self, *args, **options):
        username = 'demo'
        email = 'demo@example.com'
        password = 'demo1234'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Utente "{username}" già esistente - skip')
            )
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Demo',
            last_name='User'
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Utente demo creato con successo!\n'
                f'\n📝 Credenziali di accesso:'
                f'\n   Username: {username}'
                f'\n   Password: {password}'
                f'\n   Email: {email}'
                f'\n\n🌐 Apri http://localhost:3000 e accedi con queste credenziali\n'
            )
        )
