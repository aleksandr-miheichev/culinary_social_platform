import csv

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, CustomUser, Genre, GenreTitle,
                            Review, Title)

TABLES = {
    CustomUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

replace_field = [
    'author',
    'category',
]


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **kwargs):
        for model, csv_file in TABLES.items():
            file_path = f'./static/data/{csv_file}'
            try:
                f = open(file_path, 'r', encoding='utf8')
            except FileNotFoundError:
                print(f'Sorry, the file "{csv_file}" does not exist.')
            else:
                with f:
                    reader = csv.DictReader(f, delimiter=',')
                    for index, field in enumerate(reader.fieldnames):
                        if field in replace_field:
                            reader.fieldnames[index] += '_id'
                    for data in reader:
                        model.objects.get_or_create(**data)
        self.stdout.write(
            self.style.SUCCESS('Database successfully loaded into models!')
        )
