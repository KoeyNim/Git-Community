from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..forms import NoticeForm
from ..models import Notice

# 내용 출력
def NoticeDetail(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    context = {'notice': notice}
    return render(request, 'Notice/notice_detail.html', context)

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
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.create_date = timezone.now()
            notice.save()
            return redirect('myweb:NoList')
    else:
        form = NoticeForm
    return render(request, 'Notice/notice_create.html', {'form': form})

# 수정
@login_required(login_url='login:login') # 로그인 상태 확인
def NoticeModify(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myweb:NoDetail', notice_id=notice.id)

    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.modify_date = timezone.now()
            notice.save()
            return redirect('myweb:NoDetail', notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)
    context = {'form': form}
    return render(request, 'Notice/notice_create.html', context)

# 삭제
@login_required(login_url='login:login')
def NoticeDelete(request, notice_id):

    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myweb:NoDetail', notice_id=notice.id)
    notice.delete()

    return redirect('myweb:NoList')