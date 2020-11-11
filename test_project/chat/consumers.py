import json
import collections
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import *

class ChatConsumer(AsyncWebsocketConsumer):
    # TODO attribute for storing new messasges
    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.message_list = None
    

    async def connect(self):
        self.message_list = []

        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # print(self.message_list)
        for message, time in self.message_list:
            # print(message)
            # print(time)
            await create_and_add_message_to_session(message, self.scope['user'].username, self.scope['url_route']['kwargs']['room_id'], time)

        self.message_list = None

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        self.message_list.append((text_data_json['message'], datetime.datetime.now()))

        message = self.scope['user'].username + ": " + text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # TODO check if user is banned

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))