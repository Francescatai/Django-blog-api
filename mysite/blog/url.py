from django.urls import path
from . import views

# 當有使用者訪問/目錄時，就會呼叫views的index函式，將這個path命名為index
urlpatterns = [
    path('', views.index, name="index"),
    path('articles/<int:a_id>', views.view_article, name="articles"),
    path('articles/edit/<int:a_id>', views.edit_article, name="edit_articles"),
    path('articles/create', views.create_articles, name="create_articles"),
    path('articles/delete/<int:id>',views.delete_article, name="delete_article"),
    path('signin', views.login, name="signin"),
    path('login', views.usr_login, name="login"),
    path('logout', views.usr_logout, name="logout")
]
