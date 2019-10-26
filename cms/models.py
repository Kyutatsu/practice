from django.db import models


class Book(models.Model):
    """書籍"""
    name = models.CharField(
            verbose_name='書籍名', max_length=255
    )
    publisher = models.CharField(
            verbose_name='出版社', max_length=255
    )
    page = models.IntegerField(
            verbose_name='ページ数', blank=True, default=0
    )

    def __str__(self):
        return self.name


class Impression(models.Model):
    """感想"""
    book = models.ForeignKey(
            Book, verbose_name='書籍',
            on_delete=models.CASCADE, related_name='impressions'
    )
    comment = models.TextField(
            verbose_name='コメント', blank=True
    )

    def __str__(self):
        return self.comment
