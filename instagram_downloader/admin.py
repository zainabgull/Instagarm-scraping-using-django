from django.contrib import admin
from .models import ScrapedInstagramImage
@admin.register(ScrapedInstagramImage)
class ScrapedInstagramImageAdmin(admin.ModelAdmin):
    list_display = ('hashtag', 'image_url', 'timestamp')
    search_fields = ('hashtag', 'image_url')
