from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        
        # print(self.channel_layer)
        # print(self.channel_name)
        # print(self.scope["user"].id)
        group = "user_{0}".format(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, text_data):
        pass
        # print("rec:: ", text_data)
        # async_to_sync(self.channel_layer.group_send)("group", {
        #     "type": "request_message",
        #     "text": "okay"
        # })

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