# Generated by Django 3.1.4 on 2021-01-03 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spoton', '0002_delete_choiceresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkboxresponse',
            name='choices',
            field=models.ManyToManyField(related_name='choice_responses', to='spoton.Choice'),
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_responses', to='spoton.question'),
        ),
    ]
