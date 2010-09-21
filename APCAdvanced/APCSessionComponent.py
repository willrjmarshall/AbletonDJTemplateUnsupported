# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live 
from _Framework.SessionComponent import SessionComponent 
from _Framework.CompoundComponent import CompoundComponent #added
#from SpecialClipSlotComponent import SpecialClipSlotComponent #added
from _Framework.SceneComponent import SceneComponent #added
from _Framework.ClipSlotComponent import ClipSlotComponent #added

class APCSessionComponent(SessionComponent):
    " Special SessionComponent for the APC controllers' combination mode "
    __module__ = __name__

    def __init__(self, num_tracks, num_scenes):
        SessionComponent.__init__(self, num_tracks, num_scenes)
    #def __init__(self, num_tracks, num_scenes):
        #if not SessionComponent._session_highlighting_callback != None:
            #raise AssertionError
        #if not isinstance(num_tracks, int):
            #isinstance(num_tracks, int)
            #raise AssertionError
        #isinstance(num_tracks, int)
        #if not num_tracks >= 0:
            #raise AssertionError
        #if not isinstance(num_scenes, int):
            #isinstance(num_scenes, int)
            #raise AssertionError
        #isinstance(num_scenes, int)
        #if not num_scenes >= 0:
            #raise AssertionError
        #CompoundComponent.__init__(self)
        #self._track_offset = -1
        #self._scene_offset = -1
        #self._num_tracks = num_tracks
        #self._bank_up_button = None
        #self._bank_down_button = None
        #self._bank_right_button = None
        #self._bank_left_button = None
        #self._stop_all_button = None
        #self._next_scene_button = None
        #self._prev_scene_button = None
        #self._stop_track_clip_buttons = None
        #self._scroll_up_ticks_delay = -1
        #self._scroll_down_ticks_delay = -1
        #self._scroll_right_ticks_delay = -1
        #self._scroll_left_ticks_delay = -1
        #self._stop_track_clip_value = 127
        #self._offset_callback = None
        #self._highlighting_callback = SessionComponent._session_highlighting_callback
        #if num_tracks > 0:
            #pass
        #self._show_highlight = num_tracks > 0
        #self._mixer = None
        #self._selected_scene = SpecialSceneComponent(self._num_tracks, self.tracks_to_use)
        #self.on_selected_scene_changed()
        #self.register_components(self._selected_scene)
        #self._scenes = []
        #self._tracks_and_listeners = []
        #for index in range(num_scenes):
            #self._scenes.append(self._create_scene(self._num_tracks))
            #self.register_components(self._scenes[index])
        #self.set_offsets(0, 0)
        #self._register_timer_callback(self._on_timer)
        #return None

    #def _create_scene(self, num_tracks):
        #return SpecialSceneComponent(self.tracks_to_use)    
    
    def link_with_track_offset(self, track_offset):
        assert (track_offset >= 0)
        if self._is_linked():
            self._unlink()
        self._change_offsets(track_offset, 0)
        self._link()


# local variables:
# tab-width: 4

#class SpecialSceneComponent(SceneComponent):

    #def __init__(self, num_slots, tracks_to_use_callback):
        #SceneComponent.__init__(self, num_slots, tracks_to_use_callback)

    #def _create_clip_slot(self):
        #return ClipSlotComponent()


#class SpecialClipSlotComponent(ClipSlotComponent):

    #def __init__(self):
        #ClipSlotComponent.__init__(self)


    #def update(self):
        #self._has_fired_slot = False
        #if (self.is_enabled() and (self._launch_button != None)):
            #self._launch_button.turn_off()
            #value_to_send = -1
            #if (self._clip_slot != None):
                #if self.has_clip():
                    #value_to_send = self._stopped_value
                    #if self._clip_slot.clip.is_triggered:
                        #if self._clip_slot.clip.will_record_on_start:
                            #value_to_send = self._triggered_to_record_value
                        #else:
                            #value_to_send = self._triggered_to_play_value
                    #elif self._clip_slot.clip.is_playing:
                        #if self._clip_slot.clip.is_recording:
                            #value_to_send = self._recording_value
                        #else:
                            #value_to_send = self._started_value
                #elif self._clip_slot.is_triggered:
                    #if self._clip_slot.will_record_on_start:
                        #value_to_send = self._triggered_to_record_value
                    #else:
                        #value_to_send = self._triggered_to_play_value
                #if (value_to_send in range(128)):
                    #self._launch_button.send_value(value_to_send, True)