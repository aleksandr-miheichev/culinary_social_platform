from django.contrib import admin

from recipes.models import (FavoritesRecipe, Ingredient, Recipe,
                            RecipeIngredient, RecipeTag, ShoppingList,
                            Subscription, Tag)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(FavoritesRecipe)
class FavoritesRecipeAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_recipe_name',)
    search_fields = ('user__username', 'recipe__name',)
    list_filter = ('user__username', 'recipe__name',)
    save_on_top = True

    @admin.display(ordering='user__username', description='Логин пользователя')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Название рецепта')
    def get_recipe_name(self, obj):
        return obj.recipe.name


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'get_username_author',
        'name',
        'cooking_time',
        'get_favorites_recipe_count'
    )
    search_fields = ('author__username', 'name', 'cooking_time',)
    list_filter = ('author__username', 'name', 'tags__name', 'cooking_time',)
    inlines = (RecipeIngredientInLine, RecipeTagInLine,)
    save_on_top = True

    @admin.display(description='Число добавлений данного рецепта в Избранное')
    def get_favorites_recipe_count(self, obj):
        return obj.in_favorites.count()

    @admin.display(
        ordering='author__username',
        description='Логин автора рецепта'
    )
    def get_username_author(self, obj):
        return obj.author.username


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_recipe_name',)
    search_fields = ('user__username', 'recipe__name',)
    list_filter = ('user__username', 'recipe__name',)
    save_on_top = True

    @admin.display(ordering='user__username', description='Логин пользователя')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Название рецепта')
    def get_recipe_name(self, obj):
        return obj.recipe.name


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('get_username_user', 'get_username_subscribed_author',)
    search_fields = ('user__username', 'subscribed_author__username',)
    list_filter = ('user__username',)
    save_on_top = True

    @admin.display(
        ordering='user__username',
        description='Пользователь, подписавшийся на автора'
    )
    def get_username_user(self, obj):
        return obj.user.username

    @admin.display(
        description='Автор на которого подписались'
    )
    def get_username_subscribed_author(self, obj):
        return obj.subscribed_author.username


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
