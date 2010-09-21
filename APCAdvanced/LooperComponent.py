from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added    

class LooperComponent():
  'Handles looping controls'
  __module__ = __name__


  def __init__(self, parent):
    self._parent = parent
    self._loop_toggle_button = None
    self._loop_start_button = None
    self._loop_double_button = None
    self._loop_halve_button = None
    self._loop_length = 64
    self._loop_start = 0
    self._clip_length = 0
    self._shift_button = None
    self._current_clip = None
    self._shift_pressed = False

  def set_loop_toggle_button(self, button):
    assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
    if self._loop_toggle_button != button:
      if self._loop_toggle_button != None:
        self._loop_toggle_button.remove_value_listener(self.toggle_loop)
      self._loop_toggle_button = button
      if (self._loop_toggle_button != None):
        self._loop_toggle_button.add_value_listener(self.toggle_loop)


  def toggle_loop(self, value):
    if value == 1: 
      self.get_current_clip()
      if self._current_clip != None:
        current_clip = self._current_clip
        if not self._shift_pressed:
          if current_clip.looping == 1:
            current_clip.looping = 0
          else:
            self._clip_length = current_clip.length
            current_clip.looping = 1
        else:
          was_playing = current_clip.looping
          current_clip.looping = 1
          if current_clip.loop_start >= 32.0:
            current_clip.loop_end = current_clip.loop_end - 32.0
            current_clip.loop_start = current_clip.loop_start - 32.0 
          else:
            current_clip.loop_end = 0.0 + self._loop_length
            current_clip.loop_start = 0.0
          if was_playing == 0:
            current_clip.looping = 0


  def set_loop_start_button(self, button):
    assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
    if self._loop_start_button != button:
      if self._loop_start_button != None:
        self._loop_start_button.remove_value_listener(self.move_loop_start)
      self._loop_start_button = button
      if (self._loop_start_button != None):
        self._loop_start_button.add_value_listener(self.move_loop_start)

  def move_loop_start(self, value):
    if value == 1: 
      self.get_current_clip()
      if self._current_clip != None:
        current_clip = self._current_clip
        if not self._shift_pressed:
          self._loop_start = round(current_clip.playing_position / 4.0) * 4
          was_playing = current_clip.looping
          current_clip.looping = 1
          current_clip.loop_end = self._loop_start + self._loop_length
          current_clip.loop_start = self._loop_start
          # Twice to fix a weird bug
          current_clip.loop_end = self._loop_start + self._loop_length
          if was_playing == 0:
            current_clip.looping = 0
        else:
          was_playing = current_clip.looping
          current_clip.looping = 1
          current_clip.loop_end = current_clip.loop_end + 32.0
          current_clip.loop_start = current_clip.loop_start + 32.0
          if was_playing == 0:
            current_clip.looping = 0

  def set_loop_double_button(self, button):
    assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
    if self._loop_double_button != button:
      if self._loop_double_button != None:
        self._loop_double_button.remove_value_listener(self.increase_loop)
      self._loop_double_button = button
      if (self._loop_double_button != None):
        self._loop_double_button.add_value_listener(self.increase_loop)

  # Doubles loop without shift
  # Moves loop one bar right with shift
  def increase_loop(self, value):
    if value == 1: 
      self.get_current_clip()
      if self._current_clip != None:
        current_clip = self._current_clip
        was_playing = current_clip.looping
        current_clip.looping = 1
        if not self._shift_pressed:
          if self._loop_length <= 128:
            self._loop_length = self._loop_length * 2.0
          else:
            self._loop_length = self._loop_length + 16 
          current_clip.loop_end = current_clip.loop_start + self._loop_length
        else:
          current_clip.loop_end = current_clip.loop_end + 4.0
          current_clip.loop_start = current_clip.loop_start + 4.0
        if was_playing == 0:
          current_clip.looping = 0


  def set_loop_halve_button(self, button):
    assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
    if self._loop_halve_button != button:
      if self._loop_halve_button != None:
        self._loop_halve_button.remove_value_listener(self.decrease_loop)
      self._loop_halve_button = button
      if (self._loop_halve_button != None):
        self._loop_halve_button.add_value_listener(self.decrease_loop)

  # halves loop without shift
  # left loop one bar right with shift
  def decrease_loop(self, value):
    if value == 1: 
      self.get_current_clip()
      if self._current_clip != None:
        current_clip = self._current_clip
        was_playing = current_clip.looping
        current_clip.looping = 1
        if not self._shift_pressed:
          if self._loop_length <= 128:
            self._loop_length = self._loop_length / 2.0
          else:
            self._loop_length = self._loop_length - 16 
          current_clip.loop_end = current_clip.loop_start + self._loop_length
        else:
          if current_clip.loop_start >= 4.0:
            current_clip.loop_end = current_clip.loop_end - 4.0
            current_clip.loop_start = current_clip.loop_start - 4.0
          else:
            current_clip.loop_end = 0.0 + self._loop_length 
            current_clip.loop_start = 0.0 
        if was_playing == 0:
          current_clip.looping = 0


  def get_current_clip(self):
    if (self._parent.song().view.highlighted_clip_slot != None):
      clip_slot = self._parent.song().view.highlighted_clip_slot
      if clip_slot.has_clip:
        self._current_clip = clip_slot.clip
      else:
        self._current_clip = None
    else:
      self._current_clip = None


  def set_shift_button(self, button): #added
      assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
      if (self._shift_button != button):
          if (self._shift_button != None):
              self._shift_button.remove_value_listener(self._shift_value)
          self._shift_button = button
          if (self._shift_button != None):
              self._shift_button.add_value_listener(self._shift_value)

  def _shift_value(self, value): #added
      assert (self._shift_button != None)
      assert (value in range(128))
      self._shift_pressed = (value != 0)
