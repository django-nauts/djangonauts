from django.urls import path
from .views import (
	BlogList,
	BlogDetail,
	BlogCreate,
	BlogUpdate,
	BlogDelete,
)

app_name = 'blog'


urlpatterns = [
    path('', BlogList.as_view(), name='blog_list'),
	path('<slug:slug>', BlogDetail.as_view(), name='blog_detail'),
	path("post/new/", BlogCreate.as_view(), name="post_new"),
	path("post/<slug:slug>/update/", BlogUpdate.as_view(), name="post_edit"),
	path("post/<slug:slug>/delete/", BlogDelete.as_view(), name="post_delete"),
]
