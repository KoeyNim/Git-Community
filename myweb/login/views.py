from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm

# 계정 생성
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            # 회원가입에서 입력한 값을 얻기 위함
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 신규 사용자를 저장한 후에 자동 로그인
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('myweb:home')
    else:
        form = UserForm()
    return render(request, 'Login/signup.html', {'form': form})