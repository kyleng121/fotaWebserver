import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        value = data.get('value')  # Adjust this based on your data structure

        # Send the received data to all connected clients
        await self.send(text_data=json.dumps({
            'value': value
        }))
