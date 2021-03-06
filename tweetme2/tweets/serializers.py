from django.conf import settings

from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    '''
    This is the serializer for tweet actions
    '''
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        if not value in TWEET_ACTION_OPTIONS:
            value = value.lower().strip()  # "Like " --> "like"
            raise serializers.ValidationError("This is not a valid action for tweets.")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['user', 'id','content','likes', 'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()
        
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long.")
        return value



class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    og_tweet = TweetCreateSerializer(source='parent' ,read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'likes', 'is_retweet', 'og_tweet', 'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()

    # def get_user(self, obj):
    #     return obj.user.id
   
        