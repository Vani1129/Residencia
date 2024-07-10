# Generated by Django 4.2 on 2024-07-09 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('society', '0003_alter_societyprofile_society'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='total_flats',
            field=models.PositiveIntegerField(default=0, verbose_name='Number of Flats'),
        ),
        migrations.AddField(
            model_name='building',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.type'),
        ),
    ]
