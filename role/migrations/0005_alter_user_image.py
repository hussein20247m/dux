# Generated by Django 5.0.1 on 2024-01-28 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0004_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
