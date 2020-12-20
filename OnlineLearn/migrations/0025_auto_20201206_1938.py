# Generated by Django 3.1 on 2020-12-06 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineLearn', '0024_auto_20201206_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qa', to='OnlineLearn.answer')),
                ('q', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qa', to='OnlineLearn.question')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='choices',
            field=models.ManyToManyField(blank=True, related_name='exams', to='OnlineLearn.QA'),
        ),
    ]
