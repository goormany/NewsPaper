from django.contrib import admin
from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'authorUser', 'raitingAuthor')
    list_display_links = ('id', 'authorUser',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    save_as = True


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_choice', 'author', 'dateCreation', 'raitingPost')
    list_display_links = ('id', 'title',)
    list_filter = ('category_choice',)
    search_fields = ('title',)
    inlines = [CommentInlineAdmin]
    save_on_top = True
    save_as = True
    list_editable = ('category_choice',)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'postTrough', 'categoryTrough')
    list_display_links = ('id', 'postTrough',)


@admin.register(Comment)
class CommentAdminInline(admin.ModelAdmin):
    list_display = ('id', 'commentPost', 'commentUser', 'DateCreation', 'raitingComment')
    list_display_links = ('id', 'commentPost', )


