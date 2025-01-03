import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat messages.
    Manages connecting, disconnecting, and receiving/sending messages.
    """
    async def connect(self):
        """
        Establishes a WebSocket connection and adds the user to the chat group.
        """
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles disconnection, removing the user from the chat group.
        """
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receives a message from the WebSocket, and sends it to the group.

        Args:
            text_data (str): The received message in JSON format.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    async def sendMessage(self, event):
        """
        Sends the message to the WebSocket for broadcast.

        Args:
            event (dict): Contains the message and username to be sent.
        """
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
