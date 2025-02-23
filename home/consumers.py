from channels.consumer import AsyncConsumer, async_to_sync
from channels.exceptions import StopConsumer

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

        # Broadcast the message to all connected clients
        await self.channel_layer.group_send(
            self.group_name, {
                'type': 'chat.message',
                'message': event['text']
            }
        )

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
