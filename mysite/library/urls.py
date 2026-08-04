from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authors/", views.authors, name="authors"),
    path("authors/<int:author_pk>/", views.author, name="author"),
]
