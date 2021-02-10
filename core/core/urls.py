"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import routers
from movie import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('movies/', views.GetMoviesView.as_view(), name="movies"),
    path('register/',views.UserRegisterView.as_view(),name="user-register"),
    path('collection/',views.CollectionView.as_view(),name="collection"),
    path('collection/<uuid:collection_uuid>/',views.CrudCollectionView.as_view(),name='collection-details'),
    path('request-count/',views.RequestCountView.as_view(), name="req-count"),
    path('request-count/reset/',views.ResetView.as_view(), name="reset"),
]