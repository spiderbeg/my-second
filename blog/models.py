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


	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments', default=True)
	post1 = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comment_comment', default=True)#可以不要
	author2 = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=True)
	author1 = models.CharField(max_length=200)
	talk = models.TextField()
	published_date1 = models.DateTimeField(
		default=timezone.now)
	approved_commment = models.BooleanField(default=False)

	def approve(self):
		self.approved_commment = True
		self.save()

	def __str__(self):
		return self.talk
