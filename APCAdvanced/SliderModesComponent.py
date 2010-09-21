# emacs-mode: -*- python-*-

import Live 
from _Framework.ModeSelectorComponent import ModeSelectorComponent 
from _Framework.ButtonElement import ButtonElement 
class SliderModesComponent(ModeSelectorComponent):
    ' SelectorComponent that assigns sliders to different functions '
    __module__ = __name__

    def __init__(self, mixer, sliders):
        assert (len(sliders) == 8)
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._sliders = sliders
        self._mode_index = 0


    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._mixer = None
        self._sliders = None

        
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

        self.update()
        
        
    def number_of_modes(self):
        return 8


    def update(self):
        if self.is_enabled():
            assert (self._mode_index in range(self.number_of_modes()))
            for index in range(len(self._modes_buttons)):
                if (index == self._mode_index):
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

            for index in range(len(self._sliders)):
                strip = self._mixer.channel_strip(index)
                slider = self._sliders[index]
                slider.use_default_message()
                slider.set_identifier((slider.message_identifier() - self._mode_index))
                strip.set_volume_control(None)
                strip.set_pan_control(None)
                strip.set_send_controls((None, None, None))
                slider.release_parameter()
                if (self._mode_index == 0):
                    strip.set_volume_control(slider)
                elif (self._mode_index == 1):
                    strip.set_pan_control(slider)
                elif (self._mode_index < 5):
                    send_controls = [None,
                     None,
                     None]
                    send_controls[(self._mode_index - 2)] = slider
                    strip.set_send_controls(tuple(send_controls))
                self._rebuild_callback()


# local variables:
# tab-width: 4
