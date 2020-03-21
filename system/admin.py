from django.contrib import admin

# Register your models here.
from system.models import Slider, ImageFile, News


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["name", "types"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["types", "title", "content"]


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    list_display = ["summary"]

