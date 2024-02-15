from django.shortcuts import render
from miniblog.forms import SignupForm, Loginform ,postForm
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponseRedirect
from miniblog.models import Post
from django.contrib.auth.models import Group


#Home
def home(request):
    model_post =Post.objects.all()
    return render(request , 'temp_mini/home.html' ,{'post':model_post})




def About(request):
    return render(request , 'temp_mini/about.html')



def contact(request):
    return render(request , 'temp_mini/contact.html')



def dashboard(request):
    if request.user.is_authenticated:

        post =Post.objects.all()
        user =request.user
        full_name =user.get_full_name()
        grps =user.groups.all()

        return render(request , 'temp_mini/dashboard.html',{'posts':post ,'grps':grps,'full_name':full_name})
    else:
        return HttpResponseRedirect('/login/',)


#Add post
def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm =postForm(request.POST)
            if fm.is_valid():
                tit =fm.cleaned_data['title']
                desc=fm.cleaned_data['description']
                pst =Post(title=tit, description=desc)
                pst.save()
                fm =postForm()
        else:
            fm =postForm()
        return render(request , 'temp_mini/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')


#Update post
def updatepost(request,id):
    if request.user.is_authenticated:

        if request.method == 'POST':
            pi =Post.objects.get(pk=id)
            fm =postForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi =Post.objects.get(pk=id)
            fm=postForm(instance=pi)


        return render(request , 'temp_mini/update.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
    
#Delete Post
def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi =Post.objects.get(pk=id)
            pi.delete() 
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')






#login
def user_login(request):
    if  not request.user.is_authenticated:
        if request.method == 'POST':
            fm = Loginform(request=request,data=request.POST)
            if fm.is_valid():
                un =fm.cleaned_data['username']
                pa =fm.cleaned_data['password']
                user =authenticate(username=un, password=pa)
                if user is not None:
                    login(request,user)
                    messages.success(request,'login successful!!')
                    return HttpResponseRedirect('/dashboard/')
                
        else:
            fm =Loginform()
            return render(request , 'temp_mini/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')
    

#logout
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')



#Signup
def signup(request):
    if request.method == 'POST':
        fm =SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congrats!! You Become an Author')
            user=fm.save()
            grup =Group.objects.get(name='Author')
            user.groups.add(grup)
    else:
        fm =SignupForm()
    return render(request , 'temp_mini/signup.html', {'form':fm})


