# Generated by Django 5.1.6 on 2025-02-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0002_alter_battle_date_alter_battle_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='battle_log',
            field=models.TextField(blank=True),
        ),
    ]
