# Generated by Django 4.0.4 on 2022-11-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_disliked_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='predicts',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
