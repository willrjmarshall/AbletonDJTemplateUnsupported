
import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent 
from EncoderUserModesComponent import EncoderUserModesComponent #added
from PedaledSessionComponent import PedaledSessionComponent #added
from _Framework.SessionZoomingComponent import SessionZoomingComponent #added
#from consts import * #see below (not used)
#MANUFACTURER_ID = 71
#ABLETON_MODE = 65
#NOTE_MODE = 65 #67 = APC20 Note Mode; 65 = APC40 Ableton Mode 1

class ShiftableSelectorComponent(ModeSelectorComponent):
    __doc__ = ' SelectorComponent that assigns buttons to functions based on the shift button '
    #def __init__(self, select_buttons, master_button, arm_buttons, matrix, session, zooming, mixer, transport, slider_modes, mode_callback):
    def __init__(self, parent, select_buttons, master_button, arm_buttons, matrix, session, zooming, mixer, slider_modes, matrix_modes):
        if not len(select_buttons) == 8:
            raise AssertionError
        if not len(arm_buttons) == 8:
            raise AssertionError
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False
        self._note_mode_active = False
        self._invert_assignment = False
        self._select_buttons = select_buttons
        self._master_button = master_button
        self._slider_modes = slider_modes
        self._matrix_modes = matrix_modes #added new        
        self._arm_buttons = arm_buttons
        #self._transport = transport
        self._session = session
        self._zooming = zooming
        self._matrix = matrix
        self._mixer = mixer
        #self._master_button.add_value_listener(self._master_value)
        self._parent = parent #use this to call methods of parent class (APC40plus21)


    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        #self._master_button.remove_value_listener(self._master_value)
        self._select_buttons = None
        self._master_button = None
        self._slider_modes = None
        self._matrix_modes = None #added
        self._arm_buttons = None
        #self._transport = None
        self._session = None
        self._zooming = None
        self._matrix = None
        self._mixer = None
        self._parent = None #added
        return None

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button) #called from APC40_22: self._shift_modes.set_mode_toggle(self._shift_button)
        self.set_mode(0)

    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()

    def number_of_modes(self):
        return 2

    def update(self):
        if self.is_enabled():
            if self._mode_index == int(self._invert_assignment):
                self._slider_modes.set_mode_buttons(None)
                self._matrix_modes.set_mode_buttons(None)
                for index in range(len(self._arm_buttons)): #was: for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(self._arm_buttons[index])
                    self._mixer.channel_strip(index).set_select_button(self._select_buttons[index])
            else:
                for index in range(len(self._arm_buttons)): #was: for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_select_button(None)
                self._slider_modes.set_mode_buttons(self._arm_buttons)
                self._matrix_modes.set_mode_buttons(self._select_buttons)
        return None

    def _partial_refresh(self, value):
        #for control in self._parent.controls:
            #control.clear_send_cache()   
        for component in self._parent.components:
            if isinstance(component, PedaledSessionComponent) or isinstance(component, SessionZoomingComponent):
                component.update()


    def _toggle_value(self, value): #"toggle" is shift button
        if not self._mode_toggle != None:
            raise AssertionError
        if not value in range(128):
            raise AssertionError
        self._toggle_pressed = value > 0
        self._recalculate_mode()
        if value < 1 and self._matrix_modes._last_mode > 1: #refresh on Shift button release, and if previous mode was Note Mode
            self._parent.schedule_message(2, self._partial_refresh, value)
        return None


    def _recalculate_mode(self): #called if toggle (i.e. shift) is pressed
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())



