import asyncio
import websockets
import serial
import json

# WebSocket URI
uri = "ws://localhost:8001/ws/location/"
# Device URL
device = '/dev/cu.usbserial-1420'
device1 = '/dev/cu.usbserial-1410'

async def SendData(uri):
    async with websockets.connect(uri) as websocket:
        ser = None
        try:
            ser = serial.Serial(device, 9600)
        except:
            if ser is None:
                ser = serial.Serial(device1, 9600)
        print("working Normaly")
        while True:
            data = ser.readline().decode('utf-8').strip()
            print(data)
            if len(data.split(',')) > 1:
                lat, lon, alt,spd = data.split(',')
                await websocket.send(json.dumps({
            'latitude': lat,
            'longitude': lon,
            'altitude' : alt,
            'speed': spd
        }))


if __name__ == "__main__":
    asyncio.run(SendData(uri))
    print("running")
