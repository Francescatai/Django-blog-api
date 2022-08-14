from django.shortcuts import render, redirect
from .models import _create_articles, _get_articles, _get_articles_by_id, _edit_articles_by_id, _del_articles_by_id
from .create_articles import create_articles_form, edit_articles_form
# django登入模組
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# 緩存
from django.views.decorators.cache import cache_page


# Create your views here.

@cache_page(10)
def index(request):
    articles = _get_articles()
    content = {"articles": articles}
    return render(request, 'index.html', content)


# 登入
def login(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return redirect("index")


def usr_login(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        auth_login(request, user)
        return redirect('index')
    else:
        return redirect('usr_login')


# 登出
def usr_logout(request):
    auth_logout(request)
    return redirect('index')


# 新增文章
def create_articles(request):
    if request.method == "POST":
        _create_articles(request)
        return redirect("index")
    else:
        form = create_articles_form()
        context = {"form": form}
        return render(request, "create_articles.html", context)


# 查看單篇文章
def view_article(request, a_id):
    context = {"article": _get_articles_by_id(a_id)}
    return render(request, "show_articles.html", context)


# 編輯單篇文章
def edit_article(request, a_id):
    if request.method == 'POST':
        _edit_articles_by_id(request, a_id)
        return redirect("index")
    else:
        form = edit_articles_form(a_id)
        context = {"form": form, "id": a_id}
        return render(request, "edit_articles.html", context)


# 刪除單篇文章
def delete_article(request,id):
    _del_articles_by_id(id)
    return redirect("index")
