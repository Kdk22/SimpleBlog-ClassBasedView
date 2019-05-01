from django.conf.urls import url
from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'Blog'

urlpatterns=[
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('admin/dashboard', views.DashBoard.as_view(), name='dashboard'),
    path('home/', views.home, name='home'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('<int:pk>/', views.DetailsView.as_view(), name='details'),
    path('<int:pk>/post_delete/', views.PostDelete.as_view(), name='post-delete'),
    path('<int:pk>/post_update/', views.PostUpdate.as_view(), name='post-update'),
    path('<int:pk>/post_comment/', views.PostComment.as_view(), name='post-comment'),

    path('login/<int:pk>/update/', views.PostUpdate.as_view(), name='update'),
    path('login/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),
    path('<username>/UserView/', views.UserView.as_view(), name='user_view'),



]

# Be careful setting the name to just /login use userlogin instead!
