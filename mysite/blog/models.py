from django.db import models
# 引用django內建的會員管理系統
from django.contrib.auth.models import User as auth_user

# Create your models here.
# 建立表到資料庫
# python manage.py makemigrations blog
# python manage.py migrate


# python manage.py createsuperuser
class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    # 只return標籤名字
    def __str__(self):
        return self.name


class Articles(models.Model):
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    # on_delete:如果user被刪除的話會報錯
    title = models.CharField(max_length=500, blank=False, null=False)
    content = models.CharField(max_length=500, blank=False, null=False)
    # blank:收到的值是否可以為空值
    # null:在資料庫是否可以為空
    last_update = models.DateField(auto_now=True)
    # auto_now:新增現在的時間
    tags = models.ManyToManyField(
        Tag,
        related_name='articles_related_tags'
    )
    # ManyToManyField:每個article可以屬於多個tags，一個tags也可以屬於多個articles
    # related_name:可用於反向查找


# 新增文章
def _create_articles(request):
    a = Articles.objects.create(user = request.user, title = request.POST['title'], content = request.POST['content'])
    query = dict(request.POST)
    for i in query['tags']:
        a.tags.add(Tag.objects.get(id=i))


# 取得所有文章
def _get_articles():
    return Articles.objects.all().order_by('-last_update')


# 取得單篇文章
def _get_articles_by_id(id):
    return Articles.objects.filter(id=id).first()
    # Uses "first()" because Django objects return objects by default


# 編輯單篇文章
def _edit_articles_by_id(request,id):
    Articles.objects.filter(id=id).update(title = request.POST['title'], content = request.POST['content']) # No need to update user
    a = Articles.objects.filter(id=id).get()
    a.tags.remove()
    # Remove all of the previous tags
    query = dict(request.POST)
    for i in query['tags']:
        a.tags.add(Tag.objects.get(id=i))
        # Update the new tags


# 刪除單篇文章
def _del_articles_by_id(id):
    Articles.objects.filter(id=id).delete()