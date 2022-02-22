from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string

from notifications.models import Notification
from .models import Comment
from .forms import CommentForm


class JsonableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax(request=self.request):
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.is_ajax(request=self.request) and self.request.method == "POST":
            if 'parent' in self.request.POST and int(self.request.POST['parent']) > 0:
                form.instance.parent = Comment.objects.get(pk=self.request.POST['parent'])

            self.object = form.save()
            if self.object.post.user.id != self.request.user.id:
                Notification().create_notification(ContentType.objects.get(model='comment'), self.object.id)

            if 'parent' in self.request.POST and int(self.request.POST['parent']) > 0:
                template = 'reply.html'
                context = {
                    "reply_comment": self.object
                }
            else:
                template = 'comment.html'
                context = {
                    "comment": self.object, 
                    "user": self.request.user, 
                    "post": self.object.post, 
                    "without_comment_form": True
                }
            
            html = render_to_string(f'comments/{template}', context)

            data = {
                'comment_id': self.object.id,
                'html': html,
                'status': 200
            }

            return JsonResponse(data)
        else:
            response = super(JsonableResponseMixin, self).form_valid(form)
            return response

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class CommentCreateView(JsonableResponseMixin, CreateView):
    model = Comment
    form_class = CommentForm
