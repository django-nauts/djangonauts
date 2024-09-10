from django.urls import path
from .views import (
	BlogList,
	BlogDetail,
	BlogCreate,
	BlogUpdate,
	BlogDelete,
	BlogCategory,
	AboutPage,
	CommentUpdate,
	CommentDelete
)

app_name = 'blog'


urlpatterns = [
    path('', BlogList.as_view(), name='blog_list'),
	path('<slug:slug>', BlogDetail.as_view(), name='blog_detail'),
	path("post/new/", BlogCreate.as_view(), name="post_new"),
	path("post/<slug:slug>/update/", BlogUpdate.as_view(), name="post_edit"),
	path("post/<slug:slug>/delete/", BlogDelete.as_view(), name="post_delete"),
	path('post/<slug:tag_slug>/', BlogCategory.as_view(), name='blog_category'),
	path("about/", AboutPage.as_view(), name="about"),
    path('comment/<int:pk>/edit/', CommentUpdate.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),	
]
