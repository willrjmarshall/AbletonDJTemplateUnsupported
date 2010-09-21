
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent 

class ShiftableEncoderSelectorComponent(ModeSelectorComponent):
    __doc__ = ' SelectorComponent that assigns encoders to functions based on the shift button '

    def __init__(self, parent, bank_buttons, encoder_user_modes, encoder_modes, encoder_eq_modes, encoder_device_modes):#, select_buttons, master_button, arm_buttons, matrix, session, zooming, mixer, slider_modes, matrix_modes): #, mode_callback):
        if not len(bank_buttons) == 4:
            raise AssertionError
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False
        self._invert_assignment = False
        self._parent = parent
        self._bank_buttons = bank_buttons        
        self._encoder_user_modes = encoder_user_modes
        self._encoder_modes = encoder_modes
        self._encoder_eq_modes = encoder_eq_modes
        self._encoder_device_modes = encoder_device_modes

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._parent = None #added
        self._bank_buttons = None #added
        self._encoder_modes = None
        self._encoder_user_modes = None
        self._encoder_eq_modes = None
        self._encoder_device_modes = None
        return None

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button) #called from parent: self._shift_modes.set_mode_toggle(self._shift_button)
        self.set_mode(0)

    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()

    def number_of_modes(self):
        return 2

    def update(self):
        if self.is_enabled():
            if self._mode_index == int(self._invert_assignment):
                self._encoder_user_modes.set_mode_buttons(None)
                self._encoder_modes.set_modes_buttons(self._bank_buttons)                                 
            else:
                self._encoder_modes.set_modes_buttons(None)
                self._encoder_user_modes.set_mode_buttons(self._bank_buttons)             
        return None
      
    
    def _toggle_value(self, value): #"toggle" is shift button
        if not self._mode_toggle != None:
            raise AssertionError
        if not value in range(128):
            raise AssertionError
        self._toggle_pressed = value > 0
        self._recalculate_mode()
        if value > 0:
            self._encoder_eq_modes._ignore_buttons = True
            if self._encoder_eq_modes._track_eq != None:
                self._encoder_eq_modes._track_eq._ignore_cut_buttons = True
            self._encoder_device_modes._ignore_buttons = True
            for button in self._encoder_user_modes._modes_buttons:
                button.use_default_message()
        else:
            self._encoder_eq_modes._ignore_buttons = False
            if self._encoder_eq_modes._track_eq != None:
                self._encoder_eq_modes._track_eq._ignore_cut_buttons = False
            self._encoder_device_modes._ignore_buttons = False
            if self._encoder_user_modes._mode_index == 3:
                for control in self._encoder_user_modes._param_controls:
                    control.set_channel(9 + self._encoder_user_modes._mode_index)
                if self._encoder_user_modes._user_buttons != None:
                    for button in self._encoder_user_modes._user_buttons:
                        button.turn_off()
                    for button in self._encoder_user_modes._user_buttons:
                        button.set_channel(9 + self._encoder_user_modes._mode_index) 

        return None

    
    def _recalculate_mode(self): #called if toggle (i.e. shift) is pressed
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())



        