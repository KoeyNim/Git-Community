from django.contrib import admin
from .models import Question, Answer, Notice, Movie, Game, Comment
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin) # admin 페이지에 Question 관리, 검색 추가
admin.site.register(Answer) # admin 페이지에 Answer 관리 추가
admin.site.register(Notice) # admin 페이지에 Notice 관리 추가
admin.site.register(Movie) # admin 페이지에 Movie 관리 추가
admin.site.register(Game) # admin 페이지에 Game 관리 추가
admin.site.register(Comment) # admin 페이지에 Comment 관리 추가