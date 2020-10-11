# Generated by Django 3.1.2 on 2020-10-11 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_ggfilm_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmRecordUpdateLocker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name="locker's name")),
                ('the_first', models.BooleanField(default=False, verbose_name='is the first time to create or not')),
                ('update', models.IntegerField(default=0, verbose_name='how many times we have updated the records')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'The Massive Dev Chart - Film Record Update Locker',
                'verbose_name_plural': 'The Massive Dev Chart - Film Record Update Locker',
            },
        ),
    ]
