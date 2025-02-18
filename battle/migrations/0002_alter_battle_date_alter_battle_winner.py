# Generated by Django 5.1.5 on 2025-02-18 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='battle',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ganador_batalla', to='character.character'),
        ),
    ]
