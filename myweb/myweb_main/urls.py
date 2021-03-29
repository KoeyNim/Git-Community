from django.urls import path
from .views import NoticeViews, QuestionViews, AnswerViews, CommentViews, VoteViews, HomeViews, MovieViews, GameViews

app_name = 'myweb'

urlpatterns = [

    # home 화면 url
    path('', HomeViews.homeList, name='home'),

    # 공지사항 url
    path('myweb-Notice/', NoticeViews.NoticeList, name='NoList'),
    path('myweb-Notice/<int:notice_id>/', NoticeViews.NoticeDetail, name='NoDetail'),
    path('myweb-Notice/NoCreate/', NoticeViews.NoticeCreate, name='NoCreate'),
    path('myweb-Notice/NoModify/<int:notice_id>/', NoticeViews.NoticeModify, name='NoModify'),
    path('myweb-Notice/NoDelete/<int:notice_id>/', NoticeViews.NoticeDelete, name='NoDelete'),

    # 질문 url
    path('myweb-QnA/', QuestionViews.QuestionList, name='QList'), # 질문 리스트
    path('myweb-Q/<int:question_id>/', QuestionViews.QuestionDetail, name='QDetail'), # 질문 상세
    path('myweb-Q/QCreate/', QuestionViews.QuestionCreate, name='QCreate'), # 질문 작성
    path('myweb-Q/QModify/<int:question_id>/', QuestionViews.QuestionModify, name='QModify'), # 질문 수정
    path('myweb-Q/QDelete/<int:question_id>/', QuestionViews.QuestionDelete, name='QDelete'), # 질문 삭제
    path('myweb-Q/download/<question_id>', QuestionViews.QuestionFileDownload, name="MoFileDownload"), # 파일

    # 답변 url
    path('myweb-A/ACreate/<int:question_id>/', AnswerViews.AnswerCreate, name='ACreate'), # 답변 작성
    path('myweb-A/AModify/<int:answer_id>/', AnswerViews.AnswerModify, name='AModify'), # 답변 수정
    path('myweb-A/ADelete/<int:answer_id>/', AnswerViews.AnswerDelete, name='ADelete'), # 답변 삭제

    # 질문 댓글 url
    path('myweb-Q/QCreate/Comment/<int:question_id>/', CommentViews.CommentCreateQuestion, name='CommentCreateQuestion'), # 댓글 등록 시 질문의 id인 question_id가 필요함
    path('myweb-Q/QModify/Comment/<int:comment_id>/', CommentViews.CommentModifyQuestion, name='CommentModifyQuestion'), # 수정이나 삭제 시에는 댓글의 id인 comment_id가 필요함
    path('myweb-Q/QDelete/Comment/<int:comment_id>/', CommentViews.CommentDeleteQuestion, name='CommentDeleteQuestion'),

    # 추천 url
    path('QVote/<int:question_id>/', VoteViews.VoteQusetion, name='QVote'),
    path('AVote/<int:answer_id>/', VoteViews.VoteAnswer, name='AVote'),
    path('NoVote/<int:notice_id>/', VoteViews.VoteNotice, name='NoVote'),
    path('MoVote/<int:movie_id>/', VoteViews.VoteMovie, name='MoVote'),
    path('GVote/<int:game_id>/', VoteViews.VoteGame, name='GVote'),

    # 영화 url
    path('myweb-Movie/', MovieViews.MovieList, name='MoList'),
    path('myweb-Movie/<int:movie_id>/', MovieViews.MovieDetail, name='MoDetail'),
    path('myweb-Movie/MoCreate/', MovieViews.MovieCreate, name='MoCreate'),
    path('myweb-Movie/MoModify/<int:movie_id>/', MovieViews.MovieModify, name='MoModify'),
    path('myweb-Movie/MoDelete/<int:movie_id>/', MovieViews.MovieDelete, name='MoDelete'),
    path('myweb-Movie/download/<movie_id>', MovieViews.MovieFileDownload, name="MoFileDownload"),
    # 영화 댓글 url
    path('myweb-Movie/MoCreate/Comment/<int:movie_id>/', CommentViews.CommentCreateMovie, name='CommentCreateMovie'),
    path('myweb-Movie/MoModify/Comment/<int:comment_id>/', CommentViews.CommentModifyMovie, name='CommentModifyMovie'),
    path('myweb-Movie/MoDelete/Comment/<int:comment_id>/', CommentViews.CommentDeleteMovie, name='CommentDeleteMovie'),

    # 게임 url
    path('myweb-Game/', GameViews.GameList, name='GList'),
    path('myweb-Game/<int:game_id>/', GameViews.GameDetail, name='GDetail'),
    path('myweb-Game/GCreate/', GameViews.GameCreate, name='GCreate'),
    path('myweb-Game/GModify/<int:game_id>/', GameViews.GameModify, name='GModify'),
    path('myweb-Game/GDelete/<int:game_id>/', GameViews.GameDelete, name='GDelete'),
    path('myweb-Game/download/<game_id>', GameViews.GameFileDownload, name="MoFileDownload"),
    # 게임 댓글 url
    path('myweb-Game/GCreate/Comment/<int:game_id>/', CommentViews.CommentCreateGame, name='CommentCreateGame'),
    path('myweb-Game/GModify/Comment/<int:comment_id>/', CommentViews.CommentModifyGame, name='CommentModifyGame'),
    path('myweb-Game/GDelete/Comment/<int:comment_id>/', CommentViews.CommentDeleteGame, name='CommentDeleteGame'),

]


