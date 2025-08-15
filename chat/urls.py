from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_list, name="chat_list"),
    path("room/<int:user_id>/", views.chat_room, name="chat_room"),
    path("send/<int:user_id>/", views.send_message, name="send_message"),
    path(
        "messages/<int:user_id>/", views.chat_messages_json, name="chat_messages_json"
    ),
]
