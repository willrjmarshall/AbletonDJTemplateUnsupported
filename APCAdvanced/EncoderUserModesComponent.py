
import Live 
from _Framework.ModeSelectorComponent import ModeSelectorComponent 
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent

class EncoderUserModesComponent(ModeSelectorComponent):
    ' SelectorComponent that assigns encoders to different user functions '
    __module__ = __name__

    def __init__(self, parent, encoder_modes, param_controls, bank_buttons, mixer, device, encoder_device_modes, encoder_eq_modes): #, mixer, sliders):
        assert (len(bank_buttons) == 4)
        ModeSelectorComponent.__init__(self)
        self._parent = parent
        self._encoder_modes = encoder_modes  
        self._param_controls = param_controls
        self._bank_buttons = bank_buttons
        self._mixer = mixer
        self._device = device
        self._encoder_device_modes = encoder_device_modes
        self._encoder_eq_modes = encoder_eq_modes
        self._mode_index = 0
        self._modes_buttons = []
        self._user_buttons = []
        self._last_mode = 0


    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._parent = None
        self._encoder_modes = None
        self._param_controls = None
        self._bank_buttons = None
        self._mixer = None
        self._device = None
        self._encoder_device_modes = None
        self._encoder_eq_modes = None
        self._modes_buttons = None
        self._user_buttons = None

    def on_enabled_changed(self):
        pass

    def set_mode(self, mode):
        assert isinstance(mode, int)
        assert (mode in range(self.number_of_modes()))
        if (self._mode_index != mode):
            self._last_mode = self._mode_index # keep track of previous mode, to allow conditional actions
            self._mode_index = mode
            self._set_modes()


    def set_mode_buttons(self, buttons):
        assert isinstance(buttons, (tuple,
                                    type(None)))
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)  

        self._modes_buttons = []
        if (buttons != None):
            for button in buttons:
                assert isinstance(button, ButtonElement)
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)
            assert (self._mode_index in range(self.number_of_modes()))


    def number_of_modes(self):
        return 4


    def update(self):
        pass


    def _mode_value(self, value, sender):
        assert (len(self._modes_buttons) > 0)
        assert isinstance(value, int)
        assert isinstance(sender, ButtonElement)
        assert (self._modes_buttons.count(sender) == 1)
        if ((value is not 0) or (not sender.is_momentary())):
            self.set_mode(self._modes_buttons.index(sender))    


    def _set_modes(self):
        if self.is_enabled():
            assert (self._mode_index in range(self.number_of_modes()))
            for index in range(len(self._modes_buttons)):
                if (index <= self._mode_index):
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()
            for button in self._modes_buttons:
                button.release_parameter()
                button.use_default_message()
            for control in self._param_controls:
                control.release_parameter()
                control.use_default_message()
                #control.set_needs_takeover(False)
            self._encoder_modes.set_enabled(False)
            
            self._encoder_device_modes.set_lock_button(None)
            self._encoder_device_modes._alt_device.set_bank_nav_buttons(None, None)
            self._encoder_device_modes._alt_device.set_on_off_button(None)
            if self._encoder_device_modes._alt_device._parameter_controls != None:
                for control in self._encoder_device_modes._alt_device._parameter_controls:
                    control.release_parameter()
            self._encoder_device_modes.set_enabled(False)
            
            self._encoder_eq_modes.set_enabled(False)
            self._encoder_eq_modes.set_lock_button(None)
            if self._encoder_eq_modes._track_eq != None:
                self._encoder_eq_modes._track_eq.set_cut_buttons(None)
                if self._encoder_eq_modes._track_eq._gain_controls != None:
                    for control in self._encoder_eq_modes._track_eq._gain_controls:
                        control.release_parameter()  
            if self._encoder_eq_modes._strip != None:
                self._encoder_eq_modes._strip.set_send_controls(None)              
            
            self._user_buttons = []

            if (self._mode_index == 0):               
                self._encoder_modes.set_enabled(True)

            elif (self._mode_index == 1):
                self._encoder_device_modes.set_enabled(True)
                self._encoder_device_modes.set_controls_and_buttons(self._param_controls, self._modes_buttons)

            elif (self._mode_index == 2):
                self._encoder_eq_modes.set_enabled(True)
                self._encoder_eq_modes.set_controls_and_buttons(self._param_controls, self._modes_buttons)


            elif (self._mode_index == 3):
                self._encoder_eq_modes._ignore_buttons = True
                if self._encoder_eq_modes._track_eq != None:
                    self._encoder_eq_modes._track_eq._ignore_cut_buttons = True
                self._encoder_device_modes._ignore_buttons = True
                for button in self._modes_buttons:
                    self._user_buttons.append(button)
                for control in self._param_controls:
                    control.set_identifier((control.message_identifier() - 9))
                    control._ring_mode_button.send_value(0)
            else:
                pass
            self._rebuild_callback()



# local variables:
# tab-width: 4
