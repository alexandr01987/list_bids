# Generated by Django 2.2.3 on 2019-08-02 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solvo_support', '0002_requestsolvo_is_defect_registered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errorsolvo',
            old_name='status_error',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='revisionsolvo',
            old_name='status_revision',
            new_name='status',
        ),
    ]