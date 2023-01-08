import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag

TABLES = {
    Ingredient: 'ingredients.csv',
    Tag: 'tags.csv',
}

TAGS_HEADER = ['name', 'color', 'slug', ]

INGREDIENTS_HEADER = ['name', 'measurement_unit', ]

TAGS_DATA = [
    {'name': 'На завтрак', 'color': '#ffcf48', 'slug': 'na-zavtrak'},
    {'name': 'На обед', 'color': '#ffff00', 'slug': 'na-obed'},
    {'name': 'На ужин', 'color': '#f64747', 'slug': 'na-uzhin'},
    {'name': 'Праздничный', 'color': '#00ff00', 'slug': 'prazdnichnyj'},
    {'name': 'За 5 минут', 'color': '#ff0000', 'slug': 'za-5-minut'},
]


class Command(BaseCommand):
    help = ("First, a csv file with recipe tags is created, then data from it "
            "is loaded into the database and then data from the csv file with "
            "ingredients is loaded into the Ingredients model.")

    def handle(self, *args, **kwargs): # noqa: C901
        for model, csv_file in TABLES.items():
            file_path = f'./static/data/{csv_file}'
            if model == Tag:
                self.stdout.write(
                    self.style.WARNING(
                        'Started creating a csv file with recipe tags!'
                    )
                )
                with open(
                        file=file_path,
                        mode='w',
                        encoding='utf-8',
                        newline=''
                ) as f:
                    writer = csv.DictWriter(f=f, fieldnames=TAGS_HEADER)
                    writer.writeheader()
                    writer.writerows(TAGS_DATA)
                self.stdout.write(
                    self.style.SUCCESS(
                        'The csv file with recipe tags was successfully '
                        'created!'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        'Started adding data from a csv file to the Tag model!'
                    )
                )
                try:
                    f = open(file=file_path, mode='r', encoding='utf8')
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Sorry, the file "{csv_file}" does not exist!'
                        )
                    )
                else:
                    with f:
                        reader = csv.DictReader(f, delimiter=',')
                        for data in reader:
                            obj, created = model.objects.get_or_create(**data)
                            if not created:
                                self.stdout.write(
                                    self.style.ERROR(
                                        'The tag with the name '
                                        f'"{data[TAGS_HEADER[0]]}" is already '
                                        'in the database!'
                                    )
                                )
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Database successfully loaded into model!'
                            )
                        )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        'Started adding data from a csv file to the '
                        'Ingredient model!'
                    )
                )
                try:
                    f = open(file=file_path, mode='r', encoding='utf8')
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Sorry, the file "{csv_file}" does not exist!'
                        )
                    )
                else:
                    with f:
                        reader = csv.DictReader(
                            f=f,
                            fieldnames=INGREDIENTS_HEADER,
                            delimiter=','
                        )
                        for data in reader:
                            obj, created = model.objects.get_or_create(**data)
                            if not created:
                                self.stdout.write(
                                    self.style.ERROR(
                                        'An ingredient with the name: '
                                        f'"{data[INGREDIENTS_HEADER[0]]}" is '
                                        'already in the database!')
                                )
                        self.stdout.write(
                            self.style.SUCCESS(
                                'Database successfully loaded into model!'
                            )
                        )
