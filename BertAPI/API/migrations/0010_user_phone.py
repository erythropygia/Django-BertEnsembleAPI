# Generated by Django 4.1.6 on 2023-03-13 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
