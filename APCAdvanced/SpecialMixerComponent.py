# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from _Framework.MixerComponent import MixerComponent 
from SpecialChannelStripComponent import SpecialChannelStripComponent 
from _Framework.ButtonElement import ButtonElement #added
from _Framework.EncoderElement import EncoderElement #added    

class SpecialMixerComponent(MixerComponent):
    ' Special mixer class that uses return tracks alongside midi and audio tracks, and only maps prehear when not shifted '
    __module__ = __name__

    def __init__(self, parent, num_tracks):
        self._is_locked = False #added
        self._parent = parent #added
        MixerComponent.__init__(self, num_tracks)
        self._shift_button = None #added
        self._pedal = None
        self._shift_pressed = False #added
        self._pedal_pressed = False #added



    def disconnect(self): #added
        MixerComponent.disconnect(self)
        if (self._shift_button != None):
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        if (self._pedal != None):
            self._pedal.remove_value_listener(self._pedal_value)
            self._pedal = None


    def set_shift_button(self, button): #added
        assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
        if (self._shift_button != button):
            if (self._shift_button != None):
                self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = button
            if (self._shift_button != None):
                self._shift_button.add_value_listener(self._shift_value)
            self.update()

    def set_pedal(self, pedal):
        assert ((pedal == None) or (isinstance(pedal, ButtonElement) and pedal.is_momentary()))
        if (self._pedal != pedal):
            if (self._pedal != None):
                self._pedal.remove_value_listener(self._pedal_value)
            self._pedal = pedal
            if (self._pedal != None):
                self._pedal.add_value_listener(self._pedal_value)
            self.update()


    def _shift_value(self, value): #added
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = (value != 0)
        self.update()

    def _pedal_value(self, value): #added
        assert (self._pedal != None)
        assert (value in range(128))
        self._pedal_pressed = (value == 0)
        self.update()


    def on_selected_track_changed(self): #added override
        selected_track = self.song().view.selected_track
        if (self._selected_strip != None):
            if self._is_locked == False: #added
                self._selected_strip.set_track(selected_track)
        if self.is_enabled():
            if (self._next_track_button != None):
                if (selected_track != self.song().master_track):

                    self._next_track_button.turn_on()
                else:
                    self._next_track_button.turn_off()
            if (self._prev_track_button != None):
                if (selected_track != self.song().tracks[0]):
                    self._prev_track_button.turn_on()
                else:
                    self._prev_track_button.turn_off()        



    def update(self): #added override
        if self._allow_updates:
            master_track = self.song().master_track
            if self.is_enabled():
                if (self._prehear_volume_control != None):
                    #if self._shift_pressed: #added
                    if not self._shift_pressed and not self._pedal_pressed: #added 
                        self._prehear_volume_control.connect_to(master_track.mixer_device.cue_volume)
                    else:
                        self._prehear_volume_control.release_parameter() #added        
                if (self._crossfader_control != None):
                    self._crossfader_control.connect_to(master_track.mixer_device.crossfader)
            else:
                if (self._prehear_volume_control != None):
                    self._prehear_volume_control.release_parameter()
                if (self._crossfader_control != None):
                    self._crossfader_control.release_parameter()
                if (self._bank_up_button != None):
                    self._bank_up_button.turn_off()
                if (self._bank_down_button != None):
                    self._bank_down_button.turn_off()
                if (self._next_track_button != None):
                    self._next_track_button.turn_off()
                if (self._prev_track_button != None):
                    self._prev_track_button.turn_off()
            #self._rebuild_callback()
        else:
            self._update_requests += 1


    def tracks_to_use(self):
        return (self.song().visible_tracks + self.song().return_tracks)



    def _create_strip(self):
        return SpecialChannelStripComponent()


    def set_track_offset(self, new_offset): #added override
        MixerComponent.set_track_offset(self, new_offset)
        if self._parent._slider_modes != None:
            self._parent._slider_modes.update()
        if self._parent._encoder_modes != None:
            self._parent._encoder_modes.update()


# local variables:
# tab-width: 4
