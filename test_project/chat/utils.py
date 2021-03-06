from channels.db import database_sync_to_async

from django.contrib.auth.models import User

from .models import *

@database_sync_to_async
def is_user_banned(user_id: int):
    return ChatUser.objects.get(user_id=user_id).banned

@database_sync_to_async
def create_and_add_message_to_session(message: str, sender_username: str, session_id: int, time) -> None:
        session = ChatSession.objects.get(id=session_id)
        sender = User.objects.get(username=sender_username)

        message = Message.objects.create(sender=sender, content=message, time=time, session_id=session_id)

@database_sync_to_async
def get_message_history_from_session(session_id: int) -> str:
    session = ChatSession.objects.get(id=session_id)

    messages_query_set = Message.objects.filter(session_id=session_id).order_by('time')
    messages = ''

    for message in messages_query_set:
        messages += message.sender.username + ': ' + message.content + '\n'
    
    return messages

def user_exists(username: str) -> bool:
    return User.objects.all().filter(username=username).exists()

def chat_session_with_users_exists(username_one: str, username_two: str) -> bool:
    user_one = User.objects.get(username=username_one)
    user_two = User.objects.get(username=username_two)

    return ChatSession.objects.filter(users__in=[user_one]).filter(users__in=[user_two]).exists() # ??? 

def get_or_create_chat_session(user_one: str, user_two: str):
    user_one_existence = user_exists(user_one)
    user_two_existence = user_exists(user_two)

    
    if chat_session_with_users_exists(user_one, user_two):
        return ChatSession.objects.filter(users__in=[User.objects.get(username=user_one)]).filter(users__in=[User.objects.get(username=user_two)])[0]
    else:
        new_chat_session = ChatSession.objects.create()

        new_chat_session.users.add(User.objects.get(username=user_one))
        new_chat_session.users.add(User.objects.get(username=user_two))
        new_chat_session.save()

        return new_chat_session