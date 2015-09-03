# functions are specific to microsoft windows currently

import logging
import time
import win32gui
import win32api
import numpy as np
from PIL import ImageGrab

class GameWindow(object):

    def __init__(self, frame_size):
        self.frame_size = frame_size

        # fetch window handle
        self.window_handle = self.find_game_window()
        #logging.debug("game window hex: %s" % (self.window_handle))

        # get screen coordinates of game window as (left, upper, right, lower)
        self.window_coords = self.get_game_window_coordinates()
        #logging.debug("game window coords: %s" % (self.window_coords,))

        # center mouse cursor to game crosshair
        self.center_cursor()

        # activate the game window to prepare for input
        self.activate_game_window()

        # calculate screen coordinates for screenshot box centered on crosshair
        self.frame_coords = self.calculate_frame_box(self.frame_size)
        #logging.debug("bounding box coords for frame is: %s" % (self.frame_coords))

    def find_game_window(self):
        """ finds minecraft game window and returns its handle """

        window_name = "Minecraft 1.8.8"
        handle = win32gui.FindWindow(None, window_name)
        return handle

    def activate_game_window(self):
        """ activates the game window with ID 'self.window_handle' """

        win32gui.SetForegroundWindow(self.window_handle)
        time.sleep(0.5) # activation can be slow sometimes

    def get_game_window_coordinates(self):
        """ returns a tuple with game window coordinates like so (left, upper, right, lower)"""

        window_rect = win32gui.GetWindowRect(self.window_handle)
        #logging.debug("GetWindowRect: %s" % (window_rect,))

        diff_coords = win32gui.ScreenToClient(self.window_handle, (window_rect[0], window_rect[1])) # returns negative values
        #logging.debug("ScreenToClient: %s" % (diff_coords,))

        client_rect = win32gui.GetClientRect(self.window_handle)
        #logging.debug("GetClientRect: %s" % (client_rect,))

        game_window_coords = (window_rect[0] - diff_coords[0],
                              window_rect[1] - diff_coords[1],
                              window_rect[2] + diff_coords[0],
                              window_rect[3] + diff_coords[0])

        return game_window_coords

    def calculate_frame_box(self, box_size):
        """ returns the screen coordinates for box of size 'frame_size' used in grab_frame """

        center = ((self.window_coords[2] - self.window_coords[0]) / 2,
                  (self.window_coords[3] - self.window_coords[1]) / 2)
        #logging.debug("center coordinate: %s" % (center,))

        box = (self.window_coords[0] + center[0] - (box_size / 2),
               self.window_coords[1] + center[1] - (box_size / 2) + 1,
               self.window_coords[0] + center[0] + (box_size / 2),
               self.window_coords[1] + center[1] + (box_size / 2) + 1) # +1 is correction for self.window_coords
        #logging.debug("box is: %s" % (box,))

        return box

    def center_cursor(self):
        """ centers mouse cursor to avoid in-game camera movement when activating game window """

        center_box = self.calculate_frame_box(0)
        crosshair = (center_box[0], center_box[1] - 1) # correction for self.window_coords
        #logging.debug("crosshair coords: %s" % (crosshair,))

        win32api.SetCursorPos(crosshair)
        time.sleep(0.05) # compensation for slow SetCursorPos function

    def grab_frame(self):
        """ returns RGB pixel matrix of size self.frame_size as numpy array
            20x20 bbox returns in 50-80ms """

        frame = ImageGrab.grab(self.frame_coords)
        #frame.show()
        return np.asarray(frame)





















