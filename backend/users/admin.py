from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'get_recipe_count',
        'get_subscribers_count',
    )
    list_filter = ('first_name', 'email',)
    search_fields = ('username', 'email',)
    save_on_top = True

    @admin.display(description='Количество рецептов')
    def get_recipe_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Количество подписчиков')
    def get_subscribers_count(self, obj):
        return obj.subscriber.count()
