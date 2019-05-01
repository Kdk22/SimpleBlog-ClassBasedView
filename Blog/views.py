from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView

from Blog.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, request
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
from itertools import chain
from django.db.models import Q
from django.utils.dateparse import parse_date

from .forms import PostSearchForm, CommentForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter


class IndexView(generic.ListView):
    template_name = 'Blog/index.html'
    context_object_name = 'all_posts'  # By default it gives object_list
    model = Post
    fields = ['like_count']

    def get_queryset(self):
        # if self.request.user.is_authenticated:
        #      return self.request.user.posts.all()
        # else:

        print(self.request.user)
        # import ipdb
        # ipdb.set_trace()
        return Post.objects.all()



class UserView(generic.ListView):
    template_name = 'Blog/user_view.html'
    context_object_name = 'all_posts'
    model = Post
    fields = ['like_count']


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.posts.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        for p in queryset:
            comment = p.comments.all()
            context[str(p)] = comment
            # str(context[p])
            # d={'all_comments':comment}
            # context.upda

        import ipdb
        ipdb.set_trace()

        return super().get_context_data(**context)

    # def get_context_data(self, **kwargs):
    #     context = {}
    #     if self.object:
    #         context_object_name = self.get_context_object_name(self.object)
    #         comments = self.object.comments.all()
    #         # commentors = Comment.comments.all()
    #         context['comments'] = comments
    #         context['field'] = self.fields
    #         if context_object_name:
    #             context[context_object_name] = self.object
    #         return super().get_context_data(**context)



class SearchView(TemplateView):

    # def get_queryset(self):
    #     model = Post
    #     title = self.kwargs['title']
    #     categories = self.kwargs['categoies']
    #     post_date = self.kwargs['daterange']
    #     author = self.kwargs['author']
    #     Results = Post.objects.filter(Q(title= title) | Q(categories= categoies) | Q(author= author))
    #     import ipdb
    #     ipdb.set_trace()
    #     return Results

    template_name = 'Blog/search.html'

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', '')
        categories = request.GET.get('categories','')
        start_date = request.GET.get('startdate','')
        end_date = request.GET.get('enddate','')
        author = request.GET.get('author','')

        # if start_date and end_date is None:
        #     start_date= 9999-12-31
        #     end_date = 9999-12-31


        # self.results = Post.objects.filter(
        #     Q(title__iexact=title) | Q(categories__iexact=categories) | Q(author__username__iexact=author)| Q(
        #         post_date__range=[start_date, end_date]))
        self.results = Post.objects.all()

        if title:
            self.results = self.results.filter(title__iexact=title)


        if categories:
            self.results = self.results.filter(categories__iexact=categories)

        if start_date and end_date:
            self.results = self.results.filter(
                post_date__range=[start_date, end_date])

        if author:
            self.results = self.results.filter(author__username__iexact=author)


            # self.results = self.results.filter(Q(title__iexact=title) | Q(categories__iexact=categories) | Q(author__username__iexact=author) , Q(
            #     post_date__range=[start_date, end_date]))
        # else:
        #     self.results = Post.objects.filter(Q(title__iexact= title) | Q(categories__iexact= categories)  | Q(author__username__iexact= author))
        # #self.results = Post.objects.filter(title__iexact=title).filter(categories__iexact = categories).filter(author__username__iexact = author)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_object_name = 'results'
        context = super().get_context_data(results=self.results, **kwargs)

        return context

    # def get(self, request, *args, **kwargs):
    #     search = request.GET.get('q', '')
    #     # self.results = Post.objects.get(Q(title__startswith=search) | Q(content__icontains=search))
    #     self.results = Post.objects.filter(title__startswith=search)
    #     return super().get(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context_object_name= 'results'
    #     context = super().get_context_data(results=self.results, **kwargs)
    #     return context

class DashBoard(generic.ListView):
    template_name = 'Blog/dashboard.html'
    context_object_name = 'all_posts'  # By default it gives object_list

    # def get_queryset(self):
    #     pass
        # if self.request.user.is_superuser:
        #     post_get = Post.objects.all()
        #     comment_all = Comment.objects.all()
        #     comment_get = Post.comment_
        # return chain(post_get, comment_get)

    def get_queryset(self):
        # if self.request.user.is_authenticated:
        #      return self.request.user.posts.all()
        # else:
            return Post.objects.all()


class DetailsView(generic.DetailView):
    model = Post
    # here model passes value to details.html
    fields = ['comment_text', 'comment_date']
    template_name = 'Blog/details.html'


    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        form = CommentForm()

        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            comments = self.object.comments.all()
            # commentors = Comment.comments.all()
            context['comments'] = comments
            context['form'] = form
            # context['commentors']= commentors
            if context_object_name:
                context[context_object_name] = self.object
        # import ipdb
        # ipdb.set_trace()
        context.update(kwargs)




        return super().get_context_data(**context)

class PostComment(CreateView):

    form = CommentForm()

    model = form.Meta.model
    fields = form.Meta.fields
    # template_name = 'Blog/details.html'
    success_url = reverse_lazy('Blog:index')

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            p1= Post.objects.get(pk=kwargs['pk'])
            obj = form.save(commit= False)
            obj.user = self.request.user
            obj.post = p1
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def form_valid(self, form):
    #
    #     if self.request.user.is_authenticated:
    #         import ipdb
    #         ipdb.set_trace()
    #         obj= form.save(commit= False)
    #         obj.user= self.request.user
    #         return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     ctx =  super().get_context_data(**kwargs)
    #     import ipdb; ipdb.set_trace()
    #     return ctx
    #
    #comment_form = CommentForm(data= request.POST)
    #context_object_name = comment_form
    # f= CommentForm.Meta.fields
    # def get_context_data(self, **kwargs):
    #     context = super(DetailsView, self).get_context_data(**kwargs)
    #     context= CommentForm.Meta.fields
    #     import ipdb
    #     ipdb.set_trace()
    #     return context

    # def get_context_data(self, **kwargs):
    #     """Insert the single object into the context dict."""
    #     # context = {}
    #     ctx = super().get_context_data(**kwargs)
    #     import ipdb
    #     ipdb.set_trace()
    #     form = CommentForm()
    #
    #     # if request.method == 'POST':
    #     #     comment_form = CommentForm(data=request.POST)
    #     #     if comment_form.is_valid():
    #     #         new_comment = comment_form.save(commit=False)
    #     #         import ipdb
    #     #         ipdb.set_trace()
    #
    #
        # if self.object:
        #     context['object'] = self.object
        #     context_object_name = self.get_context_object_name(self.object)
        #     comments = self.object.comments.all()
        #    # commentors = Comment.comments.all()
        #     context['comments'] = comments
        #     context['form'] = form
        #    # context['commentors']= commentors
        #     if context_object_name:
        #         context[context_object_name] = self.object
        # # import ipdb
        # # ipdb.set_trace()
        # context.update(kwargs)
        # return super().get_context_data(**context)
    #     return ctx
    # def get_context_data(self, **kwargs):
    #     context = {}
    #     all_posts=Post.objects.all()[:5]
    #     for posts in all_posts:
    #         comments = posts.comments.all()
    #         values = {
    #             'posts': posts,
    #             'comments': comments
    #         }
    #         #context['posts'].append(posts)
    #         #context['comments'].append(comments)
    #         context.update(values)
    #
    #     import ipdb
    #     ipdb.set_trace()
    #     for f in context:
    #         print(f)
    #     return context


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


