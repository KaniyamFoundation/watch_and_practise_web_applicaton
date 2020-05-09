from django.contrib import admin
from streamapp.models import Category, Tag, Event, StreamEvent, Organizer

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(StreamEvent)
