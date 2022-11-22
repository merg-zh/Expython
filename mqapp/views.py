from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import forms

from mqapp.models import data,post_data

import random, string


def TopView(request):
    if request.method == 'POST':
        if 'un' in request.POST:
            name = request.POST['un']
            if data.objects.filter(username = name).exists() == True:
                user_data = data.objects.filter(username = name)
                user_data.delete()
                user_data2 = User.objects.filter(username = name)
                user_data2.delete()
    if request.user.is_authenticated == True:
        return HomeView(request)
    else:
        return render(request, 'mqapp/top.html',{'path':'top'})

def HomeView(request):
    username = str(request.user)
    form = forms.NewCreate()

    if data.objects.filter(username = username).exists() == False:
        user_data = data.objects.create(username = username, title = [], text_data = [], id_data = [], post_data = [], list_data = '', type_data = '')
    else:
        user_data = data.objects.get(username = username)
        if len(user_data.title) > 0 and len(user_data.list_data) == 0:
            for i in range(len(user_data.title)):
                user_data.list_data += str(i)+','
        if len(user_data.title) > 0 and len(user_data.type_data) == 0:
            for i in range(len(user_data.title)):
                user_data.type_data += '1,'
    user_data.save()
    
    if request.method == 'POST':
        if 'title' in request.POST:
            tt = request.POST['title']
            if tt != '':
                Flag = False
                for i in user_data.title:
                    if i == tt:
                        Flag = True
                if Flag == False:
                    user_data.title.append(tt)
                    user_data.text_data.append('null')
                    while(True):
                        id_text = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
                        flag = False
                        for i in data.objects.all():
                            for ii in i.id_data:
                                if id_text == ii:
                                    flag = True
                        if flag == False:
                            break
                    user_data.id_data.append(id_text)
                    user_data.post_data.append('false')
                    user_data.type_data += '1,'
                    if user_data.list_data == '':
                        ire = 0
                        user_data.list_data += str(ire)
                    else:
                        ire = int(max(user_data.list_data)) + 1
                        user_data.list_data += ','+str(ire)
                    
        elif 'ds' in request.POST:
            tt = request.POST['ds']
            if tt != '':
                idx = user_data.title.index(tt)
                if user_data.post_data[idx] == 'true':
                    P_data = post_data.objects.filter(id_data = user_data.id_data[idx])
                    P_data.delete()
                user_data.title.pop(idx)
                user_data.text_data.pop(idx)
                user_data.id_data.pop(idx)
                user_data.post_data.pop(idx)
                a = user_data.type_data.split(',')
                a.pop(idx)
                a = ','.join(a)
                user_data.type_data = a
                ll = user_data.list_data.split(',')
                atai = ll[idx]
                ll.pop(idx)
                for i in range(len(ll)):
                    if int(ll[i]) > int(atai):
                       ll[i] = str(int(ll[i]) - 1)
                ll = ','.join(ll)
                
                user_data.list_data = ll
        elif 'duser' in request.POST and 'did' in request.POST:
            duser = request.POST['duser']
            did = request.POST['did']
            if duser != '' and data.objects.filter(username = duser).exists() and did != '':
                dlu = data.objects.get(username = duser)
                idx = dlu.id_data.index(did)
                user_data.title.append(dlu.title[idx]+'(ダウンロード)')
                user_data.text_data.append(dlu.text_data[idx])
                user_data.post_data.append('no')
                user_data.type_data += dlu.type_data.split(',')[idx]
                if user_data.list_data == '':
                    ire = 0
                    user_data.list_data += str(ire)
                else:
                    ire = int(max(user_data.list_data)) + 1
                    user_data.list_data += ','+str(ire)
                while(True):
                    id_text = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
                    flag = False
                    for i in user_data.id_data:
                        if i == id_text:
                            Flag = True
                    if flag == False:
                        break
                user_data.id_data.append(id_text)
    user_data.save()
    ul = user_data.title
    type_data = user_data.type_data
    import os
    cwd = os.getcwd()
    print(cwd)
    return render(request, 'mqapp/home.html', {'form':form, 'ul': ul, 'path':'home', 'lc':user_data.list_data, 'type':type_data, 'cwd':cwd})

from django.contrib.auth import authenticate, login

