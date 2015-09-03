from ctypes import * # for mouse clicks
import time
import win32api

def mouseClick(button):
    """ clicks mouse button 'button' (left or right) """

    # adapted from http://kvance.livejournal.com/985732.html
    # START SENDINPUT TYPE DECLARATIONS
    PUL = POINTER(c_ulong)
    class KeyBdInput(Structure):
        _fields_ = [("wVk", c_ushort),
                 ("wScan", c_ushort),
                 ("dwFlags", c_ulong),
                 ("time", c_ulong),
                 ("dwExtraInfo", PUL)]

    class HardwareInput(Structure):
        _fields_ = [("uMsg", c_ulong),
                 ("wParamL", c_short),
                 ("wParamH", c_ushort)]

    class MouseInput(Structure):
        _fields_ = [("dx", c_long),
                 ("dy", c_long),
                 ("mouseData", c_ulong),
                 ("dwFlags", c_ulong),
                 ("time",c_ulong),
                 ("dwExtraInfo", PUL)]

    class Input_I(Union):
        _fields_ = [("ki", KeyBdInput),
                  ("mi", MouseInput),
                  ("hi", HardwareInput)]

    class Input(Structure):
        _fields_ = [("type", c_ulong),
                 ("ii", Input_I)]

    class POINT(Structure):
        _fields_ = [("x", c_ulong),
                 ("y", c_ulong)]
    # END SENDINPUT TYPE DECLARATIONS

    LEFTDOWN   = 0x0002
    LEFTUP     = 0x0004
    RIGHTDOWN  = 0x0008
    RIGHTUP    = 0x0010

    FInputs = Input * 2
    extra = c_ulong(0)

    click = Input_I()
    release = Input_I()

    if button == 'left':
        click.mi = MouseInput(0, 0, 0, LEFTDOWN, 0, pointer(extra))
        release.mi = MouseInput(0, 0, 0, LEFTUP, 0, pointer(extra))
    elif button == 'right':
        click.mi = MouseInput(0, 0, 0, RIGHTDOWN, 0, pointer(extra))
        release.mi = MouseInput(0, 0, 0, RIGHTUP, 0, pointer(extra))

    x = FInputs( (0, click), (0, release) )
    windll.user32.SendInput(2, pointer(x), sizeof(x[0]))

    time.sleep(0.05) # allow for things to settle...

def mouseMove(direction, angle):
    """ moves camera position in 'direction' (horizontally or vertically) """

    # this seems to work nicely, may change to mouse_event for smoother movement
    x,y = win32api.GetCursorPos()
    if direction == 'horizontally':
        win32api.SetCursorPos( (x+angle, y) )
    elif direction == 'vertically':
        win32api.SetCursorPos( (x, y+angle))

    time.sleep(0.05) # allow for things to settle...
