from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, Comment1Form

#尝试
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#------------------------------------------------------------
def post_list(request):#文章列表
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):#内容详细页面
	post = get_object_or_404(Post, pk=pk)#pk主键
	return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):#新建草稿并保存
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			#post.published_date = timezone.now()
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):#草稿列表
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):#文章发布
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog:post_detail', pk=pk)

def publish(self):#发布时间
	self.published_date = timezone.now()
	self.save()

@login_required
def post_remove(request, pk):#删除文章
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog:post_list')

@login_required
def post_remove_draft(request, pk): #删除草稿
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog:post_draft_list')


#-------------------------------------------------------
def signup(request):#用户注册
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('blog:post_list')
	else:
		form = UserCreationForm()
	return render(request, 'blog/signup.html', {'form':form})


#-------------------------------------------------------------
def add_comment_to_post(request, pk):#对文章增加评论
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Comment1Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post#文章标题
            #print(comment.post)
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = Comment1Form()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

'''
def add_comment_to_comment(request, pk):#对评论增加评论
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Comment1Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post1 = post#文章标题
            #print(comment.post)
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = Comment1Form()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
'''
#------------------------------------------------------------------------
'''
def comment(request):#写并保存评论
	#comment = get_object_or_404(Comment)
	if request.method == "POST":
		form1 = Comment1Form(request.POST)
		if form1.is_valid():
			comment = form1.save(commit=False)#commit=False表示还不想保存Comment1Post模型
			comment.author1 = request.user #作者
			comment.published_date1 = timezone.now()#时间
			comment.save()
			return redirect('blog:post_detail', pk=comment.pk)#------------------------------------------------------------如何解决主键不同的问题
	else:
		form1 = Comment1Form()
	

	return render(request, 'blog/comment_edit.html', {'form1': form1})
'''