def Login(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HomeView(request)
        else:
            return render(request, 'mqapp/login.html', {'form':form, 'ms': '※そのユーザーは存在しません。'})
    return render(request, 'mqapp/login.html', {'form':form, 'ms':'', 'path':'login'})

class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = "mqapp/login.html"

def SignIn(request):
    ms = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
        for i in User.objects.all():
            if request.POST['username'] == str(i):
                ms = '※この名前はすでに使われています'
    else:
        form = UserCreationForm()
    return render(request, 'mqapp/signin.html', {'form': form, 'ms':ms, 'path':'signin'})

def EditView(request, En):
    user_data = data.objects.get(username = str(request.user))
    idx = user_data.title.index(En)

    if request.method == 'POST':
        if 'data_text' in request.POST:
            user_data.text_data[idx] = str(request.POST['data_text'])
            user_data.save()
        if 'h_title' in request.POST:
            tt = str(request.POST['h_title'])
            a = user_data.type_data.split(",")
            if 'radio1' in request.POST:
                a[idx] = '1'
            elif 'radio2' in request.POST:
                a[idx] = '2'
            elif 'radio3' in request.POST:
                a[idx] = '3'
            user_data.type_data = ','.join(a)
            
            user_data.title[idx] = tt
            user_data.save()
            En = tt
    type_data = user_data.type_data.split(',')[idx]
    pd = user_data.post_data[idx]
    tab = user_data.text_data[idx]
    id_text = user_data.id_data[idx]
    
    if request.method == 'POST':
        if 'pst' in request.POST:
            if request.POST['pst'] == 'ok':
                if post_data.objects.filter(id_data = user_data.id_data[idx]).exists() == False:
                    P_data = post_data.objects.create(username = request.user, title = user_data.title[idx], text_data = user_data.text_data[idx], id_data = user_data.id_data[idx], type_data = user_data.type_data.split(',')[idx])
                else:
                    P_data = post_data.objects.get(id_data = user_data.id_data[idx])
                    P_data.title = user_data.title[idx]
                    P_data.text_data = user_data.text_data[idx]
                    P_data.type_data = user_data.type_data.split(',')[idx]
                    P_data.save()
                pd = 'true'
                user_data.post_data[idx] = 'true'
                user_data.save()
                return HomeView(request)
            
            if request.POST['pst'] == 'no':
                P_data = post_data.objects.filter(id_data = user_data.id_data[idx])
                P_data.delete()
                user_data.post_data[idx] = 'false'
                user_data.save()
                pd = 'false'
                    
    return render(request, 'mqapp/edit.html', {'en':En, 'tab': tab, 'id_text': id_text, 'path':'edit', 'pf':pd, 'type':type_data})

def PlayView(request, En, Ja):
    user_data = data.objects.get(username = str(request.user))
    idx = user_data.title.index(En)
    tab = user_data.text_data[idx]
    if request.method == 'POST':
        if 'miss' in request.POST:
            text_d = request.POST['miss']
            title_d = request.POST['title']
            Flag = False
            for i in user_data.title:
                if i == title_d:
                    Flag = True
            if Flag == False:
                user_data.title.append(title_d)
                user_data.text_data.append(text_d)
                while(True):
                    id_text = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
                    flag = False
                    for i in data.objects.all():
                        for ii in i.id_data:
                            if id_text == ii:
                                flag = True
                    if flag == False:
                        break
                user_data.id_data.append(id_text)
                user_data.post_data.append('false')
                ire = int(max(user_data.list_data)) + 1
                user_data.list_data += ','+str(ire)
                user_data.type_data += '1,'
                user_data.save()
                return HomeView(request)
        elif  'middle' in request.POST:
            text_d = request.POST['middle']
            title_d = request.POST['title']
            Flag = False
            for i in user_data.title:
                if i == title_d:
                    Flag = True
            if Flag == False:
                user_data.title.append(title_d)
                user_data.text_data.append(text_d)
                while(True):
                    id_text = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
                    flag = False
                    for i in data.objects.all():
                        for ii in i.id_data:
                            if id_text == ii:
                                flag = True
                    if flag == False:
                        break
                user_data.id_data.append(id_text)
                user_data.post_data.append('no')
                ire = int(max(user_data.list_data)) + 1
                user_data.list_data += ','+str(ire)
                user_data.type_data += '1,'
                user_data.save()
                return HomeView(request)
    if Ja == 't':
        return render(request, 'mqapp/play.html', {'en':En, 'tab':tab, 'path':'play'})
    else:
        return render(request, 'mqapp/play_m.html', {'en':En, 'tab':tab, 'path':'play_m'})

def NetPost(request):
    P_data = post_data.objects.all()
    user_name = ''
    title = []
    text_data = []
    id_data = []
    type_data = ''
    for i in P_data:
        user_name += i.username+','
        title.append(i.title)
        text_data.append(i.text_data)
        id_data.append(i.id_data)
        type_data += i.type_data+','
    return render(request, 'mqapp/net_post.html', {'path':'net_post', 'user_name':user_name, 'title':title, 'text_data':text_data, 'id_data':id_data, 'type':type_data})

def Source(request):
    base = ''
    return render(request, 'mqapp/source.html', {'path':'source', 'base':base})

def Edit_nView(request, En):
    idx = int(En.split('@$&')[1])
    P_data = post_data.objects.all()[idx]
    tab = P_data.text_data
    id_text = P_data.id_data
    title = P_data.title
    
    if request.method == 'POST':
        if 'idx' in request.POST:
            indx = int(request.POST['idx'])
            user_data = data.objects.get(username = request.user)
            flag = False
            for i in user_data.id_data:
                if i == P_data.id_data:
                    flag = True
            if flag == False:
                user_data.title.append(P_data.title + '(ダウンロード)')
                user_data.text_data.append(P_data.text_data)
                user_data.id_data.append(P_data.id_data)
                user_data.post_data.append('no')
                user_data.type_data += P_data.type_data+','
                if len(user_data.list_data) != 0:
                    ire = int(max(user_data.list_data)) + 1
                    user_data.list_data += ','+str(ire)
                else:
                    user_data.list_data += '0'
                user_data.save()
            
    return render(request, 'mqapp/edit_n.html', {'en':title, 'tab': tab, 'id_text': id_text, 'path':'edit_n', 'idx':idx})

def PlayView_n(request, En, Ja):
    idx = int(En.split('@$&')[1])
    P_data = post_data.objects.all()[idx]
    tab = P_data.text_data
    title = P_data.title
    if Ja == 't':
        return render(request, 'mqapp/play_n.html', {'en':title, 'tab':tab, 'path':'play_n'})
    else:
        return render(request, 'mqapp/play_m_n.html', {'en':title, 'tab':tab, 'path':'play_m_n'})

def Ajax_List(request):
    user_data = data.objects.get(username = request.user)
    user_data.list_data = request.POST.get('list')
    user_data.save()
    return HomeView(request)
