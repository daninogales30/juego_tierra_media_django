# Generated by Django 5.1.5 on 2025-02-04 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('character1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character1', to='character.character')),
                ('character2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character2', to='character.character')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ganador_batalla', to='character.character')),
            ],
        ),
    ]
