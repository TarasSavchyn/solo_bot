from django.contrib import admin

from app.models import Event, TelegramUser

admin.site.register(TelegramUser)
admin.site.register(Event)

