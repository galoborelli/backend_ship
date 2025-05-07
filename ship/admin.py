from django.contrib import admin

# Register your models here.
from .models import Reserve, Image, Schedules

@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('id_reserve', 'name', 'date_reserve', 'email', 'phone', 'cuantity', 'message')
    search_fields = ('id_reserve', 'name', 'date_reserve', 'email', 'phone')


@admin.register(Schedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('init_hour', 'end_hour', 'type')
    search_fields = ('id_schedule', 'date', 'time')



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section',)
    ordering = ('section', 'order')