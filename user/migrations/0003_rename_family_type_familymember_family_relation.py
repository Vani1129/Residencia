# Generated by Django 4.2 on 2024-06-26 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_familymember_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='familymember',
            old_name='family_type',
            new_name='family_relation',
        ),
    ]
