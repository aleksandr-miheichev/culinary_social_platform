# Продуктовый помощник

![CI and CD of Foodgram project](https://github.com/aleksandr-miheichev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Содержание
- [Описание проекта](#Описание-проекта)
- [Технологический стек](#Технологический-стек)
- [Запуск проекта](#Запуск-проекта)
- [Примеры работы с проектом](#Примеры-работы-с-проектом)
- [Шаблон наполнения env-файла](#Шаблон-наполнения-env-файла)
- [Над проектом работал](#Над-проектом-работал)

### Описание проекта:

Пользователи смогут публиковать рецепты, подписываться на публикации других 
пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед 
походом в магазин скачивать сводный список продуктов, необходимых для 
приготовления одного или нескольких выбранных блюд.

 В проекте было реализовано Continuous Integration и Continuous Deployment, что 
означает:
- автоматический запуск тестов;
- обновление образов на Docker Hub;
- автоматический деплой на боевой сервер при пуше в главную ветку master или 
main.

Как выглядит проект, можно посмотреть на [Figma.com](https://clck.ru/TrMSi)

#### Главная страница

Содержимое главной страницы — список первых шести рецептов, отсортированных по 
дате публикации (от новых к старым). Остальные рецепты доступны на следующих 
страницах: внизу страницы есть пагинация.

#### Страница рецепта

На странице — полное описание рецепта. Для авторизованных пользователей — 
возможность добавить рецепт в избранное и в список покупок, возможность 
подписаться на автора рецепта.

#### Страница пользователя

На странице — имя пользователя, все рецепты, опубликованные пользователем и 
возможность подписаться на пользователя.

#### Подписка на авторов

Подписка на публикации доступна только авторизованному пользователю. Страница 
подписок доступна только владельцу.

#### Список избранного

Работа со списком избранного доступна только авторизованному пользователю. 
Список избранного может просматривать только его владелец.

#### Список покупок

Работа со списком покупок доступна авторизованным пользователям. Список покупок 
может просматривать только его владелец. Список покупок скачивается в формате 
PDF.

#### Фильтрация по тегам

При нажатии на название тега выводится список рецептов, отмеченных этим тегом.

### Технологический стек:

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
- [![Django REST Framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
- [![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
- [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
- [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
- [![gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)


### Примеры работы с проектом:

Удобную веб-страницу со справочным меню, документацией для эндпоинтов и 
разрешённых методов, с примерами запросов, ответов и кода Вы сможете посмотреть 
по адресу:

[https://aleksmihdjango.ddns.net/redoc/](https://aleksmihdjango.ddns.net/redoc/)

### Шаблон наполнения env-файла:

DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=xxxxxyyyyyzzzzz

DB_HOST=db

DB_PORT=5432

SECRET_KEY=xxxxxyyyyyzzzzz

### Над проектом работал:
- [Михеичев Александр](https://github.com/aleksandr-miheichev)

