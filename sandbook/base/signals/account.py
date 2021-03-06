from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from base.models import User
from base.models.account import UserInfo


@receiver(post_save, sender=User)
def on_user_saved(sender, instance, **kwargs):
    if kwargs.get('created'):
        # 创建用户及作者信息
        UserInfo.objects.create(user=instance)
        # AuthorInfo.objects.create(user=instance)
    else:
        # update
        ...


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    # 检查是否为当天第一次登录
    past_time = timezone.now() - user.last_login
    if past_time.days > 1:
        # 增加经验值
        user_detail = user.userdetail
        user_detail.exp += 1
        user_detail.save()

# @receiver(user_logged_out)
# def on_user_logged_out(sender, request, user, **kwargs):
#     ...


# @receiver(user_login_failed)
# def on_user_login_failed(sender, credentials, request, **kwargs):
#     """
#     credentials: {'username': 'admin', 'password': '********************'}
#     """
#     # try:
#     #     user = User.objects.get(username=credentials['username'])
#     # except User.DoesNotExist:
#     #     pass
#     ...
