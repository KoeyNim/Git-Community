from django.contrib import admin
from .models import User, SocialUser

admin.site.register(User) # admin 페이지에 User 관리 추가
admin.site.register(SocialUser)
