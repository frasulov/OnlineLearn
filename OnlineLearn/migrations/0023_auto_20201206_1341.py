# Generated by Django 3.1 on 2020-12-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0022_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='started',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
