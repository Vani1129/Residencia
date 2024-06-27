# Generated by Django 4.2 on 2024-06-27 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Society_profile',
            fields=[
                ('society_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_numbers', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=10, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=10, null=True)),
                ('registration_no', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=100)),
                ('joined_date', models.DateField()),
                ('duty_hours_from', models.TimeField()),
                ('duty_hours_to', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(blank=True, max_length=10, null=True)),
                ('unit_type', models.CharField(blank=True, max_length=10, null=True)),
                ('area', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='society.building')),
            ],
        ),
    ]
