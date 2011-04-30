# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from _Framework.ModeSelectorComponent import ModeSelectorComponent 
from _Framework.ButtonElement import ButtonElement 
from _Framework.MixerComponent import MixerComponent 
PAN_TO_VOL_DELAY = 5 #added delay value for _on_timer Pan/Vol Mode selection

class EncoderMixerModeSelectorComponent(ModeSelectorComponent):
    ' Class that reassigns encoders on the AxiomPro to different mixer functions '
    __module__ = __name__

    def __init__(self, mixer):
        assert isinstance(mixer, MixerComponent)
        ModeSelectorComponent.__init__(self)
        self._controls = None
        self._mixer = mixer
        self.set_mode(0) #moved here
        self._pan_to_vol_ticks_delay = -1 #added
        self._mode_is_pan = True #new
        self._register_timer_callback(self._on_timer) #added


    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._controls = None
        self._mixer = None
        self._unregister_timer_callback(self._on_timer) #added
        ModeSelectorComponent.disconnect(self)


    def set_modes_buttons(self, buttons):
        assert ((buttons == None) or (isinstance(buttons, tuple) or (len(buttons) == self.number_of_modes())))
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if (buttons != None):
            for button in buttons:
                assert isinstance(button, ButtonElement)
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)
        self.update()


    def set_controls(self, controls):
        assert ((controls == None) or (isinstance(controls, tuple) and (len(controls) == 8)))
        self._controls = controls
        self.update()


    def number_of_modes(self):
        return 4


    def _mode_value(self, value, sender):
        if self.is_enabled(): #added to ignore mode buttons when not enabled
            assert (len(self._modes_buttons) > 0)
            assert isinstance(value, int)
            assert isinstance(sender, ButtonElement)
            assert (self._modes_buttons.count(sender) == 1)
            if ((value is not 0) or (not sender.is_momentary())):
                self.set_mode(self._modes_buttons.index(sender))
            if self._modes_buttons.index(sender) == 0 and sender.is_momentary() and (value != 0): #added check for Pan button
                self._pan_to_vol_ticks_delay = PAN_TO_VOL_DELAY
            else:
                self._pan_to_vol_ticks_delay = -1

    def update(self):
        assert (self._modes_buttons != None)
        if self.is_enabled():
            if (self._modes_buttons != None):
                for button in self._modes_buttons:
                    if (self._modes_buttons.index(button) == self._mode_index):
                        button.turn_on()
                    else:
                        button.turn_off()

            if (self._controls != None):
                for index in range(len(self._controls)):
                    if (self._mode_index == 0):
                        if self._mode_is_pan == True: #added
                            self._mixer.channel_strip(index).set_volume_control(None)
                            self._mixer.channel_strip(index).set_pan_control(self._controls[index])
                        else:
                            self._mixer.channel_strip(index).set_pan_control(None)
                            self._mixer.channel_strip(index).set_volume_control(self._controls[index])
                        self._mixer.channel_strip(index).set_send_controls((None, None, None))
                    elif (self._mode_index == 1):
                        self._mixer.channel_strip(index).set_volume_control(None) #added
                        self._mixer.channel_strip(index).set_pan_control(None)
                        self._mixer.channel_strip(index).set_send_controls((self._controls[index],
                                                                            None,
                                                                            None))
                    elif (self._mode_index == 2):
                        self._mixer.channel_strip(index).set_volume_control(None) #added
                        self._mixer.channel_strip(index).set_pan_control(None)
                        self._mixer.channel_strip(index).set_send_controls((None,
                                                                            self._controls[index],
                                                                            None))
                    elif (self._mode_index == 3):
                        self._mixer.channel_strip(index).set_volume_control(None) #added
                        self._mixer.channel_strip(index).set_pan_control(None)
                        self._mixer.channel_strip(index).set_send_controls((None,
                                                                            None,
                                                                            self._controls[index]))
                    else:
                        pass
                        #print 'Invalid mode index'
                        #assert False
        else:
            for index in range(8):
                self._mixer.channel_strip(index).set_pan_control(None)
                self._mixer.channel_strip(index).set_send_controls((None, None, None))            
        #self._rebuild_callback()

        
    def _on_timer(self): #added to allow press & hold for Pan/Vol Mode selection
        if (self.is_enabled()):
            if (self._pan_to_vol_ticks_delay > -1):
                if (self._pan_to_vol_ticks_delay == 0):
                    self._mode_is_pan = not self._mode_is_pan
                    if self._mode_is_pan == True:
                        self._show_msg_callback("Set to Pan Mode")
                    else:
                        self._show_msg_callback("Set to Volume Mode")
                    self.update()
                self._pan_to_vol_ticks_delay -= 1

# local variables:
# tab-width: 4
