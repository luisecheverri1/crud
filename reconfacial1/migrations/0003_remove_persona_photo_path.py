# Generated by Django 5.0 on 2024-04-03 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reconfacial1', '0002_rename_apellido_persona_apellido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='photo_path',
        ),
    ]
