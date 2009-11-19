"""
# Copyright (C) 2007 Rob King (rob@re-mu.org)
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
# Rob King <rob@e-mu.org> or visit http://www.e-mu.org

This file contains all the current Live OSC callbacks. 

"""
import Live
import RemixNet
import OSC
import LiveUtils

class LiveOSCCallbacks:
    def __init__(self, oscServer):
        if oscServer:
            self.oscServer = oscServer
            self.callbackManager = oscServer.callbackManager
            self.oscClient = oscServer.oscClient
        else:
            return

        self.callbackManager.add(self.tempoCB, "/live/tempo")
        self.callbackManager.add(self.timeCB, "/live/time")
        self.callbackManager.add(self.nextCueCB, "/live/next/cue")
        self.callbackManager.add(self.prevCueCB, "/live/prev/cue")
        self.callbackManager.add(self.playCB, "/live/play")
        self.callbackManager.add(self.playContinueCB, "/live/play/continue")
        self.callbackManager.add(self.playSelectionCB, "/live/play/selection")
        self.callbackManager.add(self.playClipCB, "/live/play/clip")
        self.callbackManager.add(self.playSceneCB, "/live/play/scene")
        self.callbackManager.add(self.stopCB, "/live/stop")
        self.callbackManager.add(self.stopClipCB, "/live/stop/clip")
        self.callbackManager.add(self.stopTrackCB, "/live/stop/track")
        self.callbackManager.add(self.scenesCB, "/live/scenes")
        self.callbackManager.add(self.tracksCB, "/live/tracks")
        self.callbackManager.add(self.nameSceneCB, "/live/name/scene")
        self.callbackManager.add(self.sceneCB, "/live/scene")
        self.callbackManager.add(self.nameSceneBlockCB, "/live/name/sceneblock")
        self.callbackManager.add(self.nameTrackCB, "/live/name/track")
        self.callbackManager.add(self.nameTrackBlockCB, "/live/name/trackblock")
        self.callbackManager.add(self.nameClipCB, "/live/name/clip")
        self.callbackManager.add(self.nameClipFromSceneCB, "/live/name/clipfromscene")
        self.callbackManager.add(self.nameClipBlockCB, "/live/name/clipblock")    
        self.callbackManager.add(self.armTrackCB, "/live/arm")
        self.callbackManager.add(self.muteTrackCB, "/live/mute")
        self.callbackManager.add(self.soloTrackCB, "/live/solo")
        self.callbackManager.add(self.volumeCB, "/live/volume")
        self.callbackManager.add(self.panCB, "/live/pan")
        self.callbackManager.add(self.sendCB, "/live/send")
        self.callbackManager.add(self.pitchCB, "/live/pitch")
        self.callbackManager.add(self.trackJump, "/live/track/jump")
        self.callbackManager.add(self.trackInfoCB, "/live/track/info")
        self.callbackManager.add(self.undoCB, "/live/undo")
        self.callbackManager.add(self.redoCB, "/live/redo")
        self.callbackManager.add(self.playClipSlotCB, "/live/play/clipslot")
        self.callbackManager.add(self.playSelectedClipCB, "/live/play/sceneclip")
        self.callbackManager.add(self.viewTrackCB, "/live/track/view")
        self.callbackManager.add(self.viewTrackCB, "/live/return/view")
        self.callbackManager.add(self.mviewTrackCB, "/live/master/view")
        
        self.callbackManager.add(self.viewDeviceCB, "/live/track/device/view")
        self.callbackManager.add(self.viewDeviceCB, "/live/return/device/view")
        self.callbackManager.add(self.mviewDeviceCB, "/live/master/device/view")        
        
        self.callbackManager.add(self.viewClipCB, "/live/clip/view")
        
        self.callbackManager.add(self.detailViewCB, "/live/detail/view")
        
        self.callbackManager.add(self.overdubCB, "/live/overdub")
        self.callbackManager.add(self.stateCB, "/live/state")
        self.callbackManager.add(self.clipInfoCB, "/live/clip/info")
        
        self.callbackManager.add(self.muteTrackCB, "/live/return/mute")
        self.callbackManager.add(self.soloTrackCB, "/live/return/solo")
        self.callbackManager.add(self.volumeCB, "/live/return/volume")
        self.callbackManager.add(self.panCB, "/live/return/pan")
        self.callbackManager.add(self.sendCB, "/live/return/send")        

        self.callbackManager.add(self.volumeCB, "/live/master/volume")
        self.callbackManager.add(self.panCB, "/live/master/pan")
        
        self.callbackManager.add(self.devicelistCB, "/live/devicelist")
        self.callbackManager.add(self.devicelistCB, "/live/return/devicelist")
        self.callbackManager.add(self.mdevicelistCB, "/live/master/devicelist")

        self.callbackManager.add(self.devicerangeCB, "/live/device/range")
        self.callbackManager.add(self.devicerangeCB, "/live/return/device/range")
        self.callbackManager.add(self.mdevicerangeCB, "/live/master/device/range")
        
        self.callbackManager.add(self.deviceCB, "/live/device")
        self.callbackManager.add(self.deviceCB, "/live/return/device")
        self.callbackManager.add(self.mdeviceCB, "/live/master/device")
        
        self.callbackManager.add(self.loopStateCB, "/live/clip/loopstate")
        self.callbackManager.add(self.loopStartCB, "/live/clip/loopstart")
        self.callbackManager.add(self.loopEndCB, "/live/clip/loopend")
        
        self.callbackManager.add(self.loopStateCB, "/live/clip/loopstate_id")
        self.callbackManager.add(self.loopStartCB, "/live/clip/loopstart_id")
        self.callbackManager.add(self.loopEndCB, "/live/clip/loopend_id")
        
        self.callbackManager.add(self.crossfaderCB, "/live/master/crossfader")

        self.callbackManager.add(self.quantizationCB, "/live/quantization")


    def tempoCB(self, msg):
        """Called when a /live/tempo message is received.

        Messages:
        /live/tempo                 Request current tempo, replies with /live/tempo (float tempo)
        /live/tempo (float tempo)   Set the tempo, replies with /live/tempo (float tempo)
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscServer.sendOSC("/live/tempo", LiveUtils.getTempo())
        
        elif len(msg) == 3:
            tempo = msg[2]
            LiveUtils.setTempo(tempo)
        
    def timeCB(self, msg):
        """Called when a /live/time message is received.

        Messages:
        /live/time                 Request current song time, replies with /live/time (float time)
        /live/time (float time)    Set the time , replies with /live/time (float time)
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscServer.sendOSC("/live/time", float(LiveUtils.currentTime()))

        elif len(msg) == 3:
            time = msg[2]
            LiveUtils.currentTime(time)

    def nextCueCB(self, msg):
        """Called when a /live/next/cue message is received.

        Messages:
        /live/next/cue              Jumps to the next cue point
        """
        LiveUtils.jumpToNextCue()
        
    def prevCueCB(self, msg):
        """Called when a /live/prev/cue message is received.

        Messages:
        /live/prev/cue              Jumps to the previous cue point
        """
        LiveUtils.jumpToPrevCue()
        
    def playCB(self, msg):
        """Called when a /live/play message is received.

        Messages:
        /live/play              Starts the song playing
        """
        LiveUtils.play()
        
    def playContinueCB(self, msg):
        """Called when a /live/play/continue message is received.

        Messages:
        /live/play/continue     Continues playing the song from the current point
        """
        LiveUtils.continuePlaying()
        
    def playSelectionCB(self, msg):
        """Called when a /live/play/selection message is received.

        Messages:
        /live/play/selection    Plays the current selection
        """
        LiveUtils.playSelection()
        
    def playClipCB(self, msg):
        """Called when a /live/play/clip message is received.

        Messages:
        /live/play/clip     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            track = msg[2]
            clip = msg[3]
            LiveUtils.launchClip(track, clip)
            
    def playSceneCB(self, msg):
        """Called when a /live/play/scene message is received.

        Messages:
        /live/play/scene    (int scene)     Launches scene number scene
        """
        if len(msg) == 3:
            scene = msg[2]
            LiveUtils.launchScene(scene)
    
    def stopCB(self, msg):
        """Called when a /live/stop message is received.

        Messages:
        /live/stop              Stops playing the song
        """
        LiveUtils.stop()
        
    def stopClipCB(self, msg):
        """Called when a /live/stop/clip message is received.

        Messages:
        /live/stop/clip     (int track, int clip)   Stops clip number clip in track number track
        """
        if len(msg) == 4:
            track = msg[2]
            clip = msg[3]
            LiveUtils.stopClip(track, clip)

    def stopTrackCB(self, msg):
        """Called when a /live/stop/track message is received.

        Messages:
        /live/stop/track     (int track, int clip)   Stops track number track
        """
        if len(msg) == 3:
            track = msg[2]
            LiveUtils.stopTrack(track)

    def scenesCB(self, msg):
        """Called when a /live/scenes message is received.

        Messages:
        /live/scenes        no argument or 'query'  Returns the total number of scenes

        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            sceneTotal = len(LiveUtils.getScenes())
            self.oscServer.sendOSC("/live/scenes", (sceneTotal))
            return

    def sceneCB(self, msg):
        """Called when a /live/scene message is received.
        
        Messages:
        /live/scene         no argument or 'query'  Returns the currently playing scene number
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            selected_scene = LiveUtils.getSong().view.selected_scene
            scenes = LiveUtils.getScenes()
            index = 0
            selected_index = 0
            for scene in scenes:
                index = index + 1        
                if scene == selected_scene:
                    selected_index = index
                    
            self.oscServer.sendOSC("/live/scene", (selected_index))

    def tracksCB(self, msg):
        """Called when a /live/tracks message is received.

        Messages:
        /live/tracks       no argument or 'query'  Returns the total number of scenes

        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackTotal = len(LiveUtils.getTracks())
            self.oscServer.sendOSC("/live/tracks", (trackTotal))
            return


    def nameSceneCB(self, msg):
        """Called when a /live/name/scene message is received.

        Messages:
        /live/name/scene                            Returns a a series of all the scene names in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene)             Returns a single scene's name in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene, string name)Sets scene number scene's name to name

        """        
        #Requesting all scene names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            sceneNumber = 0
            for scene in LiveUtils.getScenes():
                self.oscServer.sendOSC("/live/name/scene", (sceneNumber, str(scene.name)))
                sceneNumber = sceneNumber + 1
            return
        #Requesting a single scene name
        if len(msg) == 3:
            sceneNumber = msg[2]
            self.oscServer.sendOSC("/live/name/scene", (sceneNumber, str(LiveUtils.getScene(sceneNumber).name)))
            return
        #renaming a scene
        if len(msg) == 4:
            sceneNumber = msg[2]
            name = msg[3]
            LiveUtils.getScene(sceneNumber).name = name

    def nameSceneBlockCB(self, msg):
        """Called when a /live/name/sceneblock message is received.

        /live/name/clipblock    (int offset, int blocksize) Returns a list of blocksize scene names starting at offset
        """
        if len(msg) == 4:
            block = []
            sceneOffset = msg[2]
            blocksize = msg[3]
            for scene in range(0, blocksize):
                block.extend([str(LiveUtils.getScene(sceneOffset+scene).name)])                            
            self.oscServer.sendOSC("/live/name/sceneblock", block)
            
            
    def nameTrackCB(self, msg):
        """Called when a /live/name/track message is received.

        Messages:
        /live/name/track                            Returns a a series of all the track names in the form /live/name/track (int track, string name)
        /live/name/track    (int track)             Returns a single track's name in the form /live/name/track (int track, string name)
        /live/name/track    (int track, string name)Sets track number track's name to name

        """        
        #Requesting all track names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackNumber = 0
            for track in LiveUtils.getTracks():
                self.oscServer.sendOSC("/live/name/track", (trackNumber, str(track.name)))
                trackNumber = trackNumber + 1
            return
        #Requesting a single track name
        if len(msg) == 3:
            trackNumber = msg[2]
            self.oscServer.sendOSC("/live/name/track", (trackNumber, str(LiveUtils.getTrack(trackNumber).name)))
            return
        #renaming a track
        if len(msg) == 4:
            trackNumber = msg[2]
            name = msg[3]
            LiveUtils.getTrack(trackNumber).name = name

    def nameTrackBlockCB(self, msg):
        """Called when a /live/name/trackblock message is received.

        /live/name/trackblock    (int offset, int blocksize) Returns a list of blocksize track names starting at offset
        """
        if len(msg) == 4:
            block = []
            trackOffset = msg[2]
            blocksize = msg[3]
            for track in range(0, blocksize):
                block.extend([str(LiveUtils.getTrack(trackOffset+track).name)])                            
            self.oscServer.sendOSC("/live/name/trackblock", block)


    def nameClipBlockCB(self, msg):
        """Called when a /live/name/clipblock message is received.

        /live/name/clipblock    (int track, int clip, blocksize x/tracks, blocksize y/clipslots) Returns a list of clip names for a block of clips (int blockX, int blockY, clipname)

        """
        #Requesting a block of clip names X1 Y1 X2 Y2 where X1,Y1 is the first clip (track, clip) of the block, X2 the number of tracks to cover and Y2 the number of scenes
        
        if len(msg) == 6:
            block = []
            trackOffset = msg[2]
            clipOffset = msg[3]
            blocksizeX = msg[4]
            blocksizeY = msg[5]
            for clip in range(0, blocksizeY):
                for track in range(0, blocksizeX):
                        trackNumber = trackOffset+track
                        clipNumber = clipOffset+clip
                        if LiveUtils.getClip(trackNumber, clipNumber) != None:
                            block.extend([str(LiveUtils.getClip(trackNumber, clipNumber).name)])
                        else:
                            block.extend([""])
                            
            self.oscServer.sendOSC("/live/name/clipblock", block)



    def nameClipCB(self, msg):
        """Called when a /live/name/clip message is received.

        Messages:
        /live/name/clip                                      Returns a a series of all the clip names in the form /live/name/clip (int track, int clip, string name)
        /live/name/clip    (int track, int clip)             Returns a single clip's name in the form /live/name/clip (int clip, string name)
        /live/name/clip    (int track, int clip, string name)Sets clip number clip in track number track's name to name

        """
        
        #Requesting all clip names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackNumber = 0
            clipNumber = 0
            for track in LiveUtils.getTracks():
                for clipSlot in track.clip_slots:
                    if clipSlot.clip != None:
                        self.oscServer.sendOSC("/live/name/clip", (trackNumber, clipNumber, str(clipSlot.clip.name), str(clipSlot.clip.color_index)))
                    clipNumber = clipNumber + 1
                clipNumber = 0
                trackNumber = trackNumber + 1
            return
        #Requesting a single clip name
        if len(msg) == 4:
            trackNumber = msg[2]
            clipNumber = msg[3]
            self.oscServer.sendOSC("/live/name/clip", (trackNumber, clipNumber, str(LiveUtils.getClip(trackNumber, clipNumber).name), str(LiveUtils.getClip(trackNumber, clipNumber).color_index)))
            return
        #renaming a clip
        if len(msg) == 5:
            trackNumber = msg[2]
            clipNumber = msg[3]
            name = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).name = name
            
    def nameClipFromSceneCB(self, msg):
        """Called when a /live/name/clip message is received.

        Messages:
        /live/name/clip                                      Returns a a series of all the clip names in the form /live/name/clip (int track, int clip, string name)
        /live/name/clip    (int track, int clip)             Returns a single clip's name in the form /live/name/clip (int clip, string name)
        /live/name/clip    (int track, int clip, string name)Sets clip number clip in track number track's name to name

        """
        if len(msg) == 3:
            selected_scene = LiveUtils.getSong().view.selected_scene
            scenes = LiveUtils.getScenes()
            index = 0
            selected_index = 0
            for scene in scenes:
                index = index + 1        
                if scene == selected_scene:
                    selected_index = index
            trackNumber = msg[2]
            clipNumber = selected_index
            self.oscServer.sendOSC("/live/name/clipfromscene/" + str(selected_index), (str(LiveUtils.getClip(trackNumber, clipNumber).name)))
            return
    
    def armTrackCB(self, msg):
        """Called when a /live/arm message is received.

        Messages:
        /live/arm     (int track)   (int armed/disarmed)     Arms track number track
        """
        track = msg[2]
        
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.armTrack(track)
            else:
                LiveUtils.disarmTrack(track)
        # Return arm status        
        elif len(msg) == 3:
            status = LiveUtils.getTrack(track).arm
            self.oscServer.sendOSC("/live/arm", (track, int(status)))     
            
    def muteTrackCB(self, msg):
        """Called when a /live/mute message is received.

        Messages:
        /live/mute     (int track)   Mutes track number track
        """
        ty = msg[0] == '/live/return/mute' and 1 or 0
        track = msg[2]
            
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.muteTrack(track, ty)
            else:
                LiveUtils.unmuteTrack(track, ty)
                
        elif len(msg) == 3:
            if ty == 1:
                status = LiveUtils.getSong().return_tracks[track].mute
                self.oscServer.sendOSC("/live/return/mute", (track, int(status)))
                
            else:
                status = LiveUtils.getTrack(track).mute
                self.oscServer.sendOSC("/live/mute", (track, int(status)))
            
    def soloTrackCB(self, msg):
        """Called when a /live/solo message is received.

        Messages:
        /live/solo     (int track)   Solos track number track
        """
        ty = msg[0] == '/live/return/solo' and 1 or 0
        track = msg[2]
        
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.soloTrack(track, ty)
            else:
                LiveUtils.unsoloTrack(track, ty)
            
        elif len(msg) == 3:
            if ty == 1:
                status = LiveUtils.getSong().return_tracks[track].solo
                self.oscServer.sendOSC("/live/return/solo", (track, int(status)))
                
            else:
                status = LiveUtils.getTrack(track).solo
                self.oscServer.sendOSC("/live/solo", (track, int(status)))
            
    def volumeCB(self, msg):
        """Called when a /live/volume message is received.

        Messages:
        /live/volume     (int track)                            Returns the current volume of track number track as: /live/volume (int track, float volume(0.0 to 1.0))
        /live/volume     (int track, float volume(0.0 to 1.0))  Sets track number track's volume to volume
        """
        if msg[0] == '/live/return/volume':
            ty = 1
        elif msg[0] == '/live/master/volume':
            ty = 2
        else:
            ty = 0
        
        if len(msg) == 2 and ty == 2:
            self.oscServer.sendOSC("/live/master/volume", LiveUtils.getSong().master_track.mixer_device.volume.value)
        
        elif len(msg) == 3 and ty == 2:
            volume = msg[2]
            LiveUtils.getSong().master_track.mixer_device.volume.value = volume
        
        elif len(msg) == 4:
            track = msg[2]
            volume = msg[3]
            
            if ty == 0:
                LiveUtils.trackVolume(track, volume)
            elif ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.volume.value = volume

        elif len(msg) == 3:
            track = msg[2]

            if ty == 1:
                self.oscServer.sendOSC("/live/return/volume", (track, LiveUtils.getSong().return_tracks[track].mixer_device.volume.value))
            
            else:
                self.oscServer.sendOSC("/live/volume", (track, LiveUtils.trackVolume(track)))
            
    def panCB(self, msg):
        """Called when a /live/pan message is received.

        Messages:
        /live/pan     (int track)                            Returns the pan of track number track as: /live/pan (int track, float pan(-1.0 to 1.0))
        /live/pan     (int track, float pan(-1.0 to 1.0))    Sets track number track's pan to pan

        """
        if msg[0] == '/live/return/pan':
            ty = 1
        elif msg[0] == '/live/master/pan':
            ty = 2
        else:
            ty = 0
        
        if len(msg) == 2 and ty == 2:
            self.oscServer.sendOSC("/live/master/pan", LiveUtils.getSong().master_track.mixer_device.panning.value)
        
        elif len(msg) == 3 and ty == 2:
            pan = msg[2]
            LiveUtils.getSong().master_track.mixer_device.panning.value = pan
            
        elif len(msg) == 4:
            track = msg[2]
            pan = msg[3]
            
            if ty == 0:
                LiveUtils.trackPan(track, pan)
            elif ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.panning.value = pan
            
        elif len(msg) == 3:
            track = msg[2]
            
            if ty == 1:
                self.oscServer.sendOSC("/live/pan", (track, LiveUtils.getSong().return_tracks[track].mixer_device.panning.value))
            
            else:
                self.oscServer.sendOSC("/live/pan", (track, LiveUtils.trackPan(track)))

            
    def sendCB(self, msg):
        """Called when a /live/send message is received.

        Messages:
        /live/send     (int track, int send)                              Returns the send level of send (send) on track number track as: /live/send (int track, int send, float level(0.0 to 1.0))
        /live/send     (int track, int send, float level(0.0 to 1.0))     Sets the send (send) of track number (track)'s level to (level)

        """
        ty = msg[0] == '/live/return/send' and 1 or 0
        track = msg[2]
        
        if len(msg) == 5:
            send = msg[3]
            level = msg[4]
            if ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.sends[send].value = level
            
            else:
                LiveUtils.trackSend(track, send, level)
        
        elif len(msg) == 4:
            send = msg[3]
            if ty == 1:
                self.oscServer.sendOSC("/live/return/send", (track, send, float(LiveUtils.getSong().return_tracks[track].mixer_device.sends[send].value)))

            else:
                self.oscServer.sendOSC("/live/send", (track, send, float(LiveUtils.trackSend(track, send))))
            
        elif len(msg) == 3:
            if ty == 1:
                sends = LiveUtils.getSong().return_tracks[track].mixer_device.sends
            else:
                sends = LiveUtils.getSong().visible_tracks[track].mixer_device.sends
                
            so = [track]
            for i in range(len(sends)):
                so.append(i)
                so.append(float(sends[i].value))
                
            if ty == 1:
                self.oscServer.sendOSC("/live/return/send", tuple(so))
            else:
                self.oscServer.sendOSC("/live/send", tuple(so))
                
        
            
    def pitchCB(self, msg):
        """Called when a /live/pitch message is received.

        Messages:
        /live/pitch     (int track, int clip)                                               Returns the pan of track number track as: /live/pan (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))
        /live/pitch     (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))  Sets clip number clip in track number track's pitch to coarse / fine

        """
        if len(msg) == 6:
            track = msg[2]
            clip = msg[3]
            coarse = msg[4]
            fine = msg[5]
            LiveUtils.clipPitch(track, clip, coarse, fine)
        if len(msg) ==4:
            track = msg[2]
            clip = msg[3]
            self.oscServer.sendOSC("/live/pitch", LiveUtils.clipPitch(track, clip))

    def trackJump(self, msg):
        """Called when a /live/track/jump message is received.

        Messages:
        /live/track/jump     (int track, float beats)   Jumps in track's currently running session clip by beats
        """
        if len(msg) == 4:
            track = msg[2]
            beats = msg[3]
            track = LiveUtils.getTrack(track)
            track.jump_in_running_session_clip(beats)

    def trackInfoCB(self, msg):
        """Called when a /live/track/info message is received.

        Messages:
        /live/track/info     (int track)   Returns clip slot status' for all clips in a track in the form /live/track/info (tracknumber, armed  (clipnumber, state, length))
                                           [state: 1 = Has Clip, 2 = Playing, 3 = Triggered]
        """
        
        clipslots = LiveUtils.getClipSlots()
        
        new = []
        if len(msg) == 3:
            new.append(clipslots[msg[2]])
            tracknum = msg[2] - 1
        else:
            new = clipslots
            tracknum = -1
        
        for track in new:
            tracknum = tracknum + 1
            clipnum = -1
            tmptrack = LiveUtils.getTrack(tracknum)
            armed = tmptrack.arm and 1 or 0
            li = [tracknum, armed]
            for clipSlot in track:
                clipnum = clipnum + 1
                li.append(clipnum);
                if clipSlot.clip != None:
                    clip = clipSlot.clip
                    if clip.is_playing == 1:
                        li.append(2)
                        li.append(clip.length)
                        
                    elif clip.is_triggered == 1:
                        li.append(3)
                        li.append(clip.length)
                        
                    else:
                        li.append(1)
                        li.append(clip.length)
                else:
                    li.append(0)
                    li.append(0.0)
                    
            tu = tuple(li)
            
            self.oscServer.sendOSC("/live/track/info", tu)


    def undoCB(self, msg):
        """Called when a /live/undo message is received.
        
        Messages:
        /live/undo      Requests the song to undo the last action
        """
        LiveUtils.getSong().undo()
        
    def redoCB(self, msg):
        """Called when a /live/redo message is received.
        
        Messages:
        /live/redo      Requests the song to redo the last action
        """
        LiveUtils.getSong().redo()
        
    def playClipSlotCB(self, msg):
        """Called when a /live/play/clipslot message is received.
        
        Messages:
        /live/play/clipslot     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            track_num = msg[2]
            clip_num = msg[3]
            track = LiveUtils.getTrack(track_num)
            clipslot = track.clip_slots[clip_num]
            clipslot.fire()
            
    def playSelectedClipCB(self, msg):
        """Called when a /live/play/clipslot message is received.

        Messages:
        /live/play/clipslot     (int track)   Launches current scenes clipslot in track number track
        """
        if len(msg) == 3:
            selected_scene = LiveUtils.getSong().view.selected_scene
            scenes = LiveUtils.getScenes()
            index = 0
            selected_index = 0
            for scene in scenes:
                index = index + 1        
                if scene == selected_scene:
                    selected_index = index
            track_num = msg[2]
            clip_num = (selected_index - 1)
            track = LiveUtils.getTrack(track_num)
            clipslot = track.clip_slots[clip_num]
            clipslot.fire()
    
    def viewTrackCB(self, msg):
        """Called when a /live/track/view message is received.
        
        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/view' and 1 or 0
        track_num = msg[2]
        
        if len(msg) == 3:
            if ty == 1:
                track = LiveUtils.getSong().return_tracks[track_num]
            else:
                track = LiveUtils.getSong().visible_tracks[track_num]
                
            LiveUtils.getSong().view.selected_track = track
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
                
            #track.view.select_instrument()
            
    def mviewTrackCB(self, msg):
        """Called when a /live/master/view message is received.
        
        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        track = LiveUtils.getSong().master_track

        LiveUtils.getSong().view.selected_track = track
        Live.Application.get_application().view.show_view("Detail/DeviceChain")        
        
        #track.view.select_instrument()
        
    def viewClipCB(self, msg):
        """Called when a /live/clip/view message is received.
        
        Messages:
        /live/clip/view     (int track, int clip)      Selects a track to view
        """
        track = LiveUtils.getSong().visible_tracks[msg[2]]
        
        if len(msg) == 4:
            clip  = msg[3]
        else:
            clip  = 0
        
        LiveUtils.getSong().view.selected_track = track
        LiveUtils.getSong().view.detail_clip = track.clip_slots[clip].clip
        Live.Application.get_application().view.show_view("Detail/Clip")  

    def detailViewCB(self, msg):
        """Called when a /live/detail/view message is received. Used to switch between clip/track detail

        Messages:
        /live/detail/view (int) Selects view where 0=clip detail, 1=track detail
        """
        if len(msg) == 3:
            if msg[2] == 0:
                Live.Application.get_application().view.show_view("Detail/Clip")
            elif msg[2] == 1:
                Live.Application.get_application().view.show_view("Detail/DeviceChain")

    def viewDeviceCB(self, msg):
        """Called when a /live/track/device/view message is received.
        
        Messages:
        /live/track/device/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/device/view' and 1 or 0
        track_num = msg[2]
        
        if len(msg) == 4:
            if ty == 1:
                track = LiveUtils.getSong().return_tracks[track_num]
            else:
                track = LiveUtils.getSong().visible_tracks[track_num]

            LiveUtils.getSong().view.selected_track = track
            LiveUtils.getSong().view.select_device(track.devices[msg[3]])
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
            
    def mviewDeviceCB(self, msg):
        track = LiveUtils.getSong().master_track
        
        if len(msg) == 3:
            LiveUtils.getSong().view.selected_track = track
            LiveUtils.getSong().view.select_device(track.devices[msg[2]])
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
        
    def overdubCB(self, msg):
        """Called when a /live/overdub message is received.
        
        Messages:
        /live/overdub     (int on/off)      Enables/disables overdub
        """        
        if len(msg) == 3:
            overdub = msg[2]
            LiveUtils.getSong().overdub = overdub

    def stateCB(self, msg):
        """Called when a /live/state is received.
        
        Messages:
        /live/state                    Returns the current tempo and overdub status
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            tempo = LiveUtils.getTempo()
            overdub = LiveUtils.getSong().overdub
            self.oscServer.sendOSC("/live/state", (tempo, int(overdub)))
        
    def clipInfoCB(self,msg):
        """Called when a /live/clip/info message is received.
        
        Messages:
        /live/clip/info     (int track, int clip)      Gets the status of a single clip in the form  /live/clip/info (tracknumber, clipnumber, state)
                                                       [state: 1 = Has Clip, 2 = Playing, 3 = Triggered]
        """
        
        if len(msg) == 4:
            trackNumber = msg[2]
            clipNumber = msg[3]    
            
            clip = LiveUtils.getClip(trackNumber, clipNumber)
            
            playing = 0
            
            if clip != None:
                playing = 1
                
                if clip.is_playing == 1:
                    playing = 2
                elif clip.is_triggered == 1:
                    playing = 3

            self.oscServer.sendOSC("/live/clip/info", (trackNumber, clipNumber, playing))
        
        return
        
    def deviceCB(self, msg):
        ty = msg[0] == '/live/return/device' and 1 or 0
        track = msg[2]
    
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            
            if ty == 1:
                params = LiveUtils.getSong().return_tracks[track].devices[device].parameters
            else:
                params = LiveUtils.getSong().visible_tracks[track].devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))
            
            self.oscServer.sendOSC(ty == 1 and "/live/return/device/allparam" or "/live/device/allparam", tuple(po))
    
        elif len(msg) == 5:
            device = msg[3]
            param  = msg[4]
            
            if ty == 1:
                p = LiveUtils.getSong().return_tracks[track].devices[device].parameters[param]
            else: 
                p = LiveUtils.getSong().visible_tracks[track].devices[device].parameters[param]
        
            self.oscServer.sendOSC(ty == 1 and "/live/return/device/param" or "/live/device/param", (track, device, param, p.value, str(p.name)))
    
    
        elif len(msg) == 6:
            device = msg[3]
            param  = msg[4]
            value  = msg[5]
        
            if ty == 1:
                LiveUtils.getSong().return_tracks[track].devices[device].parameters[param].value = value
            else:
                LiveUtils.getSong().visible_tracks[track].devices[device].parameters[param].value = value

    def devicerangeCB(self, msg):
        ty = msg[0] == '/live/return/device/range' and 1 or 0
        track = msg[2]
    
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            
            if ty == 1:
                params = LiveUtils.getSong().return_tracks[track].devices[device].parameters
            else:
                params = LiveUtils.getSong().visible_tracks[track].devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].min)
                po.append(params[i].max)
            
            self.oscServer.sendOSC(ty == 1 and "/live/return/device/range" or "/live/device/range", tuple(po))
    
        elif len(msg) == 5:
            device = msg[3]
            param  = msg[4]
            
            if ty == 1:
                p = LiveUtils.getSong().return_tracks[track].devices[device].parameters[param]
            else: 
                p = LiveUtils.getSong().visible_tracks[track].devices[device].parameters[param]
        
            self.oscServer.sendOSC(ty == 1 and "/live/return/device/range" or "/live/device/range", (track, device, param, p.min, p.max))
                
    def devicelistCB(self, msg):
        ty = msg[0] == '/live/return/devicelist' and 1 or 0

        track = msg[2]
    
        if len(msg) == 3:
            do = [track]
            
            if ty == 1:
                devices = LiveUtils.getSong().return_tracks[track].devices
            else:
                devices = LiveUtils.getSong().visible_tracks[track].devices
        
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))
            
            self.oscServer.sendOSC(ty == 1 and "/live/return/devicelist" or "/live/devicelist", tuple(do))

    def mdeviceCB(self, msg):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            
            params = LiveUtils.getSong().master_track.devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))
            
            self.oscServer.sendOSC("/live/master/device", tuple(po))
    
        elif len(msg) == 4:
            device = msg[2]
            param  = msg[3]
            
            p = LiveUtils.getSong().master_track.devices[device].parameters[param]
        
            self.oscServer.sendOSC("/live/master/device", (device, param, p.value, str(p.name)))
    
        elif len(msg) == 5:
            device = msg[2]
            param  = msg[3]
            value  = msg[4]
        
            LiveUtils.getSong().master_track.devices[device].parameters[param].value = value

    def mdevicerangeCB(self, msg):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            
            params = LiveUtils.getSong().master_track.devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].max)
                po.append(params[i].min)
            
            self.oscServer.sendOSC("/live/master/device/range", tuple(po))
    
        elif len(msg) == 4:
            device = msg[2]
            param  = msg[3]
            
            p = LiveUtils.getSong().master_track.devices[device].parameters[param]
        
            self.oscServer.sendOSC("/live/master/device/range", (device, param, p.min, p.max))
            
    def mdevicelistCB(self, msg):
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            do = []
            devices = LiveUtils.getSong().master_track.devices
        
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))
            
            self.oscServer.sendOSC("/live/master/devicelist", tuple(do))            
            
            
    def crossfaderCB(self, msg):
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscServer.sendOSC("/live/master/crossfader", float(LiveUtils.getSong().master_track.mixer_device.crossfader.value))
        
        elif len(msg) == 3:
            val = msg[2]
            LiveUtils.getSong().master_track.mixer_device.crossfader.value = val


    def loopStateCB(self, msg):
        type = msg[0] == '/live/clip/loopstate_id' and 1 or 0
    
        trackNumber = msg[2]
        clipNumber = msg[3]
    
        if len(msg) == 4:
            if type == 1:
                self.oscServer.sendOSC("/live/clip/loopstate", (trackNumber, clipNumber, int(LiveUtils.getClip(trackNumber, clipNumber).looping)))
            else:
                self.oscServer.sendOSC("/live/clip/loopstate", (int(LiveUtils.getClip(trackNumber, clipNumber).looping)))    
        
        elif len(msg) == 5:
            loopState = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).looping =  loopState

    def loopStartCB(self, msg):
        type = msg[0] == '/live/clip/loopstart_id' and 1 or 0
        
        trackNumber = msg[2]
        clipNumber = msg[3]
    
        if len(msg) == 4:
            if type == 1:
                self.oscServer.sendOSC("/live/clip/loopstart", (trackNumber, clipNumber, float(LiveUtils.getClip(trackNumber, clipNumber).loop_start)))    
            else:
                self.oscServer.sendOSC("/live/clip/loopstart", (float(LiveUtils.getClip(trackNumber, clipNumber).loop_start)))    
    
        elif len(msg) == 5:
            loopStart = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).loop_start = loopStart
            
    def loopEndCB(self, msg):
        type = msg[0] == '/live/clip/loopend_id' and 1 or 0
    
        trackNumber = msg[2]
        clipNumber = msg[3]    
        if len(msg) == 4:
            if type == 1:
                self.oscServer.sendOSC("/live/clip/loopend", (trackNumber, clipNumber, float(LiveUtils.getClip(trackNumber, clipNumber).loop_end)))
            else:
                self.oscServer.sendOSC("/live/clip/loopend", (float(LiveUtils.getClip(trackNumber, clipNumber).loop_end)))    
        
        elif len(msg) == 5:
            loopEnd = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).loop_end =  loopEnd

    def quantizationCB(self, msg):
        quant = msg[2]
        LiveUtils.getSong().clip_trigger_quantization = quant

