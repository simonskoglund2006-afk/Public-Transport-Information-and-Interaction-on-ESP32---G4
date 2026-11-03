import sys
import time
import json as jsn
import requests

import network
from board_lvgl import start_board
from debug_log import log
<<<<<<< HEAD
from departure_fetcher import Departure_fetcher
=======
from gui import GUI
>>>>>>> 0f40474 (created a new file and added my code there instead of main)

from gui import GUI
from secrets import WIFI_SSID, WIFI_PASSWORD

# Placeholder data for now until I get the real data
DEPARTURES = [
    ('12:05', '3', 'Bastasjo', 'On time'),                                                                               
    ('12:10', '1', 'Lyckeby', 'On time'),
    ('12:14', '5', 'Nattraby', 'Delayed'),
    ('12:20', '1', 'Salto', 'On time'),
    ('12:25', '3', 'Centrum', 'On time'),
]

# Stops shown in the settings list, backend will replace these later
STOPS = [
    "Campus Grasvik",
    "Karlskrona Centralstation",
    "Ronneby",
    "Lyckeby",
    "Nattraby",
]
TRANSPORT_TYPES = ("All", "Bus", "Train", "Ferry")

# Just for testing at the moment
DEPARTURES_BY_STOP = {
    "Campus Grasvik": [
        ("12:45", "1", "Karlskrona C", "On time"),
        ("12:52", "7", "Lyckeby", "Delayed"),
    ],
    "Karlskrona Centralstation": [
        ("12:48", "1", "Campus Grasvik", "On time"),
        ("13:05", "4", "Ronneby", "On time"),
        ("13:10", "2", "Lyckeby", "Cancelled"),
    ],
}

class Application:
    def __init__(self):
        self.display, self.touch, self.handler = start_board()
<<<<<<< HEAD
        self.gui = GUI(DEPARTURES, STOPS, TRANSPORT_TYPES)
=======
        self.gui = GUI(DEPARTURES)
>>>>>>> 0f40474 (created a new file and added my code there instead of main)
        self.connect_wifi()
        log("student application ready")

    @staticmethod
    def connect_wifi():
        'Function: Connects to WiFi'
        log("connecting to Wi-Fi SSID: " + WIFI_SSID)
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(WIFI_SSID, WIFI_PASSWORD)
        started = time.ticks_ms()
        while (not station.isconnected() and
               time.ticks_diff(time.ticks_ms(), started) < 15_000):
            time.sleep_ms(250)
        log("Wi-Fi connected" if station.isconnected()
            else "Wi-Fi could not connect (timeout)")

try:
    app = Application()
except Exception as error:
    log("FATAL: %r" % (error,))
    sys.print_exception(error)
    raise
