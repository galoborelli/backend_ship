from turtle import title
from django.contrib import admin

# Register your models here.
from .models import Reserve, Image, Schedules, Video

@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('id_reserve', 'name', 'date_selected', 'contact', 'quantity', 'message')
    search_fields = ('id_reserve', 'name', 'date_selected', 'contact')


@admin.register(Schedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('init_hour', 'end_hour', 'type')
    search_fields = ('type', 'init_hour', 'end_hour')



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section',)
    ordering = ('section', 'order')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')
    list_filter = ('section',)
    ordering = ('section', 'title')    