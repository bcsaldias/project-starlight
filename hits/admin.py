from django.contrib import admin

from .models import Hits, HitsDetail

class DetailInline(admin.TabularInline):
    model = HitsDetail
    extra = 0
    can_delete = False
    readonly_fields = ('mjd','mag','err',)


class HitsAdmin(admin.ModelAdmin):
    list_display = ['hits_id', 'periodLS', 'true_label']
    inlines = [DetailInline]
    readonly_fields = ('hits_id', 'period_fit', 'periodLS', 'mag_mean', 'mag_std', 'true_label',)


admin.site.register(Hits, HitsAdmin)
