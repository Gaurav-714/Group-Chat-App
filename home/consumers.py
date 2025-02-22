from channels.consumer import SyncConsumer, async_to_sync
from channels.exceptions import StopConsumer

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...")
        async_to_sync(self.channel_layer.group_add)("dj-devs", self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Message Received From Client...")
        self.send({
            'type': 'websocket.receive',
            'text': 'Hello from server...'
        })

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...")
        async_to_sync(self.channel_layer.group_discard)("dj-devs", self.channel_name)
        raise StopConsumer()