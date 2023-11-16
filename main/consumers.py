from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        
        group = "user_{0}".format(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

        self.send({
            "type": "websocket.accept"
        })


    def send_update(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    def websocket_disconnect(self, event):
        print("Disconnected", self.scope["user"])
        group = "user_{0}".format(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()