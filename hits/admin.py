from django.contrib import admin

from .models import MACHOObject, Vote, PendingQuestion

admin.site.register(MACHOObject)
admin.site.register(Vote)
admin.site.register(PendingQuestion)
