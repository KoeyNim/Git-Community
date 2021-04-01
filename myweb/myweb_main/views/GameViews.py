from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import GameForm
from ..models import Game

import urllib
import os
from django.http import HttpResponse, Http404

# 내용 출력
def GameDetail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    session_cookie = request.user
    cookie_name = f'game_hits:{session_cookie}'

    response = render(request, 'Game/game_detail.html', {'game': game})

    # 조회수 GET증가 방지 쿠키처리
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(game_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{game_id}', expires=None)
            game.hits += 1
            game.save()
            return response

    else:
        response.set_cookie(cookie_name, game_id, expires=None)
        game.hits += 1
        game.save()
        return response
    return response

# 목록 출력
def GameList(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 값이 없을경우 디폴트 값은 1
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬하여 조회
    if so == 'recommend':
        game_list = Game.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        game_list = Game.objects.annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:  # recent
        game_list = Game.objects.order_by('-create_date')

    # 검색
    if kw:
        game_list = game_list.filter(
            Q(subject__icontains=kw) |  # 제목검색 대소문자 구분 x (subject__contains=kw : 대소문자 구분)
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) # 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(game_list, 8)  # 페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'game_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'Game/game_list.html', context)

# 등록
@login_required(login_url='login:login')
def GameCreate(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.author = request.user
            if request.FILES:
                if 'upload_file' in request.FILES.keys():
                    game.file_subject = request.FILES['upload_file'].name
            game.create_date = timezone.now()
            game.save()
            return redirect('myweb:GList')
    else:
        form = GameForm
    return render(request, 'Post/post_create.html', {'form': form})

# 수정
@login_required(login_url='login:login')
def GameModify(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.user != game.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myweb:GDetail', game_id=game.id)

    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            game = form.save(commit=False)
            game.author = request.user
            if request.FILES: # 파일 등록
                if 'upload_file' in request.FILES.keys():
                    game.file_subject = request.FILES['upload_file'].name
            game.modify_date = timezone.now()  # 수정일시 저장
            game.save()
            return redirect('myweb:GDetail', game_id=game.id)
    else:
        form = GameForm(instance=game)
    return render(request, 'Post/post_create.html', {'form': form})

# 삭제
@login_required(login_url='login:login')
def GameDelete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.user != game.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myweb:GDetail', movie_id=game.id)
    game.delete()
    return redirect('myweb:GList')

# 파일 다운로드
@login_required(login_url='login:login')
def GameFileDownload(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    url = game.upload_file.url[1:]

    if os.path.exists(url):
        with open(url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(game.file_subject.encode('utf-8'))
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404