# Generated by Django 5.0 on 2024-04-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconfacial1', '0008_alter_persona_cedula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='cedula',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
