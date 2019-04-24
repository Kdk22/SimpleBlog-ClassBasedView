from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView

from Blog.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post , Comment
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import  ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import PostSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter


class IndexView(generic.ListView):
    template_name = 'Blog/index.html'
    context_object_name = 'all_posts'  # By default it gives object_list

    def get_queryset(self):
        if self.request.user.is_authenticated:
             return self.request.user.posts.all()
        else:
            return Post.objects.all()


class SearchView(TemplateView):
    template_name = 'Blog/search.html'

    def get(self, request, *args, **kwargs):
        search = request.GET.get('q', '')
        self.results = Post.objects.get(
            Q(title__startswith=search) |
            Q(author__iexact=search) | Q(content__starts= search) | Q(categories__startswith=search) | Q(post_date=search)
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_object_name= 'results'
        context = super().get_context_data(results=self.results, **kwargs)
        return context


class DetailsView(generic.DetailView):
    model = Post
    # here model passes value to details.html
    fields = ['comment_text', 'comment_date']
    template_name = 'Blog/details.html'


class PostCreate(CreateView):
    # Post.author= request.user

    def form_valid(self, form):

        if self.request.user.is_authenticated:
            obj= form.save(commit= False)
            obj.author= self.request.user
            obj.save()
            return super().form_valid(form)



    model = Post
    fields =['title', 'content', 'categories','icon','post_date']
    template_name = 'Blog/post_form.html'
    success_url = reverse_lazy('Blog:index')


class PostDelete(DeleteView):
        model = Post
        success_url = reverse_lazy('Blog:index')


class PostUpdate(UpdateView):
    model = Post
    # model.author= request.user
    fields = ['title', 'content', 'categories', 'icon', 'post_date']
    template_name = 'Blog/post_form.html'

    success_url = reverse_lazy('Blog:index')
    #
    # def form_valid(self, form):
    #     response = super().form_valid(self, form)
    #     obj = form.save(commit=False)
    #     obj.author = self.request.user
    #     obj.save()
    #     return super().form_valid(self, form)


# class PostsFilter(BaseFilter):
#     fields = ['title', 'categories']
#
#     import ipdb
#     ipdb.set_trace()

# class PostSearchList(ListView):
#     model = Post
#     #paginate_by = 30
#     template_name = "Blog/post_form.html"
#     form_class = PostSearchForm
#     filter_class = PostsFilter
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         if self.request.GET
#             qs = qs.filter(title__=qs)
#         return qs


def index(request):
    return render(request,'Blog/index.html')

def home(request):
    return render(request,'Blog/home.html')

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
            user = user_form.save(commit= False)

            current_site = get_current_site(request)
            user.is_active = False
            #registered = False
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                #print('found it')
                profile.profile_pic = request.FILES['profile_pic']
                profile.save()


            #registered = True
            mail_subject = 'Activate your blog account.'
            message = render_to_string('Blog/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('please Conform your mail.')
                # redirect(reverse_lazy('Blog:home'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        return render(request,'Blog/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Conformation Success.')
    else:
        return HttpResponse('Activation link is invalid!')

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


