import serial
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def read_from_serial():
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust with your serial port
    channel_layer = get_channel_layer()
    
    while True:
        data = ser.readline().decode('utf-8').strip()
        lat, lon = data.split(',')
        async_to_sync(channel_layer.group_send)(
            "location_group",
            {
                "type": "location.update",
                "latitude": lat,
                "longitude": lon,
            }
        )
