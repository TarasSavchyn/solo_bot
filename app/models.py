from django.db import models
from app.choises import EventType


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True,
        help_text="Унікальний ID користувача в Telegram",
    )
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Telegram username (наприклад, @username)",
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Ім'я користувача",
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Прізвище користувача",
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Стан користувача для FSM (якщо використовується)",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Чи активний користувач",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата створення користувача",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Дата останнього оновлення користувача"
    )

    def __str__(self):
        return f"{self.username or self.first_name} ({self.telegram_id})"


class Event(models.Model):
    event_name = models.CharField(
        max_length=255,
        help_text="Назва події",
    )
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        help_text="Тип події (весілля, ювілей, побачення тощо)",
    )
    event_date = models.DateTimeField(
        help_text="Дата та час проведення події",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Місце проведення події",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Детальний опис події",
    )
    approx_participants = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Орієнтовна кількість учасників",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Чи активна подія",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата створення події",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Дата останнього оновлення події",
    )
    users = models.ManyToManyField(
        "TelegramUser",
        blank=True,
        related_name="events",
        help_text="Замовники події",
    )

    contractors = models.ManyToManyField(
        "Contractor",
        blank=True,
        related_name="events",
        help_text="Підрядники, які беруть участь у події",
    )

    def __str__(self):
        return self.event_name


class Contractor(models.Model):

    telegram_id = models.BigIntegerField(
        unique=True,
        help_text="Унікальний ID користувача в Telegram",
    )
    name = models.CharField(
        max_length=255,
        help_text="Назва підрядника або компанії",
    )
    contact_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Ім'я контактної особи",
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Телефон підрядника",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email підрядника",
    )
    service_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Тип послуг, які надає підрядник (фотограф, ведучий, кейтеринг тощо)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата створення запису про підрядника",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Дата останнього оновлення запису про підрядника",
    )

    def __str__(self):
        return self.name
