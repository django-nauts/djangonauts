from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='images/', default='default.jpg')
    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    body = models.TextField(blank=False, null=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
