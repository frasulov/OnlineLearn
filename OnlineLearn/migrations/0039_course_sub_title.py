# Generated by Django 3.1 on 2020-12-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0038_user_last_search_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='sub_title',
            field=models.CharField(default='My Subtitle', max_length=255),
        ),
    ]