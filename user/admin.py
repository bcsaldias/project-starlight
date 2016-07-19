from django.contrib import admin

from .models import Expert, Activities


class DetailInline(admin.TabularInline):
    model = Activities
    extra = 0
    can_delete = False


class ExpertAdmin(admin.ModelAdmin):
    inlines = [DetailInline]


admin.site.register(Expert, ExpertAdmin)
