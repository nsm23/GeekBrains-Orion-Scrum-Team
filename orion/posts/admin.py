from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'status', 'user']


admin.site.register(Post, PostAdmin)
