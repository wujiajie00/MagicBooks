
# Create your models here.
from django.db import models
from mdeditor.fields import MDTextField


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    content = MDTextField(verbose_name='内容')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name