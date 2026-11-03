from django.contrib import admin

# Register your models here.
from .models import BookmarkedProfile
@admin.register(BookmarkedProfile)
class BookmarkedProfileAdmin(admin.ModelAdmin):
 list_display = ("username", "user", "public_repos", "followers", "created_at")
 search_fields = ("username", "name", "user_username") 