# Generated by Django 2.1.2 on 2018-11-09 16:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookType', models.CharField(choices=[('雑誌', '雑誌'), ('新書', '新書'), ('参考書', '参考書'), ('漫画', '漫画')], default='雑誌', max_length=3, verbose_name='本種')),
                ('name', models.CharField(max_length=255, verbose_name='書籍名')),
                ('publisher', models.CharField(blank=True, max_length=255, verbose_name='出版社')),
                ('page', models.IntegerField(blank=True, default=0, verbose_name='ページ数')),
                ('impressionCount', models.IntegerField(blank=True, default=0, verbose_name='感想数')),
                ('total_readCount', models.IntegerField(blank=True, default=0, verbose_name='総読書回数')),
                ('editer', models.CharField(blank=True, max_length=255, verbose_name='登録者')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Impression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='コメント')),
                ('readCount', models.IntegerField(blank=True, default=0, verbose_name='読書回数')),
                ('editer', models.CharField(blank=True, max_length=255, verbose_name='登録者')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='impressions', to='ReadingRec.Book', verbose_name='書籍')),
            ],
        ),
    ]