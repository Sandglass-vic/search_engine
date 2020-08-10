from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from . models import *
import hashlib


# ENCODE
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    logged = request.session.get('is_login', None)
    gender = request.session.get('gender', None)
    return render(request, 'index/index.html', {"logged": logged, "gender": gender})


def login(request):
    message = ""
    if request.method == "GET":
        if request.session.get('is_login', None):
            return HttpResponseRedirect(reverse('index:index'))
        else:
            return render(request, 'index/login.html', {"message": message})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, password=hash_code(password))
        if user:
            request.session['is_login'] = True
            request.session['gender'] = user[0].gender
            return HttpResponseRedirect(reverse('index:index'))
        else:
            message = "Invalid password !"
            return render(request, 'index/login.html', {"message": message})


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('index:index'))


def register(request):
    if request.method == "GET":
        return render(request, 'index/register.html', {"message":""})
    else:
        username = request.POST['username']
        user_set = User.objects.filter(username=username)
        if user_set:
            message = "This name already exists."
            return render(request, 'index/register.html', {"message": message})
        else:
            password = request.POST['password']
            password_repeated = request.POST['password_repeated']
            if password != password_repeated:
                message = "The two passwords are not the same! "
                return render(request, 'index/register.html', {"message": message})
            gender = request.POST['gender']
            User.objects.create(username=username, password=hash_code(password), gender=gender)
            return HttpResponseRedirect(reverse('index:login'))


def search_view(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('index:login'))
    keyword = request.GET['keyword']
    return HttpResponseRedirect(reverse('index:search', args=(keyword,)))


def search(request, keyword):
    gender = request.session.get('gender')
    news_set = News.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
    return render(request, "index/search.html", {"gender": gender, 'news_set': news_set})


def detail(request, news_id):
    gender = request.session.get('gender')
    news = News.objects.get(id=news_id)
    return render(request, "index/detail.html", {"gender": gender, 'news': news})
