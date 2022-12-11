from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from foodgram.settings import MAX_LENGTH_COLOR, MAX_LENGTH_TEXT_RECIPES
from recipes.validators import validate_slug
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Наименование',
        help_text='Введите наименование для ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения для ингредиента',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return (
            f'Наименование ингредиента: "{self.name}", '
            f'единица измерения - "{self.measurement_unit}"'
        )


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT_RECIPES,
        unique=True,
        verbose_name='Название',
        help_text='Введите название тега',
    )
    color = ColorField(
        max_length=MAX_LENGTH_COLOR,
        default='#FF0000',
        unique=True,
        verbose_name='Цвет в формате hex',
        help_text='Введите цвет в формате hex для тега',
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_TEXT_RECIPES,
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


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Тег',
        help_text='Выберите уникальный идентификатор тега для рецепта'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент для рецепта'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_TEXT_RECIPES,
        verbose_name='Название',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фотография',
        help_text='Выберите фотографию для загрузки',
    )
    text = models.TextField(
        verbose_name='Описание способа приготовления',
        help_text='Опишите способ приготовления данного блюда',
    )
    cooking_time = models.IntegerField(
        validators=(MinValueValidator(1),),
        error_messages={
            'Ошибка': 'Пожалуйста, установите время приготовления данного '
                      'рецепта более 1 минуты'
        },
        verbose_name='Время приготовления в минутах',
        help_text='Укажите время приготовления в минутах для данного блюда',
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


class RecipeIngredient(models.Model):
    """Вспомогательная модель для Рецепта и Ингредиента."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт блюда'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Рецепт и ингредиент блюда'
        verbose_name_plural = 'Рецепты и ингредиенты блюд'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique_recipe_ingredients',
            ),
        ]

    def __str__(self):
        return (
            f'Рецепта блюда "{self.recipe}" '
            f'состоит из ингредиентов "{self.ingredient}" '
            f'и их количества равным соответственно "{self.amount}"'

        )


class RecipeTag(models.Model):
    """Вспомогательная модель для Рецепта и Тега."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт блюда'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег рецепта'
    )

    class Meta:
        verbose_name = 'Рецепт и тег блюда'
        verbose_name_plural = 'Рецепты и теги блюд'

    def __str__(self):
        return f'У рецепта блюда "{self.recipe}" тег - "{self.tag}"'


class FavoritesRecipe(models.Model):
    """Модель для добавления Рецепта в список Избранное."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites_recipe',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_favorites'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Рецепт блюда в списке Избранное'
        verbose_name_plural = 'Рецепты блюд в списке Избранное'

    def __str__(self):
        return (
            f'Рецепт блюда "{self.recipe}" находится '
            f'у пользователя "{self.user.username}" в Избранном'
        )


class ShoppingList(models.Model):
    """Модель для добавления Рецепта в Список покупок."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_list'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Рецепт блюда в списке покупок'
        verbose_name_plural = 'Рецепты блюд в списке покупок'

    def __str__(self):
        return (
            f'Рецепт блюда "{self.recipe}" находится '
            f'у пользователя "{self.user.username}" в списке покупок'
        )


class Subscription(models.Model):
    """Модель для реализации подписки на автора рецептов."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь, который оформил подписку на автора',
    )
    subscribed_author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribed_author',
        verbose_name='Автор на которого подписались',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
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
