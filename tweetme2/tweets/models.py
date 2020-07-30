import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # many users can many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='image/', blank=True, null=True)

    class Meta:
        ordering = ['-id'] # '-' means that all tweets are in deacending order!
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,300)
        }

