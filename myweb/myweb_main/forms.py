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
        model = Question # Question 모델과 연결
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer # Answer 모델과 연결
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # Comment 모델과 연결
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie # Moive 모델과 연결
        fields = ['subject', 'content', 'upload_file']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game  # Game 모델과 연결
        fields = ['subject', 'content', 'upload_file']
        labels = {
            'subject': '제목',
            'content': '내용',
        }
