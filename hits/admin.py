from django.contrib import admin

from .models import MACHOObject, CatalinaObject, Vote, FullVote, PendingQuestion, FullPendingQuestion

admin.site.register(MACHOObject)
admin.site.register(CatalinaObject)
admin.site.register(Vote)
admin.site.register(FullVote)
admin.site.register(PendingQuestion)
admin.site.register(FullPendingQuestion)
