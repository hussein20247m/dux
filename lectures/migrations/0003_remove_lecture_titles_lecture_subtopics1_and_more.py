# Generated by Django 5.0.1 on 2024-01-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0002_title_remove_lecture_title_alter_lecture_course_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='titles',
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics1',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics10',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics11',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics12',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics13',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics14',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics2',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics3',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics4',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics5',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics6',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics7',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics8',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='lecture',
            name='subtopics9',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.DeleteModel(
            name='Title',
        ),
    ]