from django.db import models


class Event(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
    )
    telegram_link = models.CharField(
        max_length=255,
    )
    name = models.CharField(
        max_length=255,
    )
    event_timing_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    event_drive_guests_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    event_drive_photographer_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    current_event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.telegram_id)
