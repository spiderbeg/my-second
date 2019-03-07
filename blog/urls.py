from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('<int:pk>/', views.post_detail, name='post_detail'),
	path('new/', views.post_new, name='post_new'),
	path('<int:pk>/edit', views.post_edit, name='post_edit'),
	path('drafts/', views.post_draft_list, name='post_draft_list'),
	path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
	path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
	path('post/<int:pk>/remove/drafts/', views.post_remove_draft, name='post_remove_draft'),
	path('signup/', views.signup, name='signup'),
	path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
	#path('post/<int:pk>/comment_to/', views.add_comment_to_comment, name='add_comment_to_comment'),
	path('post/<int:pk>/comment/remove/', views.comment_remove, name='comment_remove'),
	path('post/<int:pk>/comment/vote/', views.vote, name='vote'),
]