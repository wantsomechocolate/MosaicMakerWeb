# Generated by Django 3.2.7 on 2021-10-20 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mosaic', '0002_auto_20211020_0758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='coordinate_x',
            new_name='coordinate_h',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='coordinate_y',
            new_name='coordinate_w',
        ),
    ]
