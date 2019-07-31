"""DASTP URL Configuration

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
from . import views

urlpatterns = [

	#=====url for get all images from gallery =====#
	path('gallery', views.GalleryAll.as_view(), name='GalleryAll'),
	#=====url for get all news =====#
	path('news',views.NewAll.as_view(),name='NewAll'),
	#=====url for get all news =====#
	path('anews/',views.NewsOne.as_view(),name='NewsOne'),

]
