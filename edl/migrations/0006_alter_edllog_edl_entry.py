# Generated by Django 4.1.2 on 2024-01-16 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edl', '0005_edllog_alter_edl_options_alter_edlentry_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edllog',
            name='edl_entry',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
