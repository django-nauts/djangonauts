from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms to display

class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_comment_type', 'author', 'is_approved', 'comment', 'post', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('comment',)
    actions = ['approve_comments']

    def display_comment_type(self, obj):
        return "Reply" if obj.parent else "Comment"
    display_comment_type.short_description = 'Type'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} comments approved.")
    approve_comments.short_description = "Approve selected comments"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish']
    list_filter = ['created', 'publish', 'author']
    search_fields = ['title', 'body']  # Changed 'comment' to 'body'
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['-updated']
    inlines = [CommentInline]  # Add this line

# Register the Comment model with the CommentAdmin class
admin.site.register(Comment, CommentAdmin)
