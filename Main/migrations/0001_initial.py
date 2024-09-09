# Generated by Django 5.1.1 on 2024-09-09 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unix_month', models.IntegerField()),
                ('parameter_a', models.FloatField()),
                ('parameter_b', models.FloatField()),
                ('parameter_c', models.FloatField()),
                ('parameter_d', models.FloatField()),
                ('parameter_e', models.FloatField()),
                ('parameter_f', models.FloatField()),
                ('parameter_g', models.FloatField()),
                ('parameter_h', models.FloatField()),
            ],
        ),
    ]
