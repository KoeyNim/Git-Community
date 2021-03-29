from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

import urllib
import os
from django.http import HttpResponse, Http404

# 내용 출력
def QuestionDetail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    session_cookie = request.user
    cookie_name = f'question_hits:{session_cookie}'

    response = render(request, 'QnA/question_detail.html', {'question': question})

    # 조회수 GET증가 방지 쿠키처리
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(question_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{question_id}', expires=None)
            question.hits += 1
            question.save()
            return response


    else:
        response.set_cookie(cookie_name, question_id, expires=None)
        question.hits += 1
        question.save()
        return response
    return response

# 목록 출력
def QuestionList(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 값이 없을경우 디폴트 값은 1
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬하여 조회
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색 대소문자 구분 x (subject__contains=kw : 대소문자 구분)
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'QnA/question_list.html', context)

# 질문 등록
@login_required(login_url='login:login')
def QuestionCreate(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('myweb:QList')
    else:
        form = QuestionForm
    return render(request, 'QnA/question_create.html', {'form': form})

# 질문 수정
@login_required(login_url='login:login')
def QuestionModify(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myweb:QDetail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('myweb:QDetail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'QnA/question_create.html', context)

# 질문 삭제
@login_required(login_url='login:login')
def QuestionDelete(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myweb:QDetail', question_id=question.id)
    question.delete()

    return redirect('myweb:QList')

# 파일 다운로드
@login_required(login_url='login:login')
def QuestionFileDownload(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    url = question.upload_file.url[1:]

    if os.path.exists(url):
        with open(url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(question.file_subject.encode('utf-8'))
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404