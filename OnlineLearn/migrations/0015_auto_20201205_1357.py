# Generated by Django 3.1 on 2020-12-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0014_auto_20201205_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]