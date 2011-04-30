# emacs-mode: -*- python-*-
# http://remotescripts.blogspot.com

import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.MixerComponent import MixerComponent 
from _Framework.TrackEQComponent import TrackEQComponent
from _Framework.TrackFilterComponent import TrackFilterComponent

from _Generic.Devices import *
EQ_DEVICES = {'Eq8': {'Gains': [ ('%i Gain A' % (index + 1)) for index in range(8) ]},
              'FilterEQ3': {'Gains': ['GainLo',
                                      'GainMid',
                                      'GainHi'],
                            'Cuts': ['LowOn',
                                     'MidOn',
                                     'HighOn']}}
class SpecialTrackEQComponent(TrackEQComponent): #added to override _cut_value

    def __init__(self):
        TrackEQComponent.__init__(self)
        self._ignore_cut_buttons = False

    def _cut_value(self, value, sender):
        assert (sender in self._cut_buttons)
        assert (value in range(128))
        if self._ignore_cut_buttons == False: #added
            if (self.is_enabled() and (self._device != None)):
                if ((not sender.is_momentary()) or (value is not 0)):
                    device_dict = EQ_DEVICES[self._device.class_name]
                    if ('Cuts' in device_dict.keys()):
                        cut_names = device_dict['Cuts']
                        index = list(self._cut_buttons).index(sender)
                        if (index in range(len(cut_names))):
                            parameter = get_parameter_by_name(self._device, cut_names[index])
                            if (parameter != None):
                                parameter.value = float((int((parameter.value + 1)) % 2))


class EncoderEQComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = " Class representing encoder EQ component "

    def __init__(self, mixer, parent):
        ControlSurfaceComponent.__init__(self)
        assert isinstance(mixer, MixerComponent)
        self._param_controls = None
        self._mixer = mixer
        self._buttons = []
        self._param_controls = None
        self._lock_button = None
        self._last_mode = 0
        self._is_locked = False
        self._ignore_buttons = False
        self._track = None
        self._strip = None
        self._parent = parent
        self._track_eq = SpecialTrackEQComponent()
        self._track_filter = TrackFilterComponent()

    def disconnect(self):
        self._param_controls = None
        self._mixer = None
        self._buttons = None
        self._param_controls = None
        self._lock_button = None
        self._track = None
        self._strip = None
        self._parent = None
        self._track_eq = None
        self._track_filter = None

    def update(self):
        pass


    def set_controls_and_buttons(self, controls, buttons):
        assert ((controls == None) or (isinstance(controls, tuple) and (len(controls) == 8)))
        self._param_controls = controls
        assert ((buttons == None) or (isinstance(buttons, tuple)) or (len(buttons) == 4))
        self._buttons = buttons
        self.set_lock_button(self._buttons[0])
        self._update_controls_and_buttons()


    def _update_controls_and_buttons(self):
        #if self.is_enabled():
        if self._param_controls != None and self._buttons != None:
            if self._is_locked != True:
                self._track = self.song().view.selected_track
                self._track_eq.set_track(self._track)
                cut_buttons = [self._buttons[1], self._buttons[2], self._buttons[3]]
                self._track_eq.set_cut_buttons(tuple(cut_buttons))
                self._track_eq.set_gain_controls(tuple([self._param_controls[5], self._param_controls[6], self._param_controls[7]]))
                self._track_filter.set_track(self._track)
                self._track_filter.set_filter_controls(self._param_controls[0], self._param_controls[4])
                self._strip = self._mixer._selected_strip
                self._strip.set_send_controls(tuple([self._param_controls[1], self._param_controls[2], self._param_controls[3]]))         

            else:
                self._track_eq.set_track(self._track)
                cut_buttons = [self._buttons[1], self._buttons[2], self._buttons[3]]
                self._track_eq.set_cut_buttons(tuple(cut_buttons))
                self._track_eq.set_gain_controls(tuple([self._param_controls[5], self._param_controls[6], self._param_controls[7]]))
                self._track_filter.set_track(self._track)
                self._track_filter.set_filter_controls(self._param_controls[0], self._param_controls[4])
                ##self._strip = self._mixer._selected_strip
                self._strip.set_send_controls(tuple([self._param_controls[1], self._param_controls[2], self._param_controls[3]])) 
                ##pass               

        #self._rebuild_callback()


    def on_track_list_changed(self):
        self.on_selected_track_changed()


    def on_selected_track_changed(self):
        if self.is_enabled():
            if self._is_locked != True:
                self._update_controls_and_buttons()


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
        #if (value is not 0):
            if self._ignore_buttons == False:
                if self._is_locked:
                    self._is_locked = False
                    self._mixer._is_locked = False
                    self._lock_button.turn_off()
                    self._mixer.on_selected_track_changed()
                    self.on_selected_track_changed()
                else:
                    self._is_locked = True
                    self._mixer._is_locked = True
                    self._lock_button.turn_on()



# local variables:
# tab-width: 4
