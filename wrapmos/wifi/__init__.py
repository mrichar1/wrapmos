"""Module that controls WIFI - both Client and Access Point modes.

Configuration takes the standard parameters for the `network` WLAN class:
https://docs.micropython.org/en/latest/library/network.WLAN.html

::

  {
    "wifi": {
      "client": {
        "ssid": "splat",
        "password": "mypasswd"
      },
      "ap": {
        "essid": "my_ap",
        "authmode": 0
        "password": "mysecret"
      }
    }
  }

"""

from machine import idle
import network
from .. import config

CONF = {
    'ap': {},
    'client': {},
}
CONF.update(config.config().get('wifi', {}))


def client(active=True, reconfigure=False):
    """Set up the wifi device as a client.

    Wifi details are written to flash memory for persistence.
    To avoid rewriting flash each time, reconfiguration must be explicitly requested.

    :param active: True/False to enable/disable wifi client.
    :param reconfigure: Set True to update wifi configuration on device.
    """

    wlan = network.WLAN(network.STA_IF)
    # Don't connect if no essid, or explicitly disabled
    if not active or not CONF['client'].get('ssid'):
        wlan.active(False)
        return
    # Can't find a way to get current saved password.
    # To reset password, set the essid to junk, call client
    # Then set it (and password) correctly.
    if reconfigure:
        wlan.connect(**CONF['client'])

    # Wait for wifi to come up
    while not wlan.isconnected():
        idle()


def access_point(active=True):
    """Set up the wifi device as an access point.

    Starts with the ESSID set to the MAC address, and the password `wemoswemos` if no alternative configuration is set.

    :param active: True/False to enable/disable wifi client.
    """

    ap = network.WLAN(network.AP_IF)
    if not active:
        ap.active(False)
        return
    ap.active(True)
    # Use MAC address as ESSID if not configured, disable auth
    if not 'essid' in CONF['ap']:
        from binascii import hexlify
        CONF['ap']['essid'] = hexlify(ap.config('mac'))
        # WPA-PSK2
        CONF['ap']['authmode'] = 3
        CONF['ap']['password'] = 'wemoswemos'
    ap.config(**CONF['ap'])
