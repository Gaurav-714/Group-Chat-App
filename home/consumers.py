from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
import json
from .models import GroupModel, ChatModel


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print(f"✅ Websocket Connected: {self.channel_name}")

        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print(f"📩 Message Received From Client: {event['text']}")
        try:
            data = json.loads(event['text'])
            group = await database_sync_to_async(GroupModel.objects.get)(name=self.group_name)
            chat = await database_sync_to_async(ChatModel.objects.create)(
                content=data['message'], group=group
            )
            # Send message to group
            await self.channel_layer.group_send(
                self.group_name, {
                    'type': 'chat.message',
                    'message': data['message']  # Extracted from JSON
                }
            )
        except json.JSONDecodeError:
            print("❌ Invalid JSON received.")
        except GroupModel.DoesNotExist:
            print(f"❌ Group '{self.group_name}' does not exist.")

    async def chat_message(self, event):
        print(f"🔄 Broadcasting Message: {event['message']}")

        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print(f"❌ Websocket Disconnected: {self.channel_name}")
        
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()
