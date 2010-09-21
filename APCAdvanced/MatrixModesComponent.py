# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

from _Framework.ModeSelectorComponent import ModeSelectorComponent 
from _Framework.ButtonElement import ButtonElement 
from _Framework.MixerComponent import MixerComponent 
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from Matrix_Maps import *

class MatrixModesComponent(ModeSelectorComponent):
    ' SelectorComponent that assigns matrix to different functions '
    __module__ = __name__

    def __init__(self, matrix, session, zooming, stop_buttons, parent):
        assert isinstance(matrix, ButtonMatrixElement)
        ModeSelectorComponent.__init__(self)
        self._controls = None
        self._session = session
        self._session_zoom = zooming
        self._matrix = matrix
        self._track_stop_buttons = stop_buttons
        self._stop_button_matrix = ButtonMatrixElement() #new dummy matrix for stop buttons, to allow note mode/user mode switching
        button_row = []
        for track_index in range(8):
            button = self._track_stop_buttons[track_index]
            button_row.append(button)
        self._stop_button_matrix.add_row(tuple(button_row))
        self._mode_index = 0
        self._last_mode = 0
        self._parent = parent
        self._parent.set_pad_translations(PAD_TRANSLATIONS) #comment out to remove Drum Rack mapping

        
    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._controls = None
        self._session = None
        self._session_zoom = None
        self._matrix = None
        self._track_stop_buttons = None
        self._stop_button_matrix = None
        ModeSelectorComponent.disconnect(self)

        
    def set_mode(self, mode): #override ModeSelectorComponent set_mode, to avoid flickers
        assert isinstance(mode, int)
        assert (mode in range(self.number_of_modes()))
        if (self._mode_index != mode):
            self._last_mode = self._mode_index # keep track of previous mode, to allow refresh after Note Mode only
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
            for index in range(len(self._modes_buttons)):
                if (index == self._mode_index):
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()


    def number_of_modes(self):
        return 8

    
    def update(self):
        pass

    
    def _set_modes(self):
        if self.is_enabled():
            self._session.set_allow_update(False)
            self._session_zoom.set_allow_update(False)
            assert (self._mode_index in range(self.number_of_modes()))
            for index in range(len(self._modes_buttons)):
                if (index == self._mode_index):
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()
            self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))            
            for track_index in range(8):
                button = self._track_stop_buttons[track_index]
                button.use_default_message()
                button.set_enabled(True)
                button.set_force_next_value()
                button.send_value(0)
            self._session_zoom.set_enabled(True)
            self._session.set_enabled(True)
            self._session.set_show_highlight(True)
            self._session_zoom.set_zoom_button(self._parent._shift_button)
            for scene_index in range(5):
                scene = self._session.scene(scene_index) 
                for track_index in range(8):                
                    button = self._matrix.get_button(track_index, scene_index)
                    button.use_default_message()
                    clip_slot = scene.clip_slot(track_index)
                    clip_slot.set_launch_button(button)
                    button.set_enabled(True)
                
            if (self._mode_index == 0): #Clip Launch
                self._session_zoom._zoom_value(1) #zoom out
                pass
                        
            elif (self._mode_index == 1): #Session Overview
                self._session_zoom.set_enabled(True)
                self._session_zoom._is_zoomed_out = True
                self._session_zoom._scene_bank_index = int(((self._session_zoom._session.scene_offset() / self._session_zoom._session.height()) / self._session_zoom._buttons.height()))               
                self._session.set_enabled(False)
                self._session_zoom.update()
                self._session_zoom.set_zoom_button(None)
    
            elif (self._mode_index == 2):
                self._set_note_mode(PATTERN_1, CHANNEL_1, NOTEMAP_1, USE_STOP_ROW_1, IS_NOTE_MODE_1)
            elif (self._mode_index == 3):
                self._set_note_mode(PATTERN_2, CHANNEL_2, NOTEMAP_2, USE_STOP_ROW_2, IS_NOTE_MODE_2)
            elif (self._mode_index == 4):
                self._set_note_mode(PATTERN_3, CHANNEL_3, NOTEMAP_3, USE_STOP_ROW_3, IS_NOTE_MODE_3)
            elif (self._mode_index == 5):
                self._set_note_mode(PATTERN_4, CHANNEL_4, NOTEMAP_4, USE_STOP_ROW_4, IS_NOTE_MODE_4)
            elif (self._mode_index == 6):
                self._set_note_mode(PATTERN_5, CHANNEL_5, NOTEMAP_5, USE_STOP_ROW_5, IS_NOTE_MODE_5)
            elif (self._mode_index == 7):
                self._set_note_mode(PATTERN_6, CHANNEL_6, NOTEMAP_6, USE_STOP_ROW_6, IS_NOTE_MODE_6)
            else:
                pass #assert False
            self._session.set_allow_update(True)
            self._session_zoom.set_allow_update(True)
            self._rebuild_callback()


    def _set_note_mode(self, pattern, channel, notemap, use_stop_row = False, is_note_mode = True):
        self._session_zoom.set_zoom_button(None)
        self._session_zoom.set_enabled(False)
        for scene_index in range(5):
            scene = self._session.scene(scene_index) 
            for track_index in range(8):
                clip_slot = scene.clip_slot(track_index)
                button = self._matrix.get_button(track_index, scene_index)
                clip_slot.set_launch_button(None)
                button.set_channel(channel) #remap all Note Mode notes to new channel
                button.set_identifier(notemap[scene_index][track_index])
                #button.send_value(pattern[scene_index][track_index], True)
                button.set_on_off_values(pattern[scene_index][track_index], 0)
                button.set_force_next_value()
                button.turn_on()
                #button.turn_off()
                if is_note_mode == True:
                    button.set_enabled(False)
        if use_stop_row == True:
            self._session.set_stop_track_clip_buttons(None)
            for track_index in range(8):
                button = self._stop_button_matrix.get_button(track_index, 0)
                button.set_channel(channel) #remap all Note Mode notes to new channel
                button.set_identifier(notemap[5][track_index])
                button.set_force_next_value()
                button.send_value(pattern[5][track_index])
                #button.receive_value(pattern[5][track_index]) #TODO - feedback?
                if is_note_mode == True:
                    button.set_enabled(False)
        else:
            #self._session.set_enabled(True)
            for track_index in range(8):
                button = self._stop_button_matrix.get_button(track_index, 0)
                button.send_value(0, True)
        self._session.set_enabled(True)
        self._session.set_show_highlight(True)

# local variables:
# tab-width: 4
