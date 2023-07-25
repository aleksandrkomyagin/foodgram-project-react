from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from csv file to DB'

    def handle(self, *args, **kwargs):
        Ingredient.objects.all().delete()
        with open(
            f'{settings.BASE_DIR}/data/{"ingredients.csv"}',
            'r',
            encoding='utf-8'
        ) as file:
            reader = DictReader(file, delimiter=',')
            Ingredient.objects.bulk_create(Ingredient(**d) for d in reader)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
