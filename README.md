# GPS Tracker

Real-time GPS tracking for Arduino: the device reads a GPS module, a Python bridge sends coordinates over WebSocket, and a Django map UI plots the live path (Leaflet + offline OSM tiles).

Centered around Algiers by default (latitude `36.7538`, longitude `3.1588`).

## How it works

```
GPS module  →  Arduino (NMEA GGA/RMC)
                    ↓ serial (9600 baud)
           websocket_client.py
                    ↓ WebSocket  ws://localhost:8001/ws/location/
           Django Channels
                    ↓ browser
           Leaflet map  (/tracker/gps_tracker/)
```

1. The Arduino sketch parses `$GPGGA` / `$GNGGA` (lat, lon, altitude) and `$GPRMC` / `$GNRMC` (speed).
2. Valid fixes are printed as `latitude,longitude,altitude,speed`.
3. `websocket_client.py` reads that serial line and forwards JSON to the server.
4. Connected browsers draw a marker, trail, speed, and altitude.

There is also a **route replay** page: paste or load `lat, lon` lines and draw colored polylines (sample traces: `fromElitToBabzouar.txt`).

## Project layout

```
GPS tracker/
├── GPS_Tracker_Sonser/          # Arduino sketch
│   └── GPS_Tracker_Sonser.ino
├── gps_tracker/                 # Django + Channels app
│   ├── manage.py
│   ├── gps_tracker/             # project settings, ASGI
│   ├── tracker/                 # views, WebSocket consumer, templates
│   └── static/                  # Leaflet + offline map tiles
├── websocket_client.py          # serial → WebSocket bridge
├── fromElitToBabzouar.txt       # sample path (El Harrach / Bab Ezzouar area)
└── fromElitToBabzouar2.txt
```

## Hardware

- Arduino (or compatible board) with a free serial port
- GPS module that outputs NMEA at **9600 baud** (u-blox 8-style `GNGGA` is supported)
- Wiring used by the sketch (**SoftwareSerial**):
  - GPS **TX** → Arduino pin **11**
  - GPS **RX** → Arduino pin **10**
  - GPS GND / VCC as usual (many modules are **3.3 V**)

Flash `GPS_Tracker_Sonser/GPS_Tracker_Sonser.ino` with the Arduino IDE. Open the Serial Monitor at 9600 baud; you should see `lat,lon,alt,speed` once the module has a fix.

NMEA parsing in the sketch is based on work by Mamour Diop & Congduc Pham, University of Pau.

## Software requirements

- Python **3.10+**
- Arduino IDE (to flash the sketch)
- A USB serial device (macOS often looks like `/dev/cu.usbserial-*`)

Python packages are listed in `requirements.txt`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Update `ALLOWED_HOSTS` in `gps_tracker/gps_tracker/settings.py` if you browse from another machine.

If you publish this repo, replace the Django `SECRET_KEY` in settings and do not reuse the development key.

## Run the map server

The live map talks to **port 8001** (see `websocket_client.py` and `gps_tracking.html`). From the Django project folder:

```bash
cd gps_tracker
daphne -b 0.0.0.0 -p 8001 gps_tracker.asgi:application
```

Then open:

| Page | URL | What it does |
|------|-----|----------------|
| Live tracker | http://127.0.0.1:8001/tracker/gps_tracker/ | Live marker, trail, speed, altitude, copy path |
| Route drawer | http://127.0.0.1:8001/tracker/gps_line/ | Paste `lat, lon` lines and draw a polyline |

Tiles are served locally from `gps_tracker/static/` (`/tracker/tiles/{z}/{x}/{y}.png`), so the map works without calling OpenStreetMap on every pan.

The line view currently builds tile URLs with port **8000**. If tiles are missing there, run that page on 8000 as well, or change the `uri` in `gps_line.html` to match Daphne.

## Bridge Arduino → server

1. Plug in the Arduino and note the serial port (`ls /dev/cu.usbserial-*` on macOS).
2. Set `device` / `device1` in `websocket_client.py` to that path.
3. With Daphne already running:

```bash
source .venv/bin/activate
python websocket_client.py
```

Payload sent on each fix:

```json
{
  "latitude": "36.75380",
  "longitude": "3.15880",
  "altitude": "55.10",
  "speed": "12.40"
}
```

Speed is in **km/h**, altitude in **meters**.

## Draw a saved route

1. Open `/tracker/gps_line/`.
2. Paste coordinates, one pair per line, for example:

   ```
   36.70339,  3.10414
   36.70336,  3.10417
   ```

3. Pick a color and click **trace coordinates**.

You can copy a live trail from the tracker page (**Copy**) and paste it here.

## Configuration notes

- WebSocket path: `ws://<host>:8001/ws/location/`
- Channel layer: in-memory (fine for one process; use Redis/`channels-redis` if you scale workers)
- Database: SQLite (`gps_tracker/db.sqlite3`); not required for live tracking
- Also you can change the center point of the map and add your own offline OSM tails

`tracker/serial_reader.py` is an older in-process serial helper. The working path used here is `websocket_client.py`.

## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this project, provided that the original copyright notice and license are retained.
