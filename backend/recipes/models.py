from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              UniqueConstraint)

from recipes.validators import validate_slug
from users.models import CustomUser


class Ingredient(Model):
    name = CharField(
        max_length=settings.MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Наименование',
        help_text='Введите наименование для ингредиента',
    )
    measurement_unit = CharField(
        max_length=settings.MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения для ингредиента',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return (
            f'Наименование ингредиента: "{self.name}", '
            f'единица измерения - "{self.measurement_unit}"'
        )


class Tag(Model):
    name = CharField(
        max_length=settings.MAX_LENGTH_TEXT_RECIPES,
        unique=True,
        verbose_name='Название',
        help_text='Введите название тега',
    )
    color = ColorField(
        max_length=settings.MAX_LENGTH_COLOR,
        default='#FF0000',
        unique=True,
        verbose_name='Цвет в формате hex',
        help_text='Выберите цвет для тега',
    )
    slug = SlugField(
        max_length=settings.MAX_LENGTH_TEXT_RECIPES,
        unique=True,
        validators=[validate_slug, ],
        verbose_name='Идентификатор',
        help_text='Введите уникальный идентификатор тега для рецепта'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'"{self.color}" - цвет в формате hex для тега: "{self.name}"'


class Recipe(Model):
    tags = ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Тег',
        help_text='Выберите уникальный идентификатор тега для рецепта'
    )
    author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент для рецепта'
    )
    name = CharField(
        max_length=settings.MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Название',
        help_text='Введите название рецепта',
    )
    image = ImageField(
        upload_to='recipes/',
        verbose_name='Фотография',
        help_text='Выберите фотографию для загрузки',
    )
    text = TextField(
        verbose_name='Описание способа приготовления',
        help_text='Опишите способ приготовления данного блюда',
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return (
            f'У рецепта блюда с названием "{self.name}" '
            f'автор - "{self.author.username}"'
        )


class RecipeIngredient(Model):
    """Вспомогательная модель для Рецепта и Ингредиента."""
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт блюда'
    )
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Ингредиент'
    )
    amount = PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Рецепт и ингредиент блюда'
        verbose_name_plural = 'Рецепты и ингредиенты блюд'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredients',
            ),
        ]

    def __str__(self):
        return (
            f'Рецепта блюда "{self.recipe.name}" '
            f'состоит из ингредиентов "{self.ingredient.name}" '
            f'и их количества равным соответственно "{self.amount}"'

        )


class RecipeTag(Model):
    """Вспомогательная модель для Рецепта и Тега."""
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт блюда'
    )
    tag = ForeignKey(
        Tag,
        on_delete=CASCADE,
        verbose_name='Тег рецепта'
    )

    class Meta:
        verbose_name = 'Рецепт и тег блюда'
        verbose_name_plural = 'Рецепты и теги блюд'

    def __str__(self):
        return f'У рецепта блюда "{self.recipe.name}" тег - "{self.tag}"'


class UserRecipeModel(Model):
    """Абстрактная модель для модели Списка покупок и Избранное."""
    user = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        verbose_name='Пользователь'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        default_related_name = '%(class)ss'
        ordering = ('-id',)


class FavoritesRecipe(UserRecipeModel):
    """Модель для добавления Рецепта в список Избранное."""

    class Meta(UserRecipeModel.Meta):
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_favorites'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return (
            f'Рецепт блюда "{self.recipe.name}" находится '
            f'у пользователя "{self.user.username}" в Избранном'
        )


class ShoppingList(UserRecipeModel):
    """Модель для добавления Рецепта в Список покупок."""

    class Meta(UserRecipeModel.Meta):
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_list'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (
            f'Рецепт блюда "{self.recipe.name}" находится '
            f'у пользователя "{self.user.username}" в Списке покупок'
        )


class Subscription(Model):
    """Модель для реализации подписки на автора рецептов."""
    user = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь, который оформил подписку на автора',
    )
    subscribed_author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='subscribed_author',
        verbose_name='Автор на которого подписались',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'subscribed_author'],
                name='unique_users_subscribed_author'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'Пользователь с логином "{self.user.username}" подписан на '
            f'автора рецептов с логином "{self.subscribed_author.username}"'
        )
