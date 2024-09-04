from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post


class BlogList(ListView):
    model = Post
    template_name = "blog/blog_list.html"
    paginate_by = 5


class BlogCategory(ListView):
    model = Post
    template_name = "blog/blog_category.html"
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)


class BlogDetail(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['previous_post'] = Post.objects.filter(publish__lt=post.publish).order_by('-updated').first()
        context['next_post'] = Post.objects.filter(publish__gt=post.publish).order_by('updated').first()

        return context


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_new.html"
    fields = ["title", "body", "cover", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_edit.html"
    fields = ["title", "slug", "body", "cover", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:blog_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class AboutPage(TemplateView):
    template_name = "blog/about.html"
