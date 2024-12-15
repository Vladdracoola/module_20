from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm, LoginForm, ImageFeedForm
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import process_image


# Create your views here.

def main(request):
    return render(request, 'main.html')


def menu(request):
    return render(request, template_name='menu.html')


def sign_up(request):
    info = {}
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif not age.isdigit() or int(age) < 18:
                info['error'] = 'Вы должны быть старше 18'
            elif User.objects.filter(username=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {username}!')
                login(request, user)
                return redirect(next_url)

            info.update({'username': username, 'password': password, 'repeat_password': repeat_password, 'age': age})
        return render(request, 'registration_page.html', {'form': form, 'info': info})
    else:
        form = ContactForm()
    return render(request, 'registration_page.html', {'form': form})


def log_in(request):
    info = {}
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect(next_url)
            else:
                info['error'] = 'Неверный логин или пароль'
                info.update({'username': username})
        return render(request, 'login_page.html', {'form': form, 'info': info})
    else:
        form = LoginForm()
    return render(request, 'login_page.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return redirect('/')


@login_required
def detection(request):
    image_feeds = ImageFeed.objects.filter(user=request.user)
    return render(request, 'detection.html', {'image_feeds': image_feeds})


@login_required
def add_image(request):
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user
            image_feed.save()
            return redirect('/detection')
    else:
        form = ImageFeedForm()
    return render(request, 'add_image.html', {'form': form})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageFeed, id=image_id, user=request.user)
    image.delete()
    return redirect('/detection')


@login_required
def process_image_feed(request, feed_id):
    image_feed = get_object_or_404(ImageFeed, id=feed_id, user=request.user)
    process_image(feed_id)
    return redirect('/detection')
