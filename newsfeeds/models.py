from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet

class NewsFeed(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        unique_together = (('user', 'tweet'),)
        ordering = ('-created_at',)

    def __str__(self):
        # 这里是你执行 print(newsfeed instance) 的时候会显示的内容
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'