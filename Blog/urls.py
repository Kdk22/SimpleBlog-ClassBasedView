from django.conf.urls import url
from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'Blog'

urlpatterns=[
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('<int:pk>/', views.DetailsView.as_view(), name='details'),
    path('<int:pk>/post_delete/', views.PostDelete.as_view(), name='post-delete'),
    path('<int:pk>/post_update/', views.PostUpdate.as_view(), name='post-update'),

    path('login/<int:pk>/update/', views.PostUpdate.as_view(), name='update'),
    path('login/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),



]

# Be careful setting the name to just /login use userlogin instead!
