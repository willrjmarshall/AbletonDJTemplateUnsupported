# emacs-mode: -*- python-*-
# http://remotescripts.blogspot.com

import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.MixerComponent import MixerComponent 
from _Framework.DeviceComponent import DeviceComponent

class EncoderDeviceComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = " Class representing encoder Device component "

    def __init__(self, mixer, device, parent):
        ControlSurfaceComponent.__init__(self)
        assert isinstance(mixer, MixerComponent)
        self._param_controls = None
        self._mixer = mixer
        self._buttons = []
        self._lock_button = None
        self._last_mode = 0
        self._is_locked = False
        self._ignore_buttons = False
        self._track = None
        self._strip = None
        self._parent = parent
        self._device = device
        self._alt_device = DeviceComponent()
        self._alt_device.name = 'Alt_Device_Component'
        self.song().add_appointed_device_listener(self._on_device_changed)

    def disconnect(self):
        self.song().remove_appointed_device_listener(self._on_device_changed)
        self._param_controls = None
        self._mixer = None
        self._buttons = None
        self._lock_button = None
        self._track = None
        self._strip = None
        self._parent = None
        self._device = None
        self._alt_device = None

    def update(self):
        pass
        #self._show_msg_callback("EncoderDeviceComponent update called")


    def set_controls_and_buttons(self, controls, buttons):
        assert ((controls == None) or (isinstance(controls, tuple) and (len(controls) == 8)))
        self._param_controls = controls
        assert ((buttons == None) or (isinstance(buttons, tuple)) or (len(buttons) == 4))
        self._buttons = buttons
        self.set_lock_button(self._buttons[0])

        if self._is_locked == True:
            self._alt_device.set_parameter_controls(self._param_controls)  
            self._alt_device.set_bank_nav_buttons(self._buttons[2], self._buttons[3])
            self._alt_device.set_on_off_button(self._buttons[1])
        else:
            self.on_selected_track_changed()


    def _on_device_changed(self):
        if self.is_enabled():
            if self._is_locked != True:
                selected_device= self.song().appointed_device
                self._alt_device.set_device(selected_device)
                self._setup_controls_and_buttons()


    def on_selected_track_changed(self):
        if self.is_enabled():
            if self._is_locked != True:
                track = self.song().view.selected_track
                selected_device = track.view.selected_device
                self._alt_device.set_device(selected_device)
                self._setup_controls_and_buttons()


    def _setup_controls_and_buttons(self):
        if self._buttons != None and self._param_controls != None:
            if self._alt_device != None:
                self._alt_device.set_parameter_controls(self._param_controls)  
                self._alt_device.set_bank_nav_buttons(self._buttons[2], self._buttons[3])
                self._alt_device.set_on_off_button(self._buttons[1])
            self._alt_device._on_on_off_changed()

            self._rebuild_callback()


    def on_enabled_changed(self):
        self.update()  


    def set_lock_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._lock_button != None):
            self._lock_button.remove_value_listener(self._lock_value)
            self._lock_button = None
        self._lock_button = button
        if (self._lock_button != None):
            self._lock_button.add_value_listener(self._lock_value)
            if self._is_locked:
                self._lock_button.turn_on()
            else:
                self._lock_button.turn_off()            


    def _lock_value(self, value):
        assert (self._lock_button != None)
        assert (value != None)
        assert isinstance(value, int)
        if ((not self._lock_button.is_momentary()) or (value is not 0)):
            if self._ignore_buttons == False:
                if self._is_locked:
                    self._is_locked = False
                    self._lock_button.turn_off()
                    self.on_selected_track_changed()
                else:
                    self._is_locked = True
                    self._lock_button.turn_on()



# local variables:
# tab-width: 4
