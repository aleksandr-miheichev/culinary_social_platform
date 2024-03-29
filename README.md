# Кулинарная социальная платформа

![CI and CD of Foodgram project](https://github.com/aleksandr-miheichev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Содержание

- [Описание проекта](#Описание-проекта)
- [Технологический стек](#Технологический-стек)
- [Запуск проекта](#Запуск-проекта)
- [Примеры работы с проектом](#Примеры-работы-с-проектом)
- [Инструкция для накачки базы из CSV-файлов:](#Инструкция-для-накачки-базы-из-CSV-файлов)
- [Шаблон наполнения env-файла](#Шаблон-наполнения-env-файла)
- [Над frontend проекта работал](#Над-frontend-проекта-работал)
- [Над backend проекта работал](#Над-backend-проекта-работал)

---

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

---

### Технологический стек:

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
- [![Django REST Framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
- [![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
- [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
- [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
- [![gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)

---

### Как развернуть проект:

Клонировать репозиторий и перейти в него в терминале используя команду

```bash
cd
```

```bash
git clone git@github.com:aleksandr-miheichev/culinary_social_platform.git
```

---

### Копирование файлов на сервер с клонированного репозитория проекта:

В терминале IDE (к примеру - PyCharm) открытом в папке

```
foodgram-project-react/infra
```

Ввести команду для копирования необходимого файла на сервер:

```
scp docker-compose.yaml test@62.84.114.207:/home/test/docker-compose.yaml
```

```
scp data/nginx/default.conf test@62.84.114.207:/home/test/data/nginx/default.conf
```

В терминале IDE (к примеру - PyCharm) открытом в папке

```
foodgram-project-react/docs
```

Ввести команду для копирования необходимого файла на сервер:

```
scp redoc.html test@62.84.114.207:/home/test/docs/redoc.html
```

```
scp openapi-schema.yaml test@62.84.114.207:/home/test/docs/openapi-schema.yaml
```

---

### Примеры работы с проектом:

Удобную веб-страницу со справочным меню, документацией для эндпоинтов и
разрешённых методов, с примерами запросов, ответов и кода Вы сможете посмотреть
по адресу:

[https://aleksdjango.ddns.net/api/docs/](https://aleksdjango.ddns.net/api/docs/)

---

### Инструкция для накачки базы из CSV-файлов:

Для загрузки данных, получаемых вместе с проектом, из файлов csv в базу данных
через Django ORM была написана собственная management-команда.

В терминале сервера ввести команду для просмотра описания management-команды:

```
sudo docker compose exec web python manage.py data_loading -h
```

Для выполнения процедуры загрузки в базу данных необходимо выполнить:

```
sudo docker compose exec web python manage.py data_loading
```

После этого будет выведено сообщение в терминал о начале загрузки в базу
данных:

```
Started filling the Ingredient model from a csv file!
```

В случае успешного выполнения данной процедуры будет выведено сообщение в
терминал:

```
Database successfully loaded into model!
```

Если ингредиент уже был загружен в базу данных, то будет выведено сообщение в
терминал:

```
An ingredient with the name: "<наименование_ингредиента>" and the unit 
"единица_измерения_ингредиента" is already in the database!
```

При отсутствии csv файла с данными или его неправильного наименования будет
выведена ошибка:

```
Sorry, the file "<название_файла>" does not exist.
```

---

### Шаблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=xxxxxyyyyyzzzzz
DB_HOST=db
DB_PORT=5432
SECRET_KEY=xxxxxyyyyyzzzzz
ALLOWED_HOSTS=['55.222.99.11', 'praktikum.ddns.net', ]
CSRF_TRUSTED_ORIGINS=['https://example.com']
NEED_POSTGRESQL=True
```

---

### Над frontend проекта работал:

- [Yandex Praktikum](https://github.com/yandex-praktikum)

---

### Над backend проекта работал:

- [Михеичев Александр](https://github.com/aleksandr-miheichev)
