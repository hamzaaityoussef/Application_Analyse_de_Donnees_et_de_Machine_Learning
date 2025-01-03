# Generated by Django 5.0.4 on 2024-11-25 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ML_Application', '0003_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='copied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status_cleaned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status_encoded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status_normalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status_standarized',
            field=models.BooleanField(default=False),
        ),
    ]
