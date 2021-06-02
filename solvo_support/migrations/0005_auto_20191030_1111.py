# Generated by Django 2.2.3 on 2019-10-30 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solvo_support', '0004_commentrequestsolvo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugsolvo',
            name='status',
            field=models.ForeignKey(default=3, limit_choices_to={'type_id': 3}, on_delete=django.db.models.deletion.PROTECT, to='solvo_support.Status'),
        ),
        migrations.AlterField(
            model_name='emailsolvo',
            name='sender',
            field=models.CharField(max_length=255),
        ),
    ]