# Generated by Django 4.2 on 2024-07-09 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('communication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communication',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communication', to='user.society'),
        ),
    ]
