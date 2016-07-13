from django.contrib import admin

from .models import Macho, MachoDetail


class DetailInline(admin.TabularInline):
    model = MachoDetail
    extra = 0
    can_delete = False
    readonly_fields = ('mjd','mag','err',)


class MachoAdmin(admin.ModelAdmin):
    list_display = ['macho_id', 'period', 'true_label']
    inlines = [DetailInline]
    readonly_fields = ('macho_id', 'periodicity', 'period', 'true_label',)


admin.site.register(Macho, MachoAdmin)
