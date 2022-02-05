from django.shortcuts import render
from posts.models import Post


def hub_view(request, slug):
    post_list = Post.objects.filter(hub__alias=slug).order_by('-created_at')
    context = {'post_list': post_list, 'slug': slug}
    return render(request, '../templates/hub/index.html', context=context)
