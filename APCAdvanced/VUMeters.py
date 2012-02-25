import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.SessionComponent import SessionComponent 
import math


# Constants. Tweaking these would let us work with different grid sizes or different templates

#Index of the columns used for VU display
A_COL = [4]
B_COL = [5]
C_COL = [6]
D_COL = [7]
# Which channels we are monitoring for RMS
A_SOURCE = 0
B_SOURCE  = 1
C_SOURCE = 2
D_SOURCE  = 3

# Grid size
CLIP_GRID_X = 8
CLIP_GRID_Y = 5

# Velocity values for clip colours. Different on some devices
LED_RED = 3
LED_ON = 127
LED_OFF = 0
LED_ORANGE = 5

# Scaling constants. Narrows the db range we display to 0db-21db or thereabouts
CHANNEL_SCALE_MAX = 0.92
CHANNEL_SCALE_MIN = 0.52
CHANNEL_SCALE_INCREMENTS = 10

MASTER_SCALE_MAX = 0.92
MASTER_SCALE_MIN = 0.52
MASTER_SCALE_INCREMENTS = 5

RMS_FRAMES = 2
USE_RMS = True

class VUMeter():
  'represents a single VU to store RMS values etc in'
  def __init__(self, parent, track, top, bottom, 
              increments, vu_set, master = False):

    self.frames = [0.0] * RMS_FRAMES
    self.parent = parent
    self.track = track
    self.top = top
    self.bottom = bottom
    self.multiplier = self.calculate_multiplier(top, bottom, increments)
    self.current_level = 0
    self.matrix = self.setup_matrix(vu_set, master)
    self.master = master

  def observe(self):
    new_frame = self.mean_peak() 
    self.store_frame(new_frame)
    if self.master and new_frame >= 0.92:
      self.parent._clipping = True
      self.parent.clip_warning()
    else:

      if self.master and self.parent._clipping:
        self.parent._parent._session._change_offsets(0, 1) 
        self.parent._parent._session._change_offsets(0, -1) 


        self.parent._clipping = False

      if not self.parent._clipping:
        if USE_RMS:
          level = self.scale(self.rms(self.frames))
        else:
          level = self.scale(new_frame)
        if level != self.current_level:
          self.current_level = level
          if self.master:
            self.parent.set_master_leds(level)
          else:
            self.parent.set_leds(self.matrix, level) 

  def store_frame(self, frame):
    self.frames.pop(0)
    self.frames.append(frame)

  def rms(self, frames):
    return math.sqrt(sum(frame*frame for frame in frames)/len(frames))

  # return the mean of the L and R peak values
  def mean_peak(self):
    return (self.track.output_meter_left + self.track.output_meter_right) / 2


  # Perform the scaling as per params. We reduce the range, then round it out to integers
  def scale(self, value):
    if (value > self.top):
      value = self.top
    elif (value < self.bottom):
      value = self.bottom
    value = value - self.bottom
    value = value * self.multiplier #float, scale 0-10
    return int(round(value))
  
  def calculate_multiplier(self, top, bottom, increments):
    return (increments / (top - bottom))


  # Goes from top to bottom: so clip grid, then stop, then select, then activator/solo/arm
  def setup_matrix(self, vu_set, master):
    matrix = []
    if master:
      for scene in self.parent._parent._session._scenes:
        matrix.append(scene._launch_button)
    else:
      for index, column_index in enumerate(vu_set):
        matrix.append([])
        column = matrix[index]
        for row_index in range(CLIP_GRID_Y):
          column.append(self.parent._parent._button_rows[row_index][column_index])
        if master != True:
          strip = self.parent._parent._mixer.channel_strip(column_index)
          column.append(self.parent._parent._track_stop_buttons[column_index])
          column.extend([strip._select_button, strip._mute_button, strip._solo_button, strip._arm_button])
    return matrix


