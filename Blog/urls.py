from django.conf.urls import url
from . import views



from django.conf.urls import url

app_name = 'Blog'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),


]