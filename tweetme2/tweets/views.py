import random
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    print("User that attach to each Request : ",request.user or None)
    data = {
        "name": "Ram",
        "new_arr": {
            "1": 1,
            "2": 2,
            "3": 3,
        }
    }
    return render(request,'pages/home.html', context=data)

def tweets_list_view(request, *args, **kwargs):
    
    return render(request, "tweets/list.html")

def tweets_detail_view(request, tweet_id, *args, **kwargs):
    
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})


def tweets_profile_view(request, username, *args, **kwargs):
    
    return render(request, "tweets/profile.html", context={"profile_username": username}, status=200)

