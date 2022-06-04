# Generated by Django 4.0.5 on 2022-06-03 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterProfilePic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('local_path', models.TextField()),
                ('has_rainbow', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('twitter_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitterbot.twitteruser')),
            ],
        ),
        migrations.DeleteModel(
            name='TwitterProfilePics',
        ),
    ]