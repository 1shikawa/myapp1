from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

"""書籍"""
class Book(models.Model):

    book_choices = (
        ("雑誌", '雑誌'),
        ("新書", '新書'),
        ("参考書", '参考書'),
        ("漫画", '漫画'),
    )
    # id = models.AutoField(primary_key=True)
    bookType = models.CharField("本種", max_length=3, blank=False, choices=book_choices,default="雑誌")
    name = models.CharField('書籍名', max_length=255)
    publisher = models.CharField('出版社', max_length=255, blank=True)
    page = models.IntegerField('ページ数', blank=True, default=0)
    impressionCount = models.IntegerField('感想数', blank=True, default=0)
    total_readCount = models.IntegerField('総読書回数', blank=True, default=0)
    editer = models.CharField('登録者', max_length=255, blank=True)
    created_at = models.DateTimeField('登録日時', default=datetime.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True)  # 更新日時

    # updated_at = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     auto_now = kwargs.pop('updated_at_auto_now', True)
    #     if auto_now:
    #         self.updated_at = datetime.now()
    #     super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


"""感想"""
class Impression(models.Model):

    book = models.ForeignKey(Book, verbose_name='書籍', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField('コメント', blank=True)
    readCount = models.IntegerField('読書回数', blank=True, default=0)
    editer = models.CharField('登録者', max_length=255, blank=True)
    created_at = models.DateTimeField('登録日時',default=datetime.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True)  # 更新日時

    def __str__(self):
        return self.comment
