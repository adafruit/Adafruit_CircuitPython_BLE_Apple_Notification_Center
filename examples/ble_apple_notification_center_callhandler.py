# SPDX-FileCopyrightText: 2022 Tod Kurt for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits notifications from Apple devices paired with it,
detecting specifically the IncomingCall and ActiveCall notification categories
and sending back Positive Actions to accept calls or Negative Actions to
decline or hang up calls. It also shows initiating pairing, prints existing
notifications and prints any new ones as they arrive.
"""

import time
import board
import digitalio

import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
import adafruit_ble_apple_notification_center as ancs

butA = digitalio.DigitalInOut(board.D4)  # Circuit Playground Bluefruit A button
butB = digitalio.DigitalInOut(board.D5)  # Circuit Playground Bluefruit A button
butA.switch_to_input(digitalio.Pull.DOWN)  # buttons are active HIGH
butB.switch_to_input(digitalio.Pull.DOWN)

radio = adafruit_ble.BLERadio()  # pylint: disable=no-member
a = SolicitServicesAdvertisement()
a.solicited_services.append(ancs.AppleNotificationCenterService)
radio.start_advertising(a)

while not radio.connected:
    pass

print("connected")

while radio.connected:
    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")

        ans = connection[ancs.AppleNotificationCenterService]
        for notification in ans.wait_for_new_notifications():
            print("new notification:", notification)

        print("Notifications:", len(ans.active_notifications))
        for nid, n in ans.active_notifications.items():
            print(
                "uid:",
                n.id,
                "cat:",
                n.category_id,
                "title:",
                n.title,
                "msg:",
                n.message,
            )
            if n.category_id == 1:  # incoming call, has positive & negative actions
                if butA.value:
                    print("accepting call")
                    n.send_positive_action()
                if butB.value:
                    print("declining call")
                    n.send_negative_action()
            if n.category_id == 12:  # active call, only has negative action
                if butB.value:
                    print("hanging up call")
                    n.send_negative_action()
    time.sleep(1)

print("disconnected")
