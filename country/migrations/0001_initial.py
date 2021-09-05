# Generated by Django 3.2.7 on 2021-09-02 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('country_code', models.CharField(blank=True, max_length=30, null=True)),
                ('slug', models.SlugField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.region')),
            ],
        ),
    ]
