from django.contrib import admin

from .models import Event

# Display related fields in fieldsets
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title info', {'fields': ['title', 'detail']}),
        ('Outcome info', {'fields': ['outcome', 'outcome_detail']}),
        ('Event date', {'fields': ['date']}),
        ('Contact info', {'fields': ['contact_name', 'contact_email']}),
    ]
    list_display = ('title', 'date', 'outcome')
    list_filter = ['date']
    search_fields = ['title']

# Register the Event model on the admin page
admin.site.register(Event, EventAdmin)
