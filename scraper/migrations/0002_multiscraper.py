# Generated by Django 3.2.16 on 2022-11-08 02:06

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0027_alter_jsonconfig_textforwinner'),
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiScraper',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('scrapableURL',
                 models.CharField(
                     max_length=128)),
                ('sourceURL',
                 models.CharField(
                     max_length=128)),
                ('lastSuccessfulScrape',
                 models.DateTimeField(
                     blank=True,
                     null=True)),
                ('lastFailedScrape',
                 models.DateTimeField(
                     blank=True,
                     null=True)),
                ('areResultsCertified',
                 models.BooleanField(
                     default=False)),
                ('jsonConfig',
                 models.OneToOneField(
                     blank=True,
                     null=True,
                     on_delete=django.db.models.deletion.CASCADE,
                     to='visualizer.jsonconfig')),
                ('listOfElections',
                 sortedm2m.fields.SortedManyToManyField(
                     blank=True,
                     help_text=None,
                     related_name='_multiscraper_listOfElections_+',
                     to='visualizer.JsonConfig')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]