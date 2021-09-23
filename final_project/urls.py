from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("register", views.register, name = "register"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name="logout"),
    path("liked_post/<int:post_id>", views.liked_post),
    path("post/<int:post_id>", views.post, name = "post"),
    path("liked_comment/<int:comment_id>", views.liked_comment),
    path("search_by_tags", views.search_by_tags, name = "search_by_tags"),
    path("search_by_title", views.search_by_title, name = "search_by_title"),
    path("search_tag/<str:tag>", views.search_tag, name = "search_tag"),
    path("edit_post/<int:post_id>", views.edit_post, name = "edit_post"),
]
