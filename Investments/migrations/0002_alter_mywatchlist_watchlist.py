# Generated by Django 4.1.4 on 2023-01-23 15:29

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Investments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mywatchlist',
            name='watchlist',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), default=list, size=None),
        ),
    ]
