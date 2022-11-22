from django.urls import path
from mqapp import views

app_name = "mqapp"

urlpatterns = [
    path("", views.TopView, name="top"),
    path("home/", views.HomeView, name="home"),
    path("login/", views.Login, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signin/", views.SignIn, name="signin"),
    path("edit/<str:En>", views.EditView, name="edit"),
    path("play/<str:En>/<str:Ja>", views.PlayView, name="play"),
    path("play_m/<str:En>/<str:Ja>", views.PlayView, name="play_m"),
    path("net_post/", views.NetPost, name="net_post"),
    path("edit_n/<str:En>", views.Edit_nView, name="edit_n"),
    path("play_n/<str:En>/<str:Ja>", views.PlayView_n, name="play_n"),
    path("play_m_n/<str:En>/<str:Ja>", views.PlayView_n, name="play_m_n"),
    path("ajax-list/",views.Ajax_List, name="ajax-list"),
]
