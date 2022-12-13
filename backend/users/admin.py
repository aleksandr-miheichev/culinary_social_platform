from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role',)
    list_filter = ('first_name', 'email',)
    search_fields = ('username', 'email',)
    save_on_top = True
