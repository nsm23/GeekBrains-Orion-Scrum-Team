from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.shortcuts import get_object_or_404

from .models import Moderation
from users.models import User


def moderation_action_create(moderator_user_id: int, decision: Moderation.ModerationDecision, model: Type[Model],
                             object_id: int) -> Moderation:
    moderation = Moderation(
        moderator_id=moderator_user_id,
        decision=decision,
        content_type=ContentType.objects.get(model.__name__.lower()),
        object_id=object_id,
    )
    moderation.save()
    return moderation


def moderation_users_ban(moderator_user_id: int, user_id: int) -> None:
    user = get_object_or_404(User, id=user_id)
    user.is_banned = True
    user.save()
    moderation_action_create(moderator_user_id, Moderation.ModerationDecision.BAN, User, user_id)


def moderation_users_unban(moderator_user_id: int, user_id: int) -> None:
    user = get_object_or_404(User, id=user_id)
    user.is_banned = False
    user.save()
    moderation_action_create(moderator_user_id, Moderation.ModerationDecision.UNBAN, User, user_id)
