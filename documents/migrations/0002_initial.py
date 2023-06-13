# Generated by Django 4.2.1 on 2023-05-28 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='receivers',
            field=models.ManyToManyField(related_name='received_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_documents', to=settings.AUTH_USER_MODEL),
        ),
    ]