import logging
import time
import win32api
import win32con

def sendKey(key, duration):
    """ sends a keypress 'key' to game window that lasts for 'duration' """

    keycodes = {
        'w': 0x57,
        's': 0x53,
        'a': 0x41,
        'd': 0x44
    }

    try:
        keycode = keycodes[key]
    except KeyError:
        logging.error("key '%s' is not implemented" % (key))
        return

    win32api.keybd_event(keycode,0,win32con.KEYEVENTF_EXTENDEDKEY,0) # press button
    time.sleep(duration) # keep pressing
    win32api.keybd_event(keycode,0,win32con.KEYEVENTF_KEYUP,0) # release button
    time.sleep(0.3) # allow key release to finish before continuing
