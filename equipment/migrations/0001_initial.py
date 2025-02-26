# Generated by Django 5.1.5 on 2025-02-04 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('tipo', models.CharField(choices=[('weapon', 'Weapon'), ('armor', 'Armor')], max_length=50)),
                ('potencia', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.equipment')),
                ('endurance', models.IntegerField()),
            ],
            bases=('equipment.equipment',),
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.equipment')),
                ('alcance', models.IntegerField()),
            ],
            bases=('equipment.equipment',),
        ),
    ]
