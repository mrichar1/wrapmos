""""Functions to handle the system (boot, sleep etc)."""

from esp import deepsleep
from machine import reset, Pin, Timer

def pin_callback(callback, pin=14):
    """If pin is pulled down, call a callback.

    This is useful to e.g. run particular code on boot.

    :param callback: Method to be called.
    :param pin: Pin to monitor.
    """

    watch_pin = Pin(14, Pin.IN, Pin.PULL_UP)
    # Pin is pulled down
    if not watch_pin.value():
        callback()

def stop_after(delay=60, action="reset", wake_after=600):
    """Start a timer thread, which will restart/sleep the device after 'delay' secs.

    :param delay: Delay before restart/sleep.
    :param action: Reset or sleep the device.
    :param wake_after: If sleeping, how long until wake (in seconds).
    """

    timer = Timer(-1)
    if action == "deepsleep":
        # lambda to handle mandatory callback arg (x)
        cb = lambda x: deepsleep(1000000 * (wake_after + delay))
    else:
        cb = lambda x: reset()
    timer.init(mode=Timer.ONE_SHOT,
               period = 1000 * delay,
               callback = cb)
