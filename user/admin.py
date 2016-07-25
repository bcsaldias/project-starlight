from django.contrib import admin

from .models import Expert, Activities
from hits.models import VoteHits



class VotesInline(admin.TabularInline):
    model = VoteHits
    extra = 0
    readonly_fields = ('hits','label')


class ExpertAdmin(admin.ModelAdmin):
    inlines = [VotesInline]


admin.site.register(Expert, ExpertAdmin)

# class ActivitiesInline(admin.TabularInline):
#     model = Activities
#     extra = 0
#     can_delete = False
