# Generated by Django 3.1 on 2020-12-05 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0013_auto_20201205_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]