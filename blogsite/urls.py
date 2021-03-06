"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth.views import LogoutView
from blogapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/login/$', views.CustomLoginView.as_view(), name="login"),
    url(r'^accounts/logout/$', views.CustomLogoutView.as_view(next_page="/"), name="logout"),

    url(r'^$', views.ArticleListView.as_view(), name="article-list"),
    url(r'^article/create/', views.ArticleCreateView.as_view(), name="article-create"),
    url(r'^article/(?P<pk>\d+)/edit/', views.ArticleUpdateView.as_view(), name="article-update"),
    url(r'^article/(?P<pk>\d+)/', views.ArticleDetailView.as_view(), name="article-detail"),






]
