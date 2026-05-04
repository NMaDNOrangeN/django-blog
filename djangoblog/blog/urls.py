from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/add_comment/", views.add_comment, name="add_comment"),
    path("comments/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path(
        "comments/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
]
