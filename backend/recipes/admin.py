from django.contrib import admin

from recipes.models import (Ingredient, FavoritesRecipe, Recipe, ShoppingList,
                            Subscription, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(FavoritesRecipe)
class FavoritesRecipeAdmin(admin.ModelAdmin):
    list_display = ('user.username', 'recipe.name',)
    search_fields = ('user.username', 'recipe.name',)
    list_filter = ('user.username', 'recipe.name',)
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author.username', 'name', 'tags.name', 'cooking_time',)
    search_fields = ('author.username', 'name', 'cooking_time',)
    list_filter = ('author.username', 'name', 'tags.name', 'cooking_time',)
    save_on_top = True

    @staticmethod
    @admin.display(description='Число рецептов в Избранном')
    def get_favorites_recipe_count(obj):
        return obj.in_favorites.count()


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user.username', 'recipe.name',)
    search_fields = ('user.username', 'recipe.name',)
    list_filter = ('user.username', 'recipe.name',)
    save_on_top = True


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user.username', 'subscribed_author.username',)
    search_fields = ('user.username', 'subscribed_author.username',)
    list_filter = ('user.username', 'subscribed_author.username',)
    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    save_on_top = True
