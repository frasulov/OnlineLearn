# Generated by Django 3.1 on 2020-12-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0018_auto_20201206_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(blank=True, related_name='question', to='OnlineLearn.Answer'),
        ),
    ]
