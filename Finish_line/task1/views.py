from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm
from .models import *
from django.core.paginator import Paginator


# Create your views here.

def main(request):
    return render(request, 'main.html')


def menu(request):
    return render(request, template_name='menu.html')


def sign_up(request):
    info = {}
    users = User.objects.all()
    next_url = request.GET.get('next', 'main/')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            for user in users:
                if user.name == username:
                    info['error'] = 'Пользователь уже существует'
                    break
            else:
                if password != repeat_password:
                    info['error'] = 'Пароли не совпадают'
                elif not age.isdigit() or int(age) < 18:
                    info['error'] = 'Вы должны быть старше 18'

            if 'error' in info:
                info.update({
                    'username': username,
                    'password': password,
                    'repeat_password': repeat_password,
                    'age': str(age)
                })
                return render(request, 'registration_page.html',
                              {'form': form, 'info': info})

            User.objects.create(name=username, password=password, age=age)

            return redirect(next_url)
    else:
        form = ContactForm()
    return render(request, 'registration_page.html',
                  {'form': form}, )


def log_in(request):
    info = {}
    next_url = request.GET.get('next', 'main/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    return redirect(next_url)
                else:
                    info['error'] = 'Неверный пароль'
            except User.DoesNotExist:
                info['error'] = 'Пользователь не найден'

            info.update({
                'username': username,
                'password': password
            })
            return render(request, 'login_page.html', {'form': form, 'info': info})
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})


def about_post(request):
    items_per_page = int(request.GET.get('items_per_page', '3'))
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, items_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, 'post.html', {
        'page_posts': page_posts,
        'current_items_per_page': items_per_page,
        'available_items_per_page': [3, 5, 10, 20],
    })
