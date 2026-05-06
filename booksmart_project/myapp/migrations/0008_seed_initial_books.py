import json
from pathlib import Path

from django.db import migrations


def load_initial_books(apps, schema_editor):
    fixture_path = Path(__file__).resolve().parents[2] / 'initial_data.json'
    data = json.loads(fixture_path.read_text(encoding='utf-8'))

    Genre = apps.get_model('myapp', 'Genre')
    Book = apps.get_model('myapp', 'Book')

    for entry in data:
        if entry['model'] != 'myapp.genre':
            continue

        Genre.objects.update_or_create(
            pk=entry['pk'],
            defaults=entry['fields'],
        )

    for entry in data:
        if entry['model'] != 'myapp.book':
            continue

        fields = entry['fields'].copy()
        fields['genre_id'] = fields.pop('genre')
        Book.objects.update_or_create(
            pk=entry['pk'],
            defaults=fields,
        )


def unload_initial_books(apps, schema_editor):
    Book = apps.get_model('myapp', 'Book')
    Genre = apps.get_model('myapp', 'Genre')

    Book.objects.filter(pk__in=range(1, 11)).delete()
    Genre.objects.filter(pk__in=range(1, 11)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_contactmessage'),
    ]

    operations = [
        migrations.RunPython(load_initial_books, unload_initial_books),
    ]
