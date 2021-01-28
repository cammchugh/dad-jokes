# Generated by Django 3.1.5 on 2021-01-28 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DadJoke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joke_reference_id', models.CharField(max_length=128, unique=True)),
                ('joke_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.CharField(choices=[('1_chuckle', 'Chuckle'), ('2_titter', 'Titter'), ('3_giggle', 'Giggle'), ('4_chortle', 'Chortle'), ('5_cackle', 'Cackle'), ('6_belly_laugh', 'LOL'), ('7_sputtering_burst', 'LMFAO')], max_length=64)),
                ('dad_joke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='rate_jokes.dadjoke')),
                ('rated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_jokes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
