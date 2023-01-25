from django.contrib import admin
from .models import Constellation, ConstellationImage, Galaxy, GalaxyImage, Post, PostImage, Comment

admin.site.site_header = 'Celestial Bay Admin'


@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('galaxy_type', 'constellation')


admin.site.register(Constellation)
admin.site.register(ConstellationImage)
admin.site.register(GalaxyImage)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
