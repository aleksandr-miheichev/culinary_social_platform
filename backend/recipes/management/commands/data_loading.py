import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient

csv_file = 'ingredients.csv'


class Command(BaseCommand):
    help = "Loading data from a csv file into the Ingredient model."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING(
                'Started filling the Ingredient model from a csv file!'
            )
        )
        file_path = f'./static/data/{csv_file}'
        try:
            f = open(file_path, 'r', encoding='utf-8')
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'Sorry, the file "{csv_file}" does not exist!'
                )
            )
        else:
            fieldnames = ['name', 'measurement_unit', ]
            with f:
                reader = csv.DictReader(
                    f,
                    fieldnames=fieldnames,
                    delimiter=','
                )
                for data in reader:
                    obj, created = Ingredient.objects.get_or_create(
                        name=data[fieldnames[0]],
                        measurement_unit=data[fieldnames[1]],
                    )
                    if not created:
                        self.stdout.write(
                            self.style.ERROR(
                                'An ingredient with the name: '
                                f'"{data[fieldnames[0]]}" and the unit '
                                f'"{data[fieldnames[1]]}" is already in the '
                                'database!')
                        )
        self.stdout.write(
            self.style.SUCCESS('Database successfully loaded into model!')
        )
