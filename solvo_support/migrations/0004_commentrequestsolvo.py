# Generated by Django 2.2.3 on 2019-08-02 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solvo_support', '0003_auto_20190802_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentRequestSolvo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_to_request', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('request_solvo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='solvo_support.RequestSolvo')),
                ('user_creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
