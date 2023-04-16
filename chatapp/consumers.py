from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage,ChatRoom
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
    ## nhận thông tin được gửi
    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        # giống với json đã gửi vào websocket ở trong file index.html
        await self.channel_layer.group_send(
            self.room_group_name,{
            'type':'chat_message',
            'message':message,
            'username':username,
            'room':room,
            }
        )
        await self.save_message(username,room,message)
    ## gửi data vào client
    async def chat_message(self,event):
        message = event['message']
        username = event['username']
        room = event['room']
        await self.send(text_data = json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))
    @sync_to_async
    def save_message(self,username,room,message):
        name = User.objects.get(username=username)
        room = ChatRoom.objects.get(slug =room )
        ChatMessage.objects.create(
            username = name,
            room=room,
            message_content = message
        )
    