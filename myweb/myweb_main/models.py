import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

# 파일 경로
def FilePath(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([ymd_path, uuid_name + extension])

# 공지사항 model
class Notice(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)  # 기존 모델을 속성으로 가져갈 경우 ForeignKey를 사용, on_delete=models.CASCADE 공지가 삭제 될 경우 삭제
    subject = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True) # null=True, blank=True을 사용하면 어떤 조건으로든 값을 비워둘수 있음
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="추천", related_name='NoVoter')  # 추천인 기능 (Notice 모델에서 사용한 author와 voter가 모두 settings.AUTH_USER_MODEL모델로 참조되고 있기 때문에 related_name을 써주어야 함)

    def __str__(self):  # id 대신 제목을 표시
        return self.subject

    class Meta:
        db_table = "공지사항"
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항"


# 질문 model
class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="추천", related_name='QVoter')

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "질문게시판"
        verbose_name = "질문게시판"
        verbose_name_plural = "질문게시판"


# 답변 model
class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name="질문아이디", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="추천", related_name='AVoter')

    class Meta:
        db_table = "질문에대한답변"
        verbose_name = "질문에대한답변"
        verbose_name_plural = "질문에대한답변"


# 영화 게시판 model
class Movie(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    subject = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="추천", related_name='MoVoter')
    upload_file = models.FileField(verbose_name="파일", upload_to=FilePath, null=True, blank=True)
    file_subject = models.CharField(verbose_name="파일제목", max_length=64, null=True)

    def __str__(self):
        return self.subject

    def delete(self, *args, **kargs):
        if self.upload_file:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_file.path))
        super(Movie, self).delete(*args, **kargs)

    class Meta:
        db_table = "영화게시판"
        verbose_name = "영화게시판"
        verbose_name_plural = "영화게시판"


# 게임 게시판 model
class Game(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    subject = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="추천", related_name='GVoter')
    upload_file = models.FileField(verbose_name="파일", upload_to=FilePath, null=True, blank=True)
    file_subject = models.CharField(verbose_name="파일제목", max_length=64, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "게임게시판"
        verbose_name = "게임게시판"
        verbose_name_plural = "게임게시판"


# 댓글 model
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    create_date = models.DateTimeField(verbose_name="작성일시")
    modify_date = models.DateTimeField(verbose_name="수정일시", null=True, blank=True)
    question = models.ForeignKey(Question, verbose_name="질문댓글", null=True, blank=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="영화댓글", null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, verbose_name="게임댓글", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "댓글"
        verbose_name = "댓글"
        verbose_name_plural = "댓글"