class VUMeters(ControlSurfaceComponent):
    'standalone class used to handle VU meters'

    def __init__(self, parent):
        # Boilerplate
        ControlSurfaceComponent.__init__(self)
        self._parent = parent

        # Default the L/R/Master levels to 0
        self._meter_level = 0
        self._a_level = 0
        self._b_level = 0
        self._c_level = 0
        self._d_level = 0

        # We don't start clipping
        self._clipping = False

        # The tracks we'll be pulling L and R RMS from
        self._a_track = self.song().tracks[A_SOURCE]
        self._b_track = self.song().tracks[B_SOURCE]
        self._c_track = self.song().tracks[C_SOURCE]
        self._d_track = self.song().tracks[D_SOURCE]
        
        #setup classes
        self.a_meter = VUMeter(self, self._a_track, 
                                  CHANNEL_SCALE_MAX, 
                                  CHANNEL_SCALE_MIN, CHANNEL_SCALE_INCREMENTS,
                                  A_COL)
        self.b_meter = VUMeter(self, self._b_track, 
                                  CHANNEL_SCALE_MAX, 
                                  CHANNEL_SCALE_MIN, CHANNEL_SCALE_INCREMENTS,
                                  B_COL)
        self.c_meter = VUMeter(self, self._c_track, 
                                  CHANNEL_SCALE_MAX, 
                                  CHANNEL_SCALE_MIN, CHANNEL_SCALE_INCREMENTS,
                                  C_COL)
        self.d_meter = VUMeter(self, self._d_track, 
                                  CHANNEL_SCALE_MAX, 
                                  CHANNEL_SCALE_MIN, CHANNEL_SCALE_INCREMENTS,
                                  D_COL)
        self.master_meter = VUMeter(self, self.song().master_track,
                                    MASTER_SCALE_MAX,
                                    MASTER_SCALE_MIN, MASTER_SCALE_INCREMENTS,
                                    None, True)
        # Listeners!
        self._a_track.add_output_meter_left_listener(self.a_meter.observe)
        self._b_track.add_output_meter_left_listener(self.b_meter.observe)
        self._c_track.add_output_meter_left_listener(self.c_meter.observe)
        self._d_track.add_output_meter_left_listener(self.d_meter.observe)

        self.song().master_track.add_output_meter_left_listener(self.master_meter.observe)

    # If you fail to kill the listeners on shutdown, Ableton stores them in memory and punches you in the face
    def disconnect(self):
        self._a_track.remove_output_meter_left_listener(self.a_meter.observe)
        self._b_track.remove_output_meter_left_listener(self.b_meter.observe)
        self._c_track.remove_output_meter_left_listener(self.c_meter.observe)
        self._d_track.remove_output_meter_left_listener(self.d_meter.observe)

        self.song().master_track.remove_output_meter_left_listener(self.master_meter.observe)

    # Called when the Master clips. Makes the entire clip grid BRIGHT RED 
    def clip_warning(self):
      for row_index in range(CLIP_GRID_Y):
        row = self._parent._button_rows[row_index]
        for button_index in range(CLIP_GRID_X):
          button = row[button_index]
          # Passing True to send_value forces it to happen even when the button in question is MIDI mapped
          button.send_value(LED_RED, True)

    def set_master_leds(self, level):
        for scene_index in range(CLIP_GRID_Y):
            scene = self._parent._session.scene(scene_index)
            if scene_index >= (CLIP_GRID_Y - level):
              scene._launch_button.send_value(LED_ON, True)
            else:
              scene._launch_button.send_value(LED_OFF, True)


    # Iterate through every column in the matrix, light up the LEDs based on the level
    # Level for channels is scaled to 10 cos we have 10 LEDs
    # Top two LEDs are red, the next is orange
    def set_leds(self, matrix, level):
        for column in matrix:
          for index in range(10):
            button = column[index] 
            if index >= (10 - level): 
              if index < 1:
                button.send_value(LED_RED, True)
              elif index < 2:
                button.send_value(LED_ORANGE, True)
              else:
                button.send_value(LED_ON, True)
            else:
              button.send_value(LED_OFF, True)

    # boilerplate
    def update(self):
        pass

    def on_enabled_changed(self):
        self.update()

    def on_selected_track_changed(self):
        self.update()

    def on_track_list_changed(self):
        self.update()

    def on_selected_scene_changed(self):
        self.update()

    def on_scene_list_changed(self):

        self.update()









