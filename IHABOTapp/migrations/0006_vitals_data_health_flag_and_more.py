# Generated by Django 4.1 on 2022-08-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IHABOTapp', '0005_rename_diastolic_bp_flag_vitals_data_bp_flag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitals_data',
            name='health_flag',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='vitals_data',
            name='health_prediction',
            field=models.CharField(default='Normal', max_length=20),
        ),
    ]
