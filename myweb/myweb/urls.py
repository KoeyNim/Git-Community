from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('', include('myweb_main.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('social-login/', include('allauth.urls')),

]