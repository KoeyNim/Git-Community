from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import MovieForm
from ..models import Movie

import urllib
import os
from django.http import HttpResponse, Http404

# 내용 출력
def MovieDetail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    session_cookie = request.user
    cookie_name = f'movie_hits:{session_cookie}'

    response = render(request, 'Movie/movie_detail.html', {'movie': movie})

    # 조회수 GET증가 방지 쿠키처리
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(movie_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{movie_id}', expires=None)
            movie.hits += 1
            movie.save()
            return response

    else:
        response.set_cookie(cookie_name, movie_id, expires=None)
        movie.hits += 1
        movie.save()
        return response
    return response

# 목록 출력
def MovieList(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 값이 없을경우 디폴트 값은 1
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬하여 조회
    if so == 'recommend':
        movie_list = Movie.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        movie_list = Movie.objects.annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:  # recent
        movie_list = Movie.objects.order_by('-create_date')

    # 검색
    if kw:
        movie_list = movie_list.filter(
            Q(subject__icontains=kw) |  # 제목검색 대소문자 구분 x (subject__contains=kw : 대소문자 구분)
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) # 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(movie_list, 8)  # 페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'movie_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'Movie/movie_list.html', context)

# 등록
@login_required(login_url='login:login')
def MovieCreate(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            if request.FILES: # 파일 등록
                if 'upload_file' in request.FILES.keys():
                    movie.file_subject = request.FILES['upload_file'].name
            movie.create_date = timezone.now()
            movie.save()
            return redirect('myweb:MoList')
    else:
        form = MovieForm
    return render(request, 'Post/post_create.html', {'form': form})

# 수정
@login_required(login_url='login:login')
def MovieModify(request, movie_id):

    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user != movie.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myweb:MoDetail', movie_id=movie.id)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            if request.FILES:
                if 'upload_file' in request.FILES.keys():
                    movie.file_subject = request.FILES['upload_file'].name
            movie.modify_date = timezone.now()
            movie.save()
            return redirect('myweb:MoDetail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'Post/post_create.html', {'form': form})

# 삭제
@login_required(login_url='login:login')
def MovieDelete(request, movie_id):

    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user != movie.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myweb:MoDetail', movie_id=movie.id)
    movie.delete()
    return redirect('myweb:MoList')

# 파일 다운로드
@login_required(login_url='login:login')
def MovieFileDownload(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    url = movie.upload_file.url[1:]

    if os.path.exists(url):
        with open(url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(movie.file_subject.encode('utf-8'))
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404