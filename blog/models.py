from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Post(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)#关联auth.User表格
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(
		default=timezone.now)
	published_date = models.DateTimeField(
		blank=True, null=True)
	views = models.PositiveIntegerField(default=0)
	vote = models.PositiveIntegerField(default=0)

	def increase_views(self):#记录阅读量的方法,也可在视图写函数实现此功能
		self.views += 1 #访问文章即调用 Post 模型
		self.save(update_fields=['views'])#告诉数据库只更新views的值

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def approved_comment(self):
		return self.comments.filter(approved_comment=True)


class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments', default=True)#models.ForeignKey中的related_name选项允许我们在Post模型中连接 comments，即对应Post模型主键
	author2 = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=True)
	author1 = models.CharField(max_length=200)
	talk = models.TextField()
	published_date1 = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.talk

class Votes(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='votes')
	author3 = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	vote = models.PositiveIntegerField(default=0)
	status = models.BooleanField(default=True)
	published_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.author3.username#不能返回一个对象