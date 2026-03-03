from django.contrib import admin
from munro_app.models import Munro, ClimbRecord, Photo, UserProfile, UserFavouriteMunro

class MunroAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'region', 'difficulty_rating')
    search_fields = ('name', 'region')
    list_filter = ('region', 'difficulty_rating')

class ClimbRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'munro', 'climb_date', 'star_rating')
    list_filter = ('climb_date', 'star_rating')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('record', 'uploaded_at')

admin.site.register(Munro, MunroAdmin)
admin.site.register(ClimbRecord, ClimbRecordAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(UserProfile)
admin.site.register(UserFavouriteMunro)
