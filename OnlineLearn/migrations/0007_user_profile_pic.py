# Generated by Django 3.1 on 2020-12-05 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0006_auto_20201205_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
