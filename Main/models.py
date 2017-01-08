from django.db import models
from users.models import User
# Create your models here.
import django.utils.timezone as timezone
class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name='标签')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

class Category(models.Model):
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
    name = models.CharField(max_length=20,verbose_name='分类')
    def __str__(self):
        return self.name

class Record(models.Model):
    class Meta:
        verbose_name = '记录'
        verbose_name_plural = '记录'
    title = models.CharField(verbose_name='标题',max_length=100)
    source = models.URLField(verbose_name='原文链接')
    publish_time = models.DateTimeField(default = timezone.now,verbose_name='发布时间')
    receipt_time = models.DateTimeField(auto_now=True,verbose_name='收录时间')
    author = models.CharField(max_length=20,verbose_name='作者',default='')
    category = models.ForeignKey(Category,verbose_name='分类', default=1)
    keywords =models.TextField(verbose_name='关键词', default='')
    content = models.TextField(verbose_name='内容',default='')
    originalpage= models.TextField(verbose_name='原文',default='')
    likenum = models.IntegerField(verbose_name='喜欢',default=0)
    def __str__(self):
        return self.title

class Evaluate(models.Model):
    class Meta:
        verbose_name = '评价'
        verbose_name_plural = '评价'
    name = models.CharField(max_length=100,verbose_name='评头')
    tags = models.ManyToManyField(Tag, blank=True,verbose_name='标签集')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    content = models.TextField(verbose_name='点评内容')
    like =models.BooleanField(verbose_name='态度')
    recorder = models.ForeignKey( Record,verbose_name='记录')
    user = models.ForeignKey( User,verbose_name='评论人')
    def __str__(self):
        return self.name
