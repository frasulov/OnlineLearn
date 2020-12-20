# Generated by Django 3.1 on 2020-12-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0017_answer_question_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='quiz', to='OnlineLearn.Question'),
        ),
    ]