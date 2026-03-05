from django.core.management.base import BaseCommand
from app.models import Event, TelegramUser
import random


class Command(BaseCommand):
    help = "Populate database with test data"

    def handle(self, *args, **kwargs):

        events = []

        for i in range(5):
            event = Event.objects.create(
                code=f"{i}{i}{i}",
                telegram_link=f"https://t.me/test_event_{i}",
                name=f"Test Event {i}",
                event_timing_link="https://example.com/timing",
                event_drive_guests_link="https://drive.google.com/guests",
                event_drive_photographer_link="https://drive.google.com/photos",
            )
            events.append(event)

        for i in range(20):
            TelegramUser.objects.create(
                telegram_id=100000000 + i,
                username=f"user{i}",
                first_name=f"User{i}",
                current_event=random.choice(events),
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully"))