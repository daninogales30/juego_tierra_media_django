# Generated by Django 5.1.5 on 2025-02-18 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='equipment/'),
        ),
    ]
