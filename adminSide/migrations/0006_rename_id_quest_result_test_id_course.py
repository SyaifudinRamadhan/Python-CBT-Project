# Generated by Django 3.2.7 on 2021-10-16 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminSide', '0005_quest_data_id_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result_test',
            old_name='id_quest',
            new_name='id_course',
        ),
    ]