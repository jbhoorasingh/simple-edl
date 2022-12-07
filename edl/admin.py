from django.contrib import admin
from .models import Edl, EdlEntry


class EdlAdmin(admin.ModelAdmin):
    list_display = ("name", "edl_type", "edl_entries_count")
    list_filter = ("edl_type",)

    def edl_entries_count(self, obj):
        # from django.db.models import Count
        result = EdlEntry.objects.filter(edl_id=obj.id).all()
        return len(result)


class EdlEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_value", "edl", "valid_until")
    list_filter = ("edl",)



admin.site.register(Edl, EdlAdmin)
admin.site.register(EdlEntry, EdlEntryAdmin)
