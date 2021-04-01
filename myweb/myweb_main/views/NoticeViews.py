from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..forms import NoticeForm
from ..models import Notice

import urllib
import os
from django.http import HttpResponse, Http404

# 내용 출력
def NoticeDetail(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    session_cookie = request.user
    cookie_name = f'notice_hits:{session_cookie}'

    response = render(request, 'Notice/notice_detail.html', {'notice': notice})

    # 조회수 GET증가 방지 쿠키처리
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(notice_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{notice_id}', expires=None)
            notice.hits += 1
            notice.save()
            return response

    else:
        response.set_cookie(cookie_name, notice_id, expires=None)
        notice.hits += 1
        notice.save()
        return response
    return response

# 목록 출력
def NoticeList(request):

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 값이 없을경우 디폴트 값은 1
    kw = request.GET.get('kw', '')  # 검색어

    notice_list = Notice.objects.order_by('-create_date')

    # 검색
    if kw:
        notice_list = notice_list.filter(
            Q(subject__icontains=kw) |  # 제목검색 대소문자 구분 x (subject__contains=kw : 대소문자 구분)
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) # 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(notice_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'notice_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'Notice/notice_list.html', context)

# 등록
@login_required(login_url='login:login')
def NoticeCreate(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            if request.FILES:
                if 'upload_file' in request.FILES.keys():
                    notice.file_subject = request.FILES['upload_file'].name
            notice.create_date = timezone.now()
            notice.save()
            return redirect('myweb:NoList')
    else:
        form = NoticeForm
    return render(request, 'Post/post_create.html', {'form': form})

# 수정
@login_required(login_url='login:login') # 로그인 상태 확인
def NoticeModify(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myweb:NoDetail', notice_id=notice.id)

    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            if request.FILES:
                if 'upload_file' in request.FILES.keys():
                    notice.file_subject = request.FILES['upload_file'].name
            notice.modify_date = timezone.now()
            notice.save()
            return redirect('myweb:NoDetail', notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'Post/post_create.html', {'form': form})

# 삭제
@login_required(login_url='login:login')
def NoticeDelete(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myweb:NoDetail', notice_id=notice.id)
    notice.delete()

    return redirect('myweb:NoList')

# 파일 다운로드
@login_required(login_url='login:login')
def NoticeFileDownload(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    url = notice.upload_file.url[1:]

    if os.path.exists(url):
        with open(url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(notice.file_subject.encode('utf-8'))
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404