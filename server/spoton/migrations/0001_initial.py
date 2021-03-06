# Generated by Django 3.0.6 on 2020-12-31 23:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(default=False)),
                ('primary_text', models.CharField(default='default choice', max_length=100)),
                ('secondary_text', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='default question', max_length=400)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_spoton.question_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_spoton.questionresponse_set+', to='contenttypes.ContentType')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='spoton.Question')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user_id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheckboxQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spoton.Question')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('spoton.question',),
        ),
        migrations.CreateModel(
            name='CheckboxResponse',
            fields=[
                ('questionresponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spoton.QuestionResponse')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('spoton.questionresponse',),
        ),
        migrations.CreateModel(
            name='SliderQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spoton.Question')),
                ('slider_min', models.IntegerField(default=0)),
                ('slider_max', models.IntegerField(default=10)),
                ('answer', models.IntegerField(default=5)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('spoton.question',),
        ),
        migrations.CreateModel(
            name='SliderResponse',
            fields=[
                ('questionresponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spoton.QuestionResponse')),
                ('answer', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('spoton.questionresponse',),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='spoton.Quiz')),
            ],
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='spoton.Response'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='spoton.Quiz'),
        ),
        migrations.CreateModel(
            name='ChoiceResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picks', to='spoton.Choice')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='spoton.CheckboxResponse')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='spoton.CheckboxQuestion'),
        ),
    ]
