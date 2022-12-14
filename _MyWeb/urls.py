"""_MyWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path('^$', views.index),
    path('crawler/', views.crawler, name="crawler"),
    path('crawler/<int:page>/', views.crawler, name="crawler"),
    path('students/', views.students),
    path('cifar10/', views.cifar10),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__', include(debug_toolbar.urls)))
