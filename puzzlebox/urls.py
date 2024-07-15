from django.urls import path

from . import views

app_name = "puzzlebox"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("secret", views.secret, name="secret"),
    path("complete", views.complete, name="complete"),
    path("movedial", views.movedial, name="movedial"),
    path("sendMoveDialMessage", views.sendMoveDialMessage, name="sendMoveDialMessage")
]