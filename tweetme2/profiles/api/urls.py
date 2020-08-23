from django.urls import path, re_path
from .views import (user_follow_view,)

from django.views.generic import TemplateView

'''

CLIENT
BASE ENDPOINT /api/profiles/

'''

urlpatterns = [
    path('<str:username>/follow/', user_follow_view),
]
