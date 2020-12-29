from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Notice, Question, Answer, Movie, Game

# 공지사항 추천 등록
@login_required(login_url='login:login')
def VoteNotice(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user == notice.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        notice.voter.add(request.user)
    return redirect('myweb:NoDetail', notice_id=notice.id)

# 질문 추천 등록
@login_required(login_url='login:login')
def VoteQusetion(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('myweb:QDetail', question_id=question.id)

# 답변 추천 등록
@login_required(login_url='login:login')
def VoteAnswer(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('myweb:QDetail', question_id=answer.question.id)

# 영화 추천 등록
@login_required(login_url='login:login')
def VoteMovie(request, movie_id):

    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        movie.voter.add(request.user)
    return redirect('myweb:MoDetail', movie_id=movie.id)

# 게임 추천 등록
@login_required(login_url='login:login')
def VoteGame(request, game_id):

    game = get_object_or_404(Game, pk=game_id)
    if request.user == game.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        game.voter.add(request.user)
    return redirect('myweb:GDetail', game_id=game.id)

