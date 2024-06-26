# Generated by Django 5.0 on 2024-04-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconfacial1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='APELLIDO',
            new_name='apellido',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='CEDULA',
            new_name='cedula',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='NOMBRE',
            new_name='nombre',
        ),
        migrations.AddField(
            model_name='persona',
            name='photo_path',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
