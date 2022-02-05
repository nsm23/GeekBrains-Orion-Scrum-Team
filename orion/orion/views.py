from django.shortcuts import render

from posts.models import Post


def main_view(request):
    post_list = Post.objects.order_by('created_at')[:12]
    context = {'post_list': post_list}
    return render(request, '../templates/index.html', context=context)
