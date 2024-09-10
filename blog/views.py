from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse 
from django.http import JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
 
from .models import Post, Comment
from .forms import CommentForm


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


class BlogDetail(DetailView, View):
    model = Post
    template_name = "blog/blog_detail.html"
    paginate_comments_by = 5  # Number of comments per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['previous_post'] = Post.objects.filter(publish__lt=post.publish).order_by('-updated').first()
        context['next_post'] = Post.objects.filter(publish__gt=post.publish).order_by('updated').first()
        
        # Get top-level comments ordered by creation date (newest first)
        comments = post.comment_set.filter(parent=None).order_by('-created_at')  # Order by created_at descending
        paginator = Paginator(comments, self.paginate_comments_by)  # Create a paginator
        page_number = self.request.GET.get('page')  # Get the page number from the request
        page_obj = paginator.get_page(page_number)  # Get the comments for the current page

        context['comments'] = page_obj
        context['page_obj'] = page_obj  # Pass the page object to the template
        context['form'] = CommentForm()

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data(object=self.object)
            comments_html = render_to_string('blog/comments_list.html', context)
            return JsonResponse({'comments_html': comments_html, 'has_next': context['page_obj'].has_next()})
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user  # Set the author to the logged-in user
            comment.save()
            return JsonResponse({
                'author': comment.author.username,
                'comment': comment.comment,
                'created_at': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
                'parent': comment.parent.id if comment.parent else None,
                'profile_image': comment.author.profile.profile_image.url,  # Assuming you have a Profile model
            })
        return JsonResponse({'errors': form.errors}, status=400)




class BlogCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_new.html"
    fields = ["title", "body", "cover", "tags"]

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to create a post.")
        return super().dispatch(request, *args, **kwargs)

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


class CommentGet(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

	
class CommentPost(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return JsonResponse({
                'author': comment.author,
                'comment': comment.comment,
                'created_at': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
            })
        return JsonResponse({'errors': form.errors}, status=400)


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'blog/comment_edit.html'  # Create this template

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.post.slug})


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'  # Create this template


    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.post.slug})	

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
