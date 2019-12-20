from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe  # 将字符串标记为安全进行输出
from markdown import markdown
from mdeditor.fields import MDTextField

# 用户信息
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, null=True,unique=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username


# 文章数据
class Article(models.Model):
    title = models.CharField(max_length=50)  # 标题
    user = models.ForeignKey(UserInfo)  # 用户
    # content = models.TextField(max_length=10000)  # 正文
    tags = models.ManyToManyField('Tag')  # 标签
    date = models.DateTimeField(auto_now_add=True)  # 发表日期
    content = MDTextField(null=True)  # 注意为MDTextField()
    def get_comment_text_md(self):
        # 将markdown格式转化为html
        return mark_safe(markdown(self.content))

    def __str__(self):
        return self.title


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
