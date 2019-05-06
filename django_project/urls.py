"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app import view

# url实例列表
# url对象：正则表达式、视图名称
urlpatterns = [
    path('admin/', admin.site.urls),

    url('^$', view.index),
    url('^index/', view.index),
    url('^get_songs/', view.get_songs),
    url('^search_songs/', view.search_songs),
    #url('^$', view.get_songs),

    #url('^index_emotion_init/', view.index_emotion_init),
    url('^index_emotion/', view.index_emotion),
    url('^recommend_songs/', view.recommend_songs),
    url('^get_url/', view.get_url),
    url('^return_emotion/', view.return_emotion),
    #url('^index_emotion/', view.index_emotion),








]
