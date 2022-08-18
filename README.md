# 用Django快速搭建一個簡易Blog API並運用Docker佈署到GCP上
## Project Tech Stack


| Backend |Frontend|Database|Cloud|Other|
| ------ | -------- | ----- | --- | --- |
| Django4| Bootstrap4| MySQL|GCP|Docker|

## 第一次使用Django就上手 
 安裝django
```
pip3 install django
```
 開啟新項目

```
django-admin startproject [mysite]
cd [mysite]
python manage.py runserver
```
 創建程式
```
python manage.py startapp [blog]
```

 ## 項目功能圖示

 #### 首頁
![](https://i.imgur.com/GwNwZpM.jpg)

#### 登入
![](https://i.imgur.com/tFsVARf.jpg)
#### 登入狀態可新增文章
![](https://i.imgur.com/tcdD7Kf.jpg)
#### 新增文章
![](https://i.imgur.com/tNI83Qw.jpg)
#### 查看/編輯/刪除文章
![](https://i.imgur.com/VvT63Wg.jpg)

## 使用Docker佈署Django到GCP上(Ubuntu20.04)

#### 安裝docker
##### [官方安裝參考](https://hub.docker.com/)
##### [學習參考](https://www.myfreax.com/how-to-install-and-use-docker-on-ubuntu-20-04/)

一鍵安裝shell
```
$ cat <<"EOF" | bash                              
sudo apt update && \
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y && \
sudo apt-get remove docker  docker.io containerd runc -y && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
sudo apt update && \
sudo apt install docker-ce docker-ce-cli containerd.io -y
EOF
```
檢查docker運行情形
```
$ sudo docker run hello-world
```
![](https://i.imgur.com/wqQ50H9.png)


#### 安装 gcloud CLI
##### [官方安裝參考](https://cloud.google.com/sdk/docs/install)
##### [學習參考](https://deskinsight.net/zh-hant/%E5%A6%82%E4%BD%95%E5%9C%A8-ubuntu-20-04-%E4%B8%8A%E5%AE%89%E8%A3%9D-google-cloud-sdk#%E5%9C%A8_Ubuntu_%E4%B8%8A%E5%AE%89%E8%A3%9D_Google_Cloud_SDK)
方法1
```
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates gnupg
$ curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
$ echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
$ sudo apt update
$ sudo apt install google-cloud-sdk
```
方法2
```
$ sudo snap install google-cloud-sdk --classic
```

#### 執行登入並選擇專案
```
$ cd google-cloud-sdk/bin
$ sudo gcloud init
$ gcloud auth login

```
![](https://i.imgur.com/L9BHF3e.jpg)

#### 建立並執行Docker file
##### [Docker file學習參考](https://solider245.github.io/VuePress-blog/%E6%96%87%E7%AB%A0%E8%BD%AC%E8%BD%BD/docker/Docker%20Compose%E4%BF%9D%E6%8C%81%E5%AE%B9%E5%99%A8%E8%BF%90%E8%A1%8C.html)
```
$ mkdir -p nginx-image; cd nginx-image;touch Dockerfile
$ vim Dockerfile
```
```
#docker file
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-files
WORKDIR /django-files
RUN git clone [git respo url]
RUN pip install Django
RUN pip install mysqlclient
ENTRYPOINT python Django-blog-api/mysite/manage.py runserver 0.0.0.0:80
```
```
$ sudo docker build --no-cache . -t [image name]
```
![](https://i.imgur.com/ihkWGn2.png)
查看docker image
```
$ sudo docker image ls
```
![](https://i.imgur.com/hIlFDbs.png)

#### 將Docker image上傳到GCP Container Registry
```
> > docker tag SOURCE_IMAGE HOSTNAME/PROJECT-ID/TARGET-IMAGE:TAG
$ sudo docker tag blog asia.gcr.io/djangopraticeblog/blog

> > docker push HOSTNAME/PROJECT-ID/IMAGE:TAG
$ sudo docker push asia.gcr.io/djangopraticeblog/blog
```
> ISSUE:[unauthorized] You don't have the needed permissions to perform this operation, and you may have invalid credentials. To authenticate your request, follow the steps in: https://cloud.google.com/container-registry/docs/advanced-authentication
> ```
> $ gcloud auth configure-docker
> $ export PATH=$PATH:/lib/google-cloud-sdk/bin
> $ gcloud auth print-access-token |sudo docker login -u oauth2accesstoken --password-stdin https://asia.gcr.io

![](https://i.imgur.com/pKwcuuB.png)

#### 建立及push Docker MySQL
```
$ sudo docker pull mysql:8
$ sudo docker images 
```
![](https://i.imgur.com/ywB6UFo.jpg)

```
$ sudo docker tag mysql:8 asia.gcr.io/djangopraticeblog/mysql:8
$ sudo docker push asia.gcr.io/djangopraticeblog/mysql:8
```
#### 新增MySQL執行個體並使用Docker image
![](https://i.imgur.com/mlGXJre.jpg)
![](https://i.imgur.com/7gEsVV2.png)
ssh 連線測試及檢查資料庫
```
$ docker ps
$ docker exec -i -t 2c5fe59531e7 /bin/bash
# mysql -u root -p
mysql> show databases;
```
![](https://i.imgur.com/cHNzHDK.jpg)

#### 新增Web API執行個體並使用Docker image
一樣要打開http與https
![](https://i.imgur.com/aFgrBZl.png)
ssh測試Django運行
```
$ docker ps
$ docker exec -i -t 3579c277f5f7 /bin/bash
# ls
# cd Django-blog-api/
# cd mysite/
# python manage.py runserver
```
![](https://i.imgur.com/HhzhfcZ.jpg)
若有報錯要修改python檔(修改前記得安裝vim)
```
# apt-get upgrade
# apt-get update
# apt-get install vim
```
更改資料庫連線(host使用內部IP)
設定ALLOW HOST(外部IP)
遷移資料庫結構
```
# python manage.py migrate

```
若要使用create article時記得要新增tag類別
建立使用者
```
# python manage.py createsuperuser
```

使用外部IP測試連線
![](https://i.imgur.com/AFJG5LE.jpg)
