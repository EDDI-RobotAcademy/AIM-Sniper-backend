# Generated by Django 5.1.1 on 2024-09-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_rename_survey_id_survey_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveydescription',
            name='description',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
