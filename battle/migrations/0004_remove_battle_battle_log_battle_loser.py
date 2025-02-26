# Generated by Django 5.1.6 on 2025-02-26 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0003_battle_battle_log'),
        ('character', '0003_character_health'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='battle_log',
        ),
        migrations.AddField(
            model_name='battle',
            name='loser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perdedor_batalla', to='character.character'),
        ),
    ]
