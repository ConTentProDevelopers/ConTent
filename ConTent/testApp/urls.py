from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/|^$', views.index, name='index'),
    url(r'^indexpage/', views.indexpage, name='indexpage'),
    url(r'^error404/', views.error404, name='404'),
    url(r'^user/addfield/', views.addfield, name='addfield'),
    url(r'^reservation/', views.reservation, name='reservation'),
    url(r'^confirmation/', views.confirmation, name='confirmation'),
    url(r'^fields/', views.fields, name='fields'),
    url(r'^fieldsite/(?P<id>\d+)$', views.fieldsite, name='fieldsite'),
    url(r'^forgotemail/', views.forgotemail, name='forgotemail'),
    url(r'^forgotpassword/', views.forgotpassword, name='forgotpassword'),
    url(r'^login/', views.login_user_form),
    url(r'^logout_method/', views.logout_method),
    url(r'^postsearch/', views.postsearch, name='postsearch'),
    url(r'^register/', views.register, name='register'),
    url(r'^static_page/', views.static_page, name='static_page'),
    url(r'^user/', views.userclientstart, name='user-client-start'),
    url(r'^user-editlogin/', views.user_editlogin, name='user_editlogin'),
    url(r'^user-editprofile/', views.user_editprofile, name='user_editprofile'),
    url(r'^user-myreservations/', views.myreservations, name='myreservations'),
    url(r'^user-reservation/', views.single_reservation, name='single_reservation'),
    url(r'^user-owner-startpage/', views.userownerstart, name='user-owner-start'),
    url(r'^user-owner-addfield/', views.userowneraddfield, name='user-owner-addfield'),


]
