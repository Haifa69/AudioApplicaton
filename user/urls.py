from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
from .views import Home, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.conf import settings
urlpatterns =[
                             path('', views.search, name="search"),
path("post/",views.upload_form, name="upload"),
path("indexsocial/",views.indexsocial, name="index"),
    path('search/', views.search, name='search'),
path("feed/",views.userfeed, name="userfeed"),
    path("record/", views.record, name="record"),
    path("record/detail/<uuid:id>/", views.record_detail, name="record_detail"),
    path("audio/", views.audio, name="index"),
    path("about/", views.about, name="about"),
    path('account/', views.start, name='account-base'),
    path("accounts/", include("allauth.urls")),  # new
       path("github", Home.as_view(), name="home"), # new


    path('register/', views.register, name='site-register'),
    path('upload', views.upload, name='upload'),
    path('homepage/', PostListView.as_view(), name='site-homepage'),

path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('homepage/editaccount/', views.editacc, name='site-editacc'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='site-user-login'),
    path('logout/',  auth_views.LogoutView.as_view(template_name='user/logout.html'), name='site-user-logout'),
    path('password-reset/enter_email/', auth_views.PasswordResetView.as_view(template_name='user/passreset.html'), name='site-user-passwordreset'),
    path('password-reset/link_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user/passreset2.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/passreset_complete.html'),
         name='password_reset_complete')]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
