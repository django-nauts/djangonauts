from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post


class BlogList(ListView):
    model = Post
    template_name = "blog/blog_list.html"


class BlogDetail(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"


class BlogCreate(CreateView):
    model = Post
    template_name = "blog/post_new.html"
    fields = ["title", "author", "body", "slug"]


class BlogUpdate(UpdateView):
    model = Post
    template_name = "blog/post_edit.html"
    fields = ["author", "title", "slug", "body"]


class BlogDelete(DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:blog_list")
