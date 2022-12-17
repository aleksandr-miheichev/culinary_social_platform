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
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'cooking_time',)
    search_fields = ('author', 'name', 'cooking_time',)
    list_filter = ('author', 'name', 'tags', 'cooking_time',)
    inlines = (RecipeIngredientInLine, RecipeTagInLine,)
    save_on_top = True

    @admin.display(description='Число добавлений данного рецепта в Избранное')
    def get_favorites_recipe_count(self, obj):
        return obj.in_favorites.count()


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    save_on_top = True


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed_author',)
    search_fields = ('user', 'subscribed_author',)
    list_filter = ('user', 'subscribed_author',)
    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    save_on_top = True
