from django.shortcuts import render, get_object_or_404
from posts.models import Post
from hub.models import Hub


def hub_view(request, slug):
    hub = get_object_or_404(Hub, alias=slug)

    post_list = Post.objects.filter(hub__alias=slug).order_by('-created_at')
    context = {'post_list': post_list, 'slug': slug, 'page_title': 'Хаб | ' + hub.title}
    return render(request, '../templates/hub/index.html', context=context)
