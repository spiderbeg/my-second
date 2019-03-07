from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Votes
from .forms import PostForm, Comment1Form

#尝试
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#------------POST------------------------------------------------------------
def post_list(request):#文章列表
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views')# - 表示反排从大到小排序，
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):#内容详细页面，每打开一次post需要调用一次detail函数
	post = get_object_or_404(Post, pk=pk)#pk主键
	post.increase_views()#调用post模型中的increase_views函数记录阅读量
	vote1 = Votes.objects.filter(status=True,post=pk).count()#在一篇文章下的点赞数量
	return render(request, 'blog/post_detail.html', {'post':post,'vote1':vote1})#第三个参数为传递进模板的参数

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

def post_edit(request, pk):#文章编辑功能。从urls里传递了一个额外的pk参数。
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)#用实例来传递这篇文章
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)#当我们只是想打开文章编辑时
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


#----------signup------------------------------------------------------------

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


#----------------comment---------------------------------------------

def add_comment_to_post(request, pk):#对文章增加评论
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Comment1Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post#文章标题
            comment.author2 = request.user#请求的使用者设置为当前评论作者
            #print(comment.post)
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = Comment1Form()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_remove(request, pk):#删除评论
	comment = get_object_or_404(Comment,pk=pk)
	comment.delete()
	return redirect('blog:post_detail', pk=comment.post.pk)

#------点赞---------------------------------------------
def vote(request, pk):#文章点赞,pk为文章传入的即POST模型中的pk
	post1 = get_object_or_404(Post, pk=pk)
	#vote = post1.votes.all()
	if request.user.is_authenticated:#不要轻易删除数据库记录，对数据库性能影响较大
		#print("判断用户是否存在")
		vote1,c = post1.votes.get_or_create(author3=request.user, post=post1.pk,)#post=post1.pk与post=post1，区别
		if c == True:
			#print("被创建")
			return redirect('blog:post_detail',pk=pk)
		elif c==False and vote1.status == True:
			#print("早就有了,变化消极状态")
			vote1.status = False
			vote1.save(update_fields=['status'])#修改一个字段
			return redirect('blog:post_detail', pk=pk)
		else:
			#print("早就有了，变化积极状态")
			vote1.status = True
			vote1.save(update_fields=['status'])
			return redirect('blog:post_detail', pk=pk)
			
	else:
		return redirect('blog:signup')

'''点赞的另一种实现
		vote1,c = post1.votes.get_or_create(author3=request.user, post=post1.pk,)#post=post1.pk与post=post1，区别
		if c == True:
			print("被创建")
			return redirect('blog:post_detail',pk=pk)
		else:
			print("早就有了")
			vote1.delete()
			return redirect('blog:post_detail', pk=pk)

'''	
"""
When you access user.details, it accesses the backreference of the UserDetail.user foreign key. The foreign Key itself doesn't specify that a 
User can only have one UserDetail, so django gives you a RelatedManager, which you can filter and query just like a regular Manager. So you do 
the same things to it that you do to your .objects managers. You can ask for user.details.all(), user.details.filter(), user.details.get(), and 
so on, which will either give you a queryset, an object, or an exception,depending on the method and the results.
"""



