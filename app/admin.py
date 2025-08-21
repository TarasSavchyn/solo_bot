from django.contrib import admin

from app.models import Event, Contractor, TelegramUser

admin.site.register(TelegramUser)
admin.site.register(Event)
admin.site.register(Contractor)
