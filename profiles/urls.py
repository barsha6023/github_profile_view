from django.urls import path
from . import views
urlpatterns = [
 path("", views.search, name="search"),
 path("bookmark/<str:username>/", views.bookmark, name="bookmark"),
 path("bookmarks/", views.bookmark_list, name="bookmarks"),
 path("bookmarks/<int:pk>/delete/", views.bookmark_delete, name="bookmark_delete"),
 path("visualise/", views.visualise, name="visualise"),
]

