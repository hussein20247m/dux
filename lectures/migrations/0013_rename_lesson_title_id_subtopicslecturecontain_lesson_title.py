# Generated by Django 5.0.1 on 2024-01-31 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0012_alter_lecture_titles_alter_lessontitle_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtopicslecturecontain',
            old_name='lesson_title_id',
            new_name='lesson_title',
        ),
    ]