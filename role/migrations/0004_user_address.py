# Generated by Django 5.0.1 on 2024-01-28 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0003_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Address',
            field=models.CharField(max_length=100, null=True),
        ),
    ]