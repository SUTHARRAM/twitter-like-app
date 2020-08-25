import random
from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetQuerySet(models.QuerySet):
    def feed(self, user):
        profiles_exists = user.following.exists()
        followed_users_id = []
        if profiles_exists:
            followed_users_id = user.following.values_list("user_id", flat=True) #[x.user.id for x in profiles]
        return self.filter(
        Q(user__id__in=followed_users_id) |
        Q(user=user)
        ).distinct().order_by("-timestamp")


class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='tweets') # many users can many tweets
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='image/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ['-id'] # '-' means that all tweets are in deacending order!
    
    @property
    def is_retweet(self):
        return self.parent != None

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,300)
        }

