# Generated by Django 5.0.6 on 2025-01-25 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='tilte',
            new_name='title',
        ),
    ]
