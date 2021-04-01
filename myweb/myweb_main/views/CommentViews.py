from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment, Movie, Game


# 질문 댓글 등록
@login_required(login_url='login:login')
def CommentCreateQuestion(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # 중복 DB 저장을 방지
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:QDetail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'question': question, 'form': form}
    return render(request, 'QnA/question_detail.html', context)

# 질문 댓글 수정
@login_required(login_url='login:login')
def CommentModifyQuestion(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('myweb:QDetail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:QDetail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'Modify/modify_Answer_comment.html', context)

# 질문 댓글 삭제
@login_required(login_url='login:login') # 로그인 상태 확인
def CommentDeleteQuestion(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('myweb:QDetail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('myweb:QDetail', question_id=comment.question_id)

# 영화 댓글 등록
@login_required(login_url='login:login')
def CommentCreateMovie(request, movie_id):

    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.movie = movie
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:MoDetail', movie_id=comment.movie.id), comment.id))
    else:
        form = CommentForm()
    context = {'movie': movie, 'form': form}
    return render(request, 'Movie/movie_detail.html', context)

# 영화 댓글 수정
@login_required(login_url='login:login')
def CommentModifyMovie(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('myweb:MoDetail', movie_id=comment.movie.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:MoDetail', movie_id=comment.movie.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'Modify/modify_Answer_comment.html', {'form': form})

# 영화 댓글 삭제
@login_required(login_url='login:login')
def CommentDeleteMovie(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('myweb:MoDetail', movie_id=comment.movie.id)
    else:
        comment.delete()
    return redirect('myweb:MoDetail', movie_id=comment.movie.id)


# 게임 댓글 등록
@login_required(login_url='login:login')
def CommentCreateGame(request, game_id):

    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.game = game
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:GDetail', game_id=comment.game.id), comment.id))
    else:
        form = CommentForm()
    context = {'game': game, 'form': form}
    return render(request, 'Game/game_detail.html', context)

# 게임 댓글 수정
@login_required(login_url='login:login')
def CommentModifyGame(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('myweb:GDetail', game_id=comment.game.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('myweb:GDetail', game_id=comment.game.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'Modify/modify_Answer_comment.html', context)

# 게임 댓글 삭제
@login_required(login_url='login:login')
def CommentDeleteGame(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('myweb:GDetail', game_id=comment.game.id)
    else:
        comment.delete()
    return redirect('myweb:GDetail', game_id=comment.game.id)
