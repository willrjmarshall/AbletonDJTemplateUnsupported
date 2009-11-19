"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Nathan Ramella <nar@remix.net> or visit http://www.remix.net

This script is based off the Ableton Live supplied MIDI Remote Scripts, customised
for OSC request delivery and response. This script can be run without any extra
Python libraries out of the box. 

This is the second file that is loaded, by way of being instantiated through
__init__.py

"""

import Live
import LiveOSCCallbacks
import RemixNet
import OSC
import LiveUtils
from Logger import Logger

class LiveOSC:
    __module__ = __name__
    __doc__ = "Main class that establishes the LiveOSC Component"
    
    # Enable Logging
    _LOG = 0
    
    clisten = {}
    slisten = {}
    mlisten = { "solo": {}, "mute": {}, "arm": {}, "panning": {}, "volume": {}, "sends": {}, "name": {} }
    rlisten = { "solo": {}, "mute": {}, "panning": {}, "volume": {}, "sends": {}, "name": {} }
    masterlisten = { "panning": {}, "volume": {}, "crossfader": {} }
    scenelisten = {}
    scene = 0

    def __init__(self, c_instance):
        self._LiveOSC__c_instance = c_instance
      
        self.basicAPI = 0       
        self.oscServer = RemixNet.OSCServer('localhost')
        self.oscServer.sendOSC('/remix/oscserver/startup', 1)
        
        self.logger = self._LOG and Logger() or 0
        self.log("Logging Enabled")
        
        # Visible tracks listener
        if self.song().visible_tracks_has_listener(self.refresh_state) != 1:
            self.song().add_visible_tracks_listener(self.refresh_state)
        
######################################################################
# Standard Ableton Methods

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here, as we do it
        connect the extension modules
        """
        return

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        """
        To be called from any components, as soon as their internal state changed in a 
        way, that we do need to remap the mappings that are processed directly by the 
        Live engine.
        Dont assume that the request will immediately result in a call to
        your build_midi_map function. For performance reasons this is only
        called once per GUI frame.
        """
        return
    
    def update_display(self):
        """
        This function is run every 100ms, so we use it to initiate our Song.current_song_time
        listener to allow us to process incoming OSC commands as quickly as possible under
        the current listener scheme.
        """
        ######################################################
        # START OSC LISTENER SETUP
              
        if self.basicAPI == 0:
            # By default we have set basicAPI to 0 so that we can assign it after
            # initialization. We try to get the current song and if we can we'll
            # connect our basicAPI callbacks to the listener allowing us to 
            # respond to incoming OSC every 60ms.
            #
            # Since this method is called every 100ms regardless of the song time
            # changing, we use both methods for processing incoming UDP requests
            # so that from a resting state you can initiate play/clip triggering.
            
            try:
                doc = self.song()
            except:
                return
            try:
                self.basicAPI = LiveOSCCallbacks.LiveOSCCallbacks(self.oscServer)
                # Commented for stability
                #doc.add_current_song_time_listener(self.oscServer.processIncomingUDP)
                self.oscServer.sendOSC('/remix/echo', 'basicAPI setup complete')
            except:
                return
            
            # If our OSC server is listening, try processing incoming requests.
            # Any 'play' initiation will trigger the current_song_time listener
            # and bump updates from 100ms to 60ms.
            
        if self.oscServer:
            try:
                self.oscServer.processIncomingUDP()
            except:
                pass
            
        # END OSC LISTENER SETUP
        ######################################################

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices 
        that this script is assigned to.
        """
        pass

    def receive_midi(self, midi_bytes):
        return

    def can_lock_to_devices(self):
        return False

    def suggest_input_port(self):
        return ''

    def suggest_output_port(self):
        return ''

    def __handle_display_switch_ids(self, switch_id, value):
	pass
    
    
######################################################################
# Useful Methods

    def getOSCServer(self):
        return self.oscServer
    
    def application(self):
        """returns a reference to the application that we are running in"""
        return Live.Application.get_application()

    def song(self):
        """returns a reference to the Live Song that we do interact with"""
        return self._LiveOSC__c_instance.song()

    def handle(self):
        """returns a handle to the c_interface that is needed when forwarding MIDI events via the MIDI map"""
        return self._LiveOSC__c_instance.handle()
    def log(self, msg):
        if self._LOG == 1:
            self.logger.log(msg) 
            
    def getslots(self):
        tracks = self.song().visible_tracks

        clipSlots = []
        for track in tracks:
            clipSlots.append(track.clip_slots)
        return clipSlots

    def trBlock(self, trackOffset, blocksize):
        block = []
        tracks = self.song().visible_tracks
        
        for track in range(0, blocksize):
            block.extend([str(tracks[trackOffset+track].name)])                            
        self.oscServer.sendOSC("/live/name/trackblock", block)        

######################################################################
# Used Ableton Methods

    def disconnect(self):
        self.rem_clip_listeners()
        self.rem_mixer_listeners()
        self.rem_scene_listeners()
        self.rem_tempo_listener()
        self.rem_overdub_listener()
        self.rem_tracks_listener()
        
        self.song().remove_visible_tracks_listener(self.refresh_state)
        
        self.oscServer.sendOSC('/remix/oscserver/shutdown', 1)
        self.oscServer.shutdown()
            
    def build_midi_map(self, midi_map_handle):
        self.refresh_state()            
            
    def refresh_state(self):
        self.add_clip_listeners()
        self.add_mixer_listeners()
        self.add_scene_listeners()
        self.add_tempo_listener()
        self.add_overdub_listener()
        self.add_tracks_listener()

        trackNumber = 0
        clipNumber = 0
        for track in self.song().visible_tracks:
            self.oscServer.sendOSC("/live/name/track", (trackNumber, str(track.name)))
            
            for clipSlot in track.clip_slots:
                if clipSlot.clip != None:
                    self.oscServer.sendOSC("/live/name/clip", (trackNumber, clipNumber, str(clipSlot.clip.name), str(clipSlot.clip.color_index)))
                clipNumber = clipNumber + 1
            clipNumber = 0
            trackNumber = trackNumber + 1

        self.trBlock(0, len(self.song().visible_tracks))

######################################################################
# Add / Remove Listeners   
    def add_scene_listeners(self):
        self.rem_scene_listeners()
    
        if self.song().view.selected_scene_has_listener(self.scene_change) != 1:
            self.song().view.add_selected_scene_listener(self.scene_change)

    def rem_scene_listeners(self):
        if self.song().view.selected_scene_has_listener(self.scene_change) == 1:
            self.song().view.remove_selected_scene_listener(self.scene_change)

    def scene_change(self):
        selected_scene = self.song().view.selected_scene
        scenes = self.song().scenes
        index = 0
        selected_index = 0
        for scene in scenes:
            index = index + 1        
            if scene == selected_scene:
                selected_index = index
                
        if selected_index != self.scene:
            self.scene = selected_index
            self.oscServer.sendOSC("/live/scene", (selected_index))
            if LiveUtils.getClip(0, (selected_index - 1)) == None:
                str1 = 'Empty'
            else:
                str1 = (str(LiveUtils.getClip(0, (selected_index - 1)).name))
                
            if LiveUtils.getClip(1, (selected_index - 1)) == None:
                str2 = 'Empty'
            else:
                str2 = (str(LiveUtils.getClip(1, (selected_index - 1)).name))

            if LiveUtils.getClip(2, (selected_index - 1)) == None:
                str3 = 'Empty'
            else:
                str3 = (str(LiveUtils.getClip(2, (selected_index - 1)).name))
                
            if LiveUtils.getClip(3, (selected_index - 1)) == None:
                str4 = 'Empty'
            else:
                str4 = (str(LiveUtils.getClip(3, (selected_index - 1)).name))

            self.oscServer.sendOSC("/live/name/clipfromscene/1", str1)
            self.oscServer.sendOSC("/live/name/clipfromscene/2", str2)
            self.oscServer.sendOSC("/live/name/clipfromscene/3", str3)
            self.oscServer.sendOSC("/live/name/clipfromscene/4", str4)
	
    def add_tempo_listener(self):
        self.rem_tempo_listener()
    
        print "add tempo listener"
        if self.song().tempo_has_listener(self.tempo_change) != 1:
            self.song().add_tempo_listener(self.tempo_change)
        
    def rem_tempo_listener(self):
        if self.song().tempo_has_listener(self.tempo_change) == 1:
            self.song().remove_tempo_listener(self.tempo_change)
    
    def tempo_change(self):
        tempo = LiveUtils.getTempo()
        self.oscServer.sendOSC("/live/tempo", (tempo))
	
    def add_overdub_listener(self):
        self.rem_overdub_listener()
    
        if self.song().overdub_has_listener(self.overdub_change) != 1:
            self.song().add_overdub_listener(self.overdub_change)
	    
    def rem_overdub_listener(self):
        if self.song().overdub_has_listener(self.overdub_change) == 1:
            self.song().remove_overdub_listener(self.overdub_change)
	    
    def overdub_change(self):
        overdub = LiveUtils.getSong().overdub
        self.oscServer.sendOSC("/live/overdub", (int(overdub) + 1))
	
    def add_tracks_listener(self):
        self.rem_tracks_listener()
    
        if self.song().tracks_has_listener(self.tracks_change) != 1:
            self.song().add_tracks_listener(self.tracks_change)
    
    def rem_tracks_listener(self):
        if self.song().tracks_has_listener(self.tempo_change) == 1:
            self.song().remove_tracks_listener(self.tracks_change)
    
    def tracks_change(self):
        self.oscServer.sendOSC("/live/refresh", (1))

    def rem_clip_listeners(self):
        self.log("** Remove Listeners **")
    
        for slot in self.slisten:
            if slot != None:
                if slot.has_clip_has_listener(self.slisten[slot]) == 1:
                    slot.remove_has_clip_listener(self.slisten[slot])
    
        self.slisten = {}
        
        for clip in self.clisten:
            if clip != None:
                if clip.playing_status_has_listener(self.clisten[clip]) == 1:
                    clip.remove_playing_status_listener(self.clisten[clip])
                
        self.clisten = {}
        
    def add_clip_listeners(self):
        self.rem_clip_listeners()
    
        tracks = self.getslots()
        for track in range(len(tracks)):
            for clip in range(len(tracks[track])):
                c = tracks[track][clip]
                if c.clip != None:
                    self.add_cliplistener(c.clip, track, clip)
                    self.log("ClipLauncher: added clip listener tr: " + str(track) + " clip: " + str(clip));
                
                self.add_slotlistener(c, track, clip)
        
    def add_cliplistener(self, clip, tid, cid):
        cb = lambda :self.clip_changestate(clip, tid, cid)
        
        if self.clisten.has_key(clip) != 1:
            clip.add_playing_status_listener(cb)
            self.clisten[clip] = cb
        
    def add_slotlistener(self, slot, tid, cid):
        cb = lambda :self.slot_changestate(slot, tid, cid)
        
        if self.slisten.has_key(slot) != 1:
            slot.add_has_clip_listener(cb)
            self.slisten[slot] = cb   
            
    
    def rem_mixer_listeners(self):
        # Master Track
        for type in ("volume", "panning", "crossfader"):
            for tr in self.masterlisten[type]:
                if tr != None:
                    cb = self.masterlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")

        # Normal Tracks
        for type in ("arm", "solo", "mute"):
            for tr in self.mlisten[type]:
                if tr != None:
                    cb = self.mlisten[type][tr]
                    
                    if type == "arm":
                        if tr.can_be_armed == 1:
                            if tr.arm_has_listener(cb) == 1:
                                tr.remove_arm_listener(cb)
                                
                    else:
                        test = eval("tr." + type+ "_has_listener(cb)")
                
                        if test == 1:
                            eval("tr.remove_" + type + "_listener(cb)")
                
        for type in ("volume", "panning"):
            for tr in self.mlisten[type]:
                if tr != None:
                    cb = self.mlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")
         
        for tr in self.mlisten["sends"]:
            if tr != None:
                for send in self.mlisten["sends"][tr]:
                    if send != None:
                        cb = self.mlisten["sends"][tr][send]

                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)
                        
                        
        for tr in self.mlisten["name"]:
            if tr != None:
                cb = self.mlisten["name"][tr]

                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)
                    
        # Return Tracks                
        for type in ("solo", "mute"):
            for tr in self.rlisten[type]:
                if tr != None:
                    cb = self.rlisten[type][tr]
                
                    test = eval("tr." + type+ "_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.remove_" + type + "_listener(cb)")
                
        for type in ("volume", "panning"):
            for tr in self.rlisten[type]:
                if tr != None:
                    cb = self.rlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")
         
        for tr in self.rlisten["sends"]:
            if tr != None:
                for send in self.rlisten["sends"][tr]:
                    if send != None:
                        cb = self.rlisten["sends"][tr][send]
                
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.rlisten["name"]:
            if tr != None:
                cb = self.rlisten["name"][tr]

                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)
                    
        self.mlisten = { "solo": {}, "mute": {}, "arm": {}, "panning": {}, "volume": {}, "sends": {}, "name": {} }
        self.rlisten = { "solo": {}, "mute": {}, "panning": {}, "volume": {}, "sends": {}, "name": {} }
        self.masterlisten = { "panning": {}, "volume": {}, "crossfader": {} }
    
    
    def add_mixer_listeners(self):
        self.rem_mixer_listeners()
        
        # Master Track
        tr = self.song().master_track
        for type in ("volume", "panning", "crossfader"):
            self.add_master_listener(0, type, tr)
        
        # Normal Tracks
        tracks = self.song().visible_tracks
        for track in range(len(tracks)):
            tr = tracks[track]

            self.add_trname_listener(track, tr, 0)
            
            for type in ("arm", "solo", "mute"):
                if type == "arm":
                    if tr.can_be_armed == 1:
                        self.add_mixert_listener(track, type, tr)
                else:
                    self.add_mixert_listener(track, type, tr)
                
            for type in ("volume", "panning"):
                self.add_mixerv_listener(track, type, tr)
                
            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])
        
        # Return Tracks
        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]

            self.add_trname_listener(track, tr, 1)
            
            for type in ("solo", "mute"):
                self.add_retmixert_listener(track, type, tr)
                
            for type in ("volume", "panning"):
                self.add_retmixerv_listener(track, type, tr)
            
            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])
        
    
    # Add track listeners
    def add_send_listener(self, tid, track, sid, send):
        if self.mlisten["sends"].has_key(track) != 1:
            self.mlisten["sends"][track] = {}
                    
        if self.mlisten["sends"][track].has_key(send) != 1:
            cb = lambda :self.send_changestate(tid, track, sid, send)
            
            self.mlisten["sends"][track][send] = cb
            send.add_value_listener(cb)
    
    def add_mixert_listener(self, tid, type, track):
        if self.mlisten[type].has_key(track) != 1:
            cb = lambda :self.mixert_changestate(type, tid, track)
            
            self.mlisten[type][track] = cb
            eval("track.add_" + type + "_listener(cb)")
            
    def add_mixerv_listener(self, tid, type, track):
        if self.mlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track)
            
            self.mlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")

    # Add master listeners
    def add_master_listener(self, tid, type, track):
        if self.masterlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track, 2)
            
            self.masterlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")
            
            
    # Add return listeners
    def add_retsend_listener(self, tid, track, sid, send):
        if self.rlisten["sends"].has_key(track) != 1:
            self.rlisten["sends"][track] = {}
                    
        if self.rlisten["sends"][track].has_key(send) != 1:
            cb = lambda :self.send_changestate(tid, track, sid, send, 1)
            
            self.rlisten["sends"][track][send] = cb
            send.add_value_listener(cb)
    
    def add_retmixert_listener(self, tid, type, track):
        if self.rlisten[type].has_key(track) != 1:
            cb = lambda :self.mixert_changestate(type, tid, track, 1)
            
            self.rlisten[type][track] = cb
            eval("track.add_" + type + "_listener(cb)")
            
    def add_retmixerv_listener(self, tid, type, track):
        if self.rlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track, 1)
            
            self.rlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")      


    # Track name listener
    def add_trname_listener(self, tid, track, ret = 0):
        cb = lambda :self.trname_changestate(tid, track, ret)

        if ret == 1:
            if self.rlisten["name"].has_key(track) != 1:
                self.rlisten["name"][track] = cb
        
        else:
            if self.mlisten["name"].has_key(track) != 1:
                self.mlisten["name"][track] = cb
        
        track.add_name_listener(cb)
            

######################################################################
# Listener Callbacks
        
    # Clip Callbacks
    def slot_changestate(self, slot, tid, cid):
        tmptrack = LiveUtils.getTrack(tid)
        armed = tmptrack.arm and 1 or 0
        
        # Added new clip
        if slot.clip != None:
            self.add_cliplistener(slot.clip, tid, cid)
            
            playing = 1
            if slot.clip.is_playing == 1:
                playing = 2
            
            if slot.clip.is_triggered == 1:
                playing = 3
            
            length =  slot.clip.loop_end - slot.clip.loop_start
            
            self.oscServer.sendOSC('/live/track/info', (tid, armed, cid, playing, length))
            self.oscServer.sendOSC('/live/name/clip', (tid, cid, str(slot.clip.name), str(slot.clip.color_index)))
        else:
            if self.clisten.has_key(slot.clip) == 1:
                slot.clip.remove_playing_status_listener(self.clisten[slot.clip])
            
            self.oscServer.sendOSC('/live/track/info', (tid, armed, cid, 0, 0.0))
            self.oscServer.sendOSC('/live/clip/info', (tid, cid, 0))
                
        #self.log("Slot changed" + str(self.clips[tid][cid]))
    
    def clip_changestate(self, clip, x, y):
        self.log("Listener: x: " + str(x) + " y: " + str(y));

        playing = 1
        
        if clip.is_playing == 1:
            playing = 2
            
        if clip.is_triggered == 1:
            playing = 3
            
        self.oscServer.sendOSC('/live/clip/info', (x, y, playing))
        
        #self.log("Clip changed x:" + str(x) + " y:" + str(y) + " status:" + str(playing)) 
        
        
    # Mixer Callbacks
    def mixerv_changestate(self, type, tid, track, r = 0):
        val = eval("track.mixer_device." + type + ".value")
        types = { "panning": "pan", "volume": "volume", "crossfader": "crossfader" }
        
        if r == 2:
            self.oscServer.sendOSC('/live/master/' + types[type], (float(val)))
        elif r == 1:
            self.oscServer.sendOSC('/live/return/' + types[type], (tid, float(val)))
        else:
            self.oscServer.sendOSC('/live/' + types[type], (tid, float(val)))        
        
    def mixert_changestate(self, type, tid, track, r = 0):
        val = eval("track." + type)
        
        if r == 1:
            self.oscServer.sendOSC('/live/return/' + type, (tid, int(val)))
        else:
            self.oscServer.sendOSC('/live/' + type, (tid, int(val)))        
    
    def send_changestate(self, tid, track, sid, send, r = 0):
        val = send.value
        
        if r == 1:
            self.oscServer.sendOSC('/live/return/send', (tid, sid, float(val)))   
        else:
            self.oscServer.sendOSC('/live/send', (tid, sid, float(val)))   


    # Track name changestate
    def trname_changestate(self, tid, track, r = 0):
        if r == 1:
            self.oscServer.sendOSC('/live/name/return', (tid, str(track.name)))
        else:
            self.oscServer.sendOSC('/live/name/track', (tid, str(track.name)))
            self.trBlock(0, len(LiveUtils.getTracks()))
            