from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)


class Comment1Form(forms.ModelForm):

	class Meta:#告诉django哪个模型使用这个表单
		model = Comment
		fields = ('author1', 'talk',)

			