from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'musicRecomender'
urlpatterns = [
    path('', view=indexView, name='index'),
    path('recommend', view=recommendView, name='recommend'),
    path('songlist', view=songListView, name='songlist')

]
