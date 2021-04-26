from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from .Validators import SignupValidate, NameValidate, PhoneValidate
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, username, password, email, name, phone, **extra_fields):
        if not username:
            raise ValueError('username Required!')
        user = self.model(
            username=username,
            email=email,
            name=name,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # 슈퍼 유저
    def create_superuser(self, username, email=None, password=None):

        user = self.create_user(username, email, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=17, verbose_name="아이디", unique=True, validators=[SignupValidate])
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    email = models.EmailField(max_length=128, verbose_name="이메일", null=True, unique=True)
    name = models.CharField(max_length=20, verbose_name="이름", null=True, unique=True, validators=[NameValidate])
    phone = models.CharField(max_length=11, verbose_name="전화번호", unique=True, validators=[PhoneValidate])

    # 사용자 권한
    is_active = models.BooleanField(default=True, verbose_name="사용자활성화")
    is_staff = models.BooleanField(default=False, verbose_name="스태프")
    is_admin = models.BooleanField(default=False, verbose_name="관리자")
    is_superuser = models.BooleanField(default=False, verbose_name="개발자")

    USERNAME_FIELD = 'username'
    # 회원 가입 시 이메일 입력을 필수로 한다.
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

class SocialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # <- 특정 사용자 모델에 종속적이지 않다.
        on_delete=models.CASCADE,
        verbose_name="소셜사용자",
    )
    name = models.CharField(max_length=20, verbose_name="이름", null=True, unique=True, validators=[NameValidate])
    phone = models.CharField(max_length=11, verbose_name="전화번호", unique=True, validators=[PhoneValidate])

    class Meta:
        db_table = '소셜회원목록'
        verbose_name = "소셜사용자"
        verbose_name_plural = "소셜사용자"
