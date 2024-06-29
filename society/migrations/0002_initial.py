# Generated by Django 4.2 on 2024-06-28 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('society', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_staff', to='user.userdetails'),
        ),
        migrations.AddField(
            model_name='staff',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userdetails'),
        ),
        migrations.AddField(
            model_name='staff',
            name='society_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_members', to='society.society_profile'),
        ),
        migrations.AddField(
            model_name='staff',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_staff', to='user.userdetails'),
        ),
        migrations.AddField(
            model_name='society_profile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_societies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='society_profile',
            name='society_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.society'),
        ),
        migrations.AddField(
            model_name='society_profile',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_societies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='building',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='society.society_profile'),
        ),
    ]
