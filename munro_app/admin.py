from django.contrib import admin
from .models import Munro, ClimbRecord, Photo, UserFavouriteMunro

#django built in
# list_display - table with those columns
# search_fields - can search for those fields
# list_filter - sidebare filter on admin page

#customize how Munnro model appears in admin
#"register" makes is visible + manageable on the admin site
@admin.register(Munro)
class MunroAdmin(admin.ModelAdmin):
    list_display = ("name", "region","height", "difficulty_rating" )
    search_fields = ("name", "region")
    list_filter = ("region", "difficulty_rating")

@admin.register(ClimbRecord)
class ClimbRecordoAdmin(admin.ModelAdmin):
    list_display = ("user", "munro","climb_date", "star_rating" )
    search_fields = ("climb_date", "star_rating")
    list_filter =("user__username", "munro__name")
# the double __ is a lookup path in django. will  go to that related object and use that field


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("record", "uploaded_at", "image")

@admin.register(UserFavouriteMunro)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "munro","set_at")
