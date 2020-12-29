from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Question, Notice, Movie, Game

# home 화면 출력
def homeList(request):

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지 값이 없을경우 디폴트 값은 1

    HomeQnA_List = Question.objects.order_by('-create_date') # 조회 결과를 역순으로 정렬
    HomeNotice_List = Notice.objects.order_by('-create_date')
    HomeMovie_List = Movie.objects.order_by('-create_date')
    HomeGame_List = Game.objects.order_by('-create_date')

    # 페이징처리
    Paginator_QnA = Paginator(HomeQnA_List, 5)  # 페이지당 5개씩 보여주기
    Paginator_Notice = Paginator(HomeNotice_List, 5)
    Paginator_Movie = Paginator(HomeMovie_List, 5)
    Paginator_Game = Paginator(HomeGame_List, 5)

    Page_Obj_QnA = Paginator_QnA.get_page(page)
    Page_Obj_Notice = Paginator_Notice.get_page(page)
    Page_Obj_Movie = Paginator_Movie.get_page(page)
    Page_Obj_Game = Paginator_Game.get_page(page)

    context = {'homeQnA_list': Page_Obj_QnA, 'homeNotice_list': Page_Obj_Notice, 'homeMovie_list': Page_Obj_Movie, 'homeGame_list': Page_Obj_Game}
    return render(request, 'main/home.html', context)
