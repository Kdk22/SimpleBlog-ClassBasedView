from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from Blog.models import Post, User, UserProfileInfo
from Blog.views import IndexView

class IndexView(generic.ListView):
    template_name = 'Blog/index.html'
    context_object_name = 'all_posts'  # By default it gives object_list

    def get_queryset(self):
        if self.request.user.is_authenticated:
             return self.request.user.posts.all()
        else:
            return Post.objects.all()


    # template_name = 'dashboard/login.html'
    # context_object_name = 'all_posts'  # By default it gives object_list
    #
    # def get_queryset(self):
    #     if self.user.is_superuser:
    #          return Post.objects.all()
    #     else:
    #         return redirect('Blog:index')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if user.is_superuser:
                    return redirect('dashboard:index')
                else :
                    return redirect('Blog:index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'Blog/login.html', {})
