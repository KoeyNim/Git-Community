from django.contrib import admin
from .models import Question, Answer, Notice, Movie, Game, Comment
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

# admin 페이지에 관리, 검색 추가
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Notice)
admin.site.register(Movie)
admin.site.register(Game)
admin.site.register(Comment)