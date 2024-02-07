from django.contrib import admin
from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title'
    )
    search_fields = ('title',)
    ordering = ['title']


admin.site.register(Event, EventAdmin)
