# Generated by Django 4.1.4 on 2022-12-19 21:23

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование для ингредиента', max_length=200, verbose_name='Наименование')),
                ('measurement_unit', models.CharField(help_text='Введите единицу измерения для ингредиента', max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Выберите фотографию для загрузки', upload_to='recipes/', verbose_name='Фотография')),
                ('text', models.TextField(help_text='Опишите способ приготовления данного блюда', verbose_name='Описание способа приготовления')),
                ('cooking_time', models.IntegerField(error_messages={'Ошибка': 'Пожалуйста, установите время приготовления данного рецепта более 1 минуты'}, help_text='Укажите время приготовления в минутах для данного блюда', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в минутах')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество ингредиентов')),
            ],
            options={
                'verbose_name': 'Рецепт и ингредиент блюда',
                'verbose_name_plural': 'Рецепты и ингредиенты блюд',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Рецепт и тег блюда',
                'verbose_name_plural': 'Рецепты и теги блюд',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Список покупок',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название тега', max_length=200, unique=True, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FF0000', help_text='Выберите цвет для тега', image_field=None, max_length=7, samples=None, unique=True, verbose_name='Цвет в формате hex')),
                ('slug', models.SlugField(help_text='Введите уникальный идентификатор тега для рецепта', max_length=200, unique=True, validators=[recipes.validators.validate_slug], verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
    ]
