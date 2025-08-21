from django.db import models


class EventType(models.TextChoices):
    WEDDING = "WEDDING", "Весілля"
    GENDER_PARTY = "GENDER_PARTY", "Гендер-паті"
    ANNIVERSARY = "ANNIVERSARY", "Річниця"
    FIRST_DATE = "FIRST_DATE", "Перше побачення"
    JUBILEE = "JUBILEE", "Ювілей"
    DATE = "DATE", "Побачення"
