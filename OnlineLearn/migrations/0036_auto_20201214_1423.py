# Generated by Django 3.1 on 2020-12-14 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0035_auto_20201214_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='profile_pic',
            field=models.ImageField(default='nouser.jpg', upload_to='category'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to='course'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='nouser.jpg', upload_to='user'),
        ),
    ]
