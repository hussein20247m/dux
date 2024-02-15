# Generated by Django 5.0.1 on 2024-01-29 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0004_alter_lecture_subtopics1_alter_lecture_subtopics10_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='subtopicsLecturecontain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('exam_link', models.URLField(blank=True, null=True)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectures.lecture')),
            ],
        ),
    ]