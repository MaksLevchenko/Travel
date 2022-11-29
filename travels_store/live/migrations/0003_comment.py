# Generated by Django 4.1.3 on 2022-11-27 08:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('live', '0002_remove_post_tag_post_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_data', models.DateTimeField(default=datetime.datetime(2022, 11, 27, 8, 29, 26, 254325, tzinfo=datetime.timezone.utc))),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='live.post')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_data'],
            },
        ),
    ]