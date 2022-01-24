Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ble_apple_notification_center/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ble_apple_notification_center/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BLE_Apple_Notification_Center/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BLE_Apple_Notification_Center/actions
    :alt: Build Status

BLE library for the Apple Notification Center


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ble_apple_notification_center/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ble-apple-notification-center

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ble-apple-notification-center

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ble-apple-notification-center

Usage Example
=============

.. code::python

    """
    This example solicits that apple devices that provide notifications connect to it, initiates
    pairing, and prints existing notifications.
    """

    import adafruit_ble
    from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
    import adafruit_ble_apple_notification_center as ancs

    radio = adafruit_ble.BLERadio()
    a = SolicitServicesAdvertisement()
    a.solicited_services.append(ancs.AppleNotificationCenterService)
    radio.start_advertising(a)

    print("Waiting for connection")

    while not radio.connected:
        pass

    print("Connected")

    for connection in radio.connections:
        if ancs.AppleNotificationCenterService not in connection:
            continue

        if not connection.paired:
            connection.pair()
            print("Paired")

        ans = connection[ancs.AppleNotificationCenterService]
        # Wait for the notifications to load.
        while len(ans.active_notifications) == 0:
            pass
        for notification_id in ans.active_notifications:
            notification = ans.active_notifications[notification_id]
            print(notification.app_id, notification.title)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ble_apple_notification_center/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BLE_Apple_Notification_Center/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
