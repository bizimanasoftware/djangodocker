import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import Thread, ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Connects the user to the chat thread's WebSocket.
        """
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'chat_{self.thread_id}'

        user = self.scope['user']
        if user.is_authenticated:
            try:
                # Fetch the thread asynchronously
                thread = await sync_to_async(Thread.objects.get)(id=self.thread_id)

                # Correct participant check: user must be either participant1 or participant2
                if user.id in [thread.participant1_id, thread.participant2_id]:
                    self.thread = thread
                    # Join the channel group
                    await self.channel_layer.group_add(
                        self.thread_group_name,
                        self.channel_name
                    )
                    await self.accept()
                else:
                    # User not participant — close with Forbidden
                    await self.close(code=403)
            except Thread.DoesNotExist:
                # Thread not found
                await self.close(code=404)
        else:
            # User not authenticated
            await self.close(code=401)

    async def disconnect(self, close_code):
        """
        Leaves the channel group on disconnect.
        """
        if hasattr(self, 'thread_group_name'):
            await self.channel_layer.group_discard(
                self.thread_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Receives a message from the WebSocket, saves it to the database,
        and broadcasts it to the group.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '').strip()
        user = self.scope['user']

        if message and user.is_authenticated:
            # Save the message asynchronously
            new_message = await sync_to_async(ChatMessage.objects.create)(
                thread=self.thread,
                sender=user,
                text=message
            )

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.thread_group_name,
                {
                    'type': 'chat_message',
                    'message': new_message.text,
                    'sender_username': user.username,
                    'timestamp': timezone.localtime(new_message.created).strftime('%b %d, %I:%M %p')
                }
            )

    async def chat_message(self, event):
        """
        Receives a message event from the group and sends it over the WebSocket.
        """
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_username': event['sender_username'],
            'timestamp': event['timestamp'],
        }))
