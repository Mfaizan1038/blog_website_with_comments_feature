from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Post, Comment

def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_text = request.POST.get("comment_text")
            post_id = request.POST.get("post_id")
            parent_id = request.POST.get("parent_id") 

            post = Post.objects.get(id=post_id)

          
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    comment=comment_text,
                    parent=parent_comment
                )
            else:
               
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    comment=comment_text
                )

            return redirect('/home/')
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('/login/')

    return render(request, 'home.html', {'posts': posts})


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_Name")
        last_name = request.POST.get("last_Name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "username taken")
            return redirect('/register/')
        
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.error(request, "Account created")

        return redirect('/register/')  

    return render(request, 'register.html')

def login_page(request):
     if request.method == "POST":
       
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
             messages.error(request, "invalid username")
             return redirect('/login/')
        user=authenticate(username=username,password=password)

        if user is None:
            messages.error(request, "invalid password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/home/')

        

     return render(request,'login.html')



def logout_user(request):
    logout(request)
    return redirect('/login/')

