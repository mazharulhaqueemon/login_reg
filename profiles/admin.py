from django.contrib import admin

from profiles.models import Profile


# Register your models here.
@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']