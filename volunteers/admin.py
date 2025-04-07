from django.contrib import admin
from django.utils.html import format_html
from volunteers.models import (
    Volunteer,
    VolunteerParticipation,
    VolunteerPositions,
    Locations,
    Event,
)

admin.site.register(VolunteerPositions)
admin.site.register(Locations)
admin.site.register(Event)

@admin.register(VolunteerParticipation)
class VolunteerParticipationAdmin(admin.ModelAdmin):
    list_display = (
        'volunteer',
        'event__name',
        'status',
    )
    list_filter = (
        'status',
        'event__name',
    )


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'education',
        'phone',
        'view_telegram',
    )

    @admin.display(empty_value='---')
    def view_telegram(self, obj):
        return format_html(f'<a href="{obj.telegram_link}">Telegram</a>')