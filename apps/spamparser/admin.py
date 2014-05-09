"""Admin configuration for spamparser app"""

from django.contrib import admin

from .models import Publisher, Sender, Recipient, Spam

admin.site.register(Publisher)
admin.site.register(Sender)
admin.site.register(Recipient)
admin.site.register(Spam)
