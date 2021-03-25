from django import forms
from .models import Notice, Question, Answer, Comment, Movie, Game

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice # Notice 모델과 연결
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변 내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용',
        }

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['subject', 'content', 'upload_file']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['subject', 'content', 'upload_file']
        labels = {
            'subject': '제목',
            'content': '내용',
        }
