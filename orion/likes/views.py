import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View

from likes.models import LikeDislike
from notifications.models import Notification
from posts.models import Post


class VotesView(View):
    model = Post
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        if self.request.user.id == obj.user.id:
            return
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                                  object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                Notification.create_notification(ContentType.objects.get(model='likedislike'), likedislike.id)
                result = True
            else:
                likedislike.delete()
                Notification.delete_notification(ContentType.objects.get(model='likedislike'), likedislike.id)
                result = False
        except ObjectDoesNotExist:
            likedislike = obj.votes.create(user=request.user, vote=self.vote_type)
            Notification.create_notification(ContentType.objects.get(model='likedislike'), likedislike.id)
            result = True
        return HttpResponse(
            json.dumps(
                {
                    "result": result,
                    "like_count": obj.votes.likes().count(),
                    "dislike_count": obj.votes.dislikes().count(),
                    "sum_rating": obj.votes.sum_rating(),
                }
            )
        )
