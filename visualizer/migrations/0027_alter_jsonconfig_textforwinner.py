# Generated by Django 3.2.5 on 2021-10-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0026_jsonconfig_ispreferentialblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsonconfig',
            name='textForWinner',
            field=models.IntegerField(
                choices=[
                    (0,
                     'Candidate was elected'),
                    (1,
                     'Candidate won'),
                    (2,
                     'Candidate advanced to the general'),
                    (3,
                     'Candidate is in the lead')],
                default=0),
        ),
    ]