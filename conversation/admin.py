from django.contrib import admin
from . import models
# Register your models here
admin.site.register(models.Conversation)
admin.site.register(models.ConversationMessage)
