from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from channels.models import SocialAccount
from messages.models import Message
from sentiment.models import SentimentAnalysis
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea dati demo per testing (utente + messaggi + sentiment)'

    def handle(self, *args, **options):
        # Crea utente demo
        username = 'demo'
        email = 'demo@example.com'
        password = 'demo1234'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Utente demo creato: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Utente demo già esistente: {username}'))

        # Crea canali social demo
        platforms = ['facebook', 'instagram']
        for platform in platforms:
            channel, created = SocialAccount.objects.get_or_create(
                user=user,
                platform=platform,
                platform_user_id=f'demo_{platform}_123',
                defaults={
                    'platform_username': f'Demo {platform.title()}',
                    'access_token': 'demo_token',
                    'status': 'active',
                    'profile_data': {
                        'name': f'Demo {platform.title()}',
                        'id': f'demo_{platform}_123'
                    },
                    'last_sync_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Canale {platform} creato'))

                # Crea messaggi demo per questo canale
                self._create_demo_messages(channel)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{"="*60}'
                f'\n✅ Dati demo creati con successo!'
                f'\n{"="*60}'
                f'\n\n📝 Credenziali di accesso:'
                f'\n   Username: {username}'
                f'\n   Password: {password}'
                f'\n   Email: {email}'
                f'\n\n🌐 Apri http://localhost:3000 e accedi con queste credenziali'
                f'\n\n📊 Dati disponibili:'
                f'\n   - 2 canali social connessi (Facebook, Instagram)'
                f'\n   - Messaggi di esempio con sentiment analizzato'
                f'\n   - Statistiche nella dashboard'
                f'\n{"="*60}\n'
            )
        )

    def _create_demo_messages(self, channel):
        """Crea messaggi demo con sentiment vario"""

        messages_data = [
            # Messaggi positivi
            {
                'text': 'Adoro il vostro prodotto! Fantastico servizio clienti! 😍',
                'sender': 'Maria Rossi',
                'type': 'comment',
                'sentiment': 'positive'
            },
            {
                'text': 'Esperienza eccellente, lo consiglio a tutti! Continuate così!',
                'sender': 'Luca Bianchi',
                'type': 'direct_message',
                'sentiment': 'positive'
            },
            {
                'text': 'Finalmente un servizio che funziona davvero! Molto soddisfatto.',
                'sender': 'Anna Verdi',
                'type': 'comment',
                'sentiment': 'positive'
            },
            # Messaggi negativi
            {
                'text': 'Servizio pessimo, non risponde nessuno. Molto deluso.',
                'sender': 'Paolo Neri',
                'type': 'direct_message',
                'sentiment': 'negative'
            },
            {
                'text': 'Ho avuto problemi con la consegna. Non sono soddisfatto.',
                'sender': 'Sara Romano',
                'type': 'comment',
                'sentiment': 'negative'
            },
            # Messaggi neutrali
            {
                'text': 'Vorrei informazioni sui prezzi e disponibilità.',
                'sender': 'Marco Ferrari',
                'type': 'direct_message',
                'sentiment': 'neutral'
            },
            {
                'text': 'Quando sarà disponibile il nuovo modello?',
                'sender': 'Giulia Conti',
                'type': 'comment',
                'sentiment': 'neutral'
            },
            {
                'text': 'A che ora chiudete oggi?',
                'sender': 'Roberto Marino',
                'type': 'direct_message',
                'sentiment': 'neutral'
            },
        ]

        for i, msg_data in enumerate(messages_data):
            # Crea il messaggio
            received_at = timezone.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))

            message, created = Message.objects.get_or_create(
                platform_message_id=f'demo_{channel.platform}_{i}',
                defaults={
                    'social_account': channel,
                    'message_type': msg_data['type'],
                    'sender_id': f'sender_{i}',
                    'sender_name': msg_data['sender'],
                    'text': msg_data['text'],
                    'received_at': received_at,
                    'is_processed': True,
                    'processed_at': received_at + timedelta(minutes=5),
                    'raw_data': {'demo': True}
                }
            )

            if created:
                # Crea l'analisi del sentiment
                sentiment_scores = {
                    'positive': 0.8,
                    'negative': -0.7,
                    'neutral': 0.0
                }

                SentimentAnalysis.objects.create(
                    message=message,
                    sentiment_label=msg_data['sentiment'],
                    sentiment_score=sentiment_scores[msg_data['sentiment']],
                    confidence=random.uniform(0.7, 0.95),
                    analyzer_used='demo_data',
                    details={
                        'polarity': sentiment_scores[msg_data['sentiment']],
                        'subjectivity': random.uniform(0.3, 0.8)
                    }
                )
