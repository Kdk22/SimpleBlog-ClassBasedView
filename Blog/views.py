from django.shortcuts import render, redirect
from Blog.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import  ImproperlyConfigured


class IndexView(generic.ListView):
    template_name = 'Blog/index.html'
    context_object_name = 'all_posts'  # By default it gives object_list

    def get_queryset(self):
        if self.request.user.is_authenticated:
             return self.request.user.posts.all()
        else:
            return Post.objects.all()


class DetailsView(generic.DetailView):
    model = Post  # here model passes value to details.html
    template_name = 'Blog/details.html'

class PostCreate(CreateView):
    model = Post
    fields =['author', 'title', 'content', 'categories','icon','post_date']
    template_name = 'Blog/post_form.html'
    success_url = reverse_lazy('Blog:index')


class PostDelete(DeleteView):
        model = Post
        success_url = reverse_lazy('Blog:index')


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'categories', 'icon', 'post_date']
    template_name = 'Blog/post_form.html'
    success_url = reverse_lazy('Blog:index')

def index(request):
    return render(request,'Blog/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Blog:index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'Blog/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('Blog:index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'Blog/login.html', {})


