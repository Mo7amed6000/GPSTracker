import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.location_group = "location_group"
        await self.channel_layer.group_add(
            self.location_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.location_group,
            self.channel_name
        )

    async def location_update(self, event):
        latitude = event['latitude']
        longitude = event['longitude']
        altitude = event['altitude']
        speed = event['speed']

        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude,
            'altitude' : altitude,
            'speed' : speed
        }))

    async def receive(self, text_data):
        loc = json.loads(text_data)
        print(loc)
        await self.channel_layer.group_send(
            self.location_group,
            {
                'type': 'location_update',
                'latitude': loc["latitude"],  # placeholder, real data should come from text_data
                'longitude': loc["longitude"],  # placeholder, real data should come from text_data
                'altitude': loc["altitude"],  # placeholder, real data should come from text_data
                'speed': loc["speed"]  # placeholder, real data should come from text_data
            }
        )
