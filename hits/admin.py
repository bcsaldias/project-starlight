from django.contrib import admin

from .models import Hits, HitsDetail, VoteHits

class DetailInline(admin.TabularInline):
    model = HitsDetail
    extra = 0
    can_delete = False
    readonly_fields = ('mjd','mag','err',)


class VotesInline(admin.TabularInline):
    model = VoteHits
    extra = 0
    readonly_fields = ('expert','label')


class HitsAdmin(admin.ModelAdmin):
    list_display = ['hits_id', 'periodLS', 'true_label']
    inlines = [DetailInline, VotesInline]
    readonly_fields = ('hits_id', 'period_fit', 'periodLS', 'mag_mean', 'mag_std', 'true_label',)


class VotesAdmin(admin.ModelAdmin):
    list_display = ('expert','hits','label')
    readonly_fields = ('expert','hits')
    class Meta:
        verbose_name = 'HiTS Votes'
        verbose_name_plural = 'HiTS Votes'


admin.site.register(Hits, HitsAdmin)
admin.site.register(VoteHits, VotesAdmin)
