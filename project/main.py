import sys
import time

import network

from board_lvgl import start_board
from debug_log import log
from gui import GUI

from secrets import WIFI_SSID, WIFI_PASSWORD


DEPARTURES = [
    ('12:05', '3', 'Bastasjo', 'On time'),                         # Placeholder data for now until I get the real data                                                      # (time, line, destination, status)
    ('12:10', '1', 'Lyckeby', 'On time'),
    ('12:14', '5', 'Nattraby', 'Delayed'),
    ('12:20', '1', 'Salto', 'On time'),
    ('12:25', '3', 'Centrum', 'On time'),
]


class Application:
    def __init__(self):
        self.display, self.touch, self.handler = start_board()
        self.gui = GUI(DEPARTURES)
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
