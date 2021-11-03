import csv
import os

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    """Загружает csv в базу данных."""

    TABLES_DICT = {User: 'users.csv',
                   Category: 'category.csv',
                   Genre: 'genre.csv',
                   Title: 'titles.csv',
                   Review: 'review.csv',
                   Comment: 'comments.csv',
                   None: 'genre_title.csv'
                   }

    FIELDS_WITH_ID = {'category': 'category_id',
                      'author': 'author_id'}

    USER_ROLES = {
        'admin': 'is_superuser',
        'moderator': 'is_staff'
    }

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def data_fixer(self, table, row):
        data = dict(row.items())
        for key in data.copy():
            if key in self.FIELDS_WITH_ID:
                data[self.FIELDS_WITH_ID[key]] = data.pop(key)
        if table is User:
            role = data['role']
            if role in self.USER_ROLES:
                data[self.USER_ROLES[role]] = True
        return data

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        for table, file in self.TABLES_DICT.items():
            filename = os.path.join(path, file)
            with open(filename, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data = self.data_fixer(table, row)
                    if table is None:
                        title = Title.objects.get(id=row['title_id'])
                        genre = Genre.objects.get(id=row['genre_id'])
                        title.genre.add(genre)
                    else:
                        table(**data).save()
