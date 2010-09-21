from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added    


class RepeatComponent():
  'Handles beat repeat controls'
  __module__ = __name__


  def __init__(self, parent):
    self._shift_button = None
    self._shift_pressed = False
    self._rack = None

    for device in parent.song().master_track.devices:
        if device.name == "Repeats":
            self._rack = device
            break
            
    if self._rack:
        for scene_index in range(5):
            scene = parent._session.scene(scene_index)
            button = scene._launch_button
            scene.set_launch_button(None)

            parent._device_buttons.append(button)
            button.add_value_listener(self._device_toggle, True)

  def _device_toggle(self, value, sender):
    if not self._shift_pressed:
      id = sender.message_identifier() - 82
      self._rack.parameters[id + 1].value = (value * 127)





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
