from django.shortcuts import render, redirect
from Blog.models import UserInfo as User
from django.contrib.auth import authenticate
from Blog import models
from django.core.mail import send_mail


# 首页
def index(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    return render(request, 'index.html', locals())


# 登陆
def login(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = authenticate(username=username, password=password)
        if obj is None:
            erro_msg = '账户或密码错误'
            return render(request, 'login.html', locals())
        request.session["username"] = username
        request.session.set_expiry(604800)
        # return render(request, 'index.html', locals())
        return redirect('/index/')

    return render(request, 'login.html', locals())


# 注册
def logon(request):
    '''
    **********************
    email数据需要保持唯一性(models修改)
    **********************
    :param request:
    :return:
    '''
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        if pwd1 != pwd2:
            erro_msg = '两次密码输入不一致'
            return render(request, 'logon.html', locals())
        try:
            user = User.objects.create_user(username=username, password=pwd1, email=email)
        except:
            erro_msg = '用户名或邮箱已被使用'
            return render(request, 'logon.html', locals())

        return render(request, 'index.html', locals())

    return render(request, 'logon.html', locals())


# 文章
def article(request):
    '''
    **********************
    显示评论
    设定文章详细页面
    标签
    **********************
    :param request:
    :return:
    '''
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    article = models.Article.objects.all().order_by('-id')
    tags = models.Tag.objects.all()
    return render(request, 'article.html', locals())


# 评论
def comment(request):
    return render(request, 'index.html')


# 搜索
def search(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    if request.method == 'POST':
        search = request.POST.get('search')
        article = models.Article.objects.filter(title__contains=search)

        if article:
            pass
        else:
            print('1')
            msg_erro = '未查询到任何相关内容'
    return render(request, 'search.html', locals())


# About me
def about(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1
    return render(request, 'about.html', locals())


# 文章详细页
def view_article(request, *args, **kwargs):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    article_id = request.get_full_path().split('/')[2]
    article_info = models.Article.objects.filter(id=article_id)
    tags = models.Tag.objects.filter(article__tags__article=article_id).first()

    return render(request, 'view_article.html', locals())


# 用户信息
def user_info(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
    else:
        active = 1

    username = request.session.get('username')
    user = models.UserInfo.objects.filter(username=username)
    # print(models.UserInfo.objects.get(username=username).id)
    user_article = models.Article.objects.filter(user_id=models.UserInfo.objects.get(username=username).id)
    if request.method == 'POST':
        msg = request.POST.get('msg')
        fs = request.POST.get('fs')
        urls = request.POST.get('urls')
        conent = username + ' 给你的留言:' + '\n' + msg + '\n' + '联系方式：' + fs + ':' + urls
        # send_mail的参数分别是  邮件标题，邮件发内容件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        email = ['***@***.com']
        send_mail('MagicBooks.top有新的留言了',
                  conent,
                  '***@***.com',
                  ['***@***.com'])

    return render(request, 'user_info.html', locals())


# 登出
def logout(request):
    request.session.flush()
    return redirect('/index/')


# 编辑文章
def editor(request):
    active = 0
    username = request.session.get('username')
    if username is None:
        active = 0
        msg_erro = '请先登陆账号再进行发表文章'
        return render(request, 'login.html', locals())
    else:
        active = 1

    if request.method == 'POST':
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        content = request.POST.get('content')

        if title == '':
            msg_erro = '请完善所有内容再进行发布'
            return render(request, 'editor.html', locals())
        if tag == '':
            msg_erro = '请完善所有内容再进行发布'
            return render(request, 'editor.html', locals())
        if content == '':
            msg_erro = '请完善所有内容再进行发布'
            return render(request, 'editor.html', locals())

        user_id = models.UserInfo.objects.filter(username=username)
        new_art = models.Article.objects.create(title=title, content=content, user=user_id[0])
        find = models.Tag.objects.filter(name=tag)

        if find:
            old_tag = models.Tag.objects.get(name=tag)
            new_art.tags.add(old_tag.id)
        else:

            new_tag = models.Tag.objects.create(name=tag)
            new_art.tags.add(new_tag.id)
        return redirect('/article/')
    return render(request, 'editor.html', locals())


# 删除文章
def delarticle(request, *args, **kwargs):
    art_id = request.get_full_path().split('/')[2]
    del_art = models.Article.objects.get(id=art_id)
    del_art.delete()
    return redirect('/user_info/')

