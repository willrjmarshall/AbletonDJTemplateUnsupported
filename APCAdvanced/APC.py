# --== Decompile ==--

import Live
from _Framework.ControlSurface import ControlSurface
MANUFACTURER_ID = 71
ABLETON_MODE = 65 #65 = 0x41 = Ableton Live Mode 1; 66 = 0x42 = Ableton Mode 2; 67 = 0x43 = Ableton Mode 3 (APC20 only)
#PRODUCT_MODEL_ID = 115 # 0x73 Product Model ID (APC40)

class APC(ControlSurface):
    __doc__ = " Script for Akai's line of APC Controllers "
    _active_instances = []
    def _combine_active_instances():
        if not len(APC._active_instances) > 0:
            raise AssertionError
        if len(APC._active_instances) > 1:
            support_devices = False
            for instance in APC._active_instances:
                support_devices |= instance._device_component != None
            track_offset = 0
            for instance in APC._active_instances:
                instance._activate_combination_mode(track_offset, support_devices)
                track_offset += instance._session.width()
        return None

    _combine_active_instances = staticmethod(_combine_active_instances)
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.set_suppress_rebuild_requests(True)
        self._suppress_session_highlight = True
        self._suppress_send_midi = True
        self._suggested_input_port = 'Akai ' + self.__class__.__name__
        self._suggested_output_port = 'Akai ' + self.__class__.__name__
        self._shift_button = None
        self._matrix = None
        self._session = None
        self._session_zoom = None
        self._mixer = None
        self._setup_session_control()
        self._setup_mixer_control()
        self._session.set_mixer(self._mixer)
        self._shift_button.name = 'Shift_Button'
        self._setup_custom_components()
        for component in self.components:
            component.set_enabled(False)
        self.set_suppress_rebuild_requests(False)
        self._device_id = 0
        self._common_channel = 0
        self._dongle_challenge = (Live.Application.get_random_int(0, 2000000), Live.Application.get_random_int(2000001, 4000000))
        return None

    def disconnect(self):
        self._shift_button = None
        self._matrix = None
        self._session = None
        self._session_zoom = None
        self._mixer = None
        ControlSurface.disconnect(self)
        return None

    def connect_script_instances(self, instanciated_scripts):
        if len(APC._active_instances) > 0 and self == APC._active_instances[0]:
            APC._combine_active_instances()

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._update_hardware)    
        
    def handle_sysex(self, midi_bytes):
        self._suppress_send_midi = False
        if ((midi_bytes[3] == 6) and (midi_bytes[4] == 2)):
            assert (midi_bytes[5] == MANUFACTURER_ID)
            assert (midi_bytes[6] == self._product_model_id_byte()) # PRODUCT_MODEL_ID
            version_bytes = midi_bytes[9:13]
            self._device_id = midi_bytes[13]
            self._send_introduction_message() # instead of _send_midi, below:
            #self._send_midi((240,
                             #MANUFACTURER_ID,
                             #self._device_id,
                             #PRODUCT_MODEL_ID,
                             #96,
                             #0,
                             #4,
                             #APPLICTION_ID,
                             #self.application().get_major_version(),
                             #self.application().get_minor_version(),
                             #self.application().get_bugfix_version(),
                             #247))
            challenge1 = [0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0]
            challenge2 = [0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0]
            for index in range(8):
                challenge1[index] = ((self._dongle_challenge[0] >> (4 * (7 - index))) & 15)
                challenge2[index] = ((self._dongle_challenge[1] >> (4 * (7 - index))) & 15)

            dongle_message = ((((240,
                                 MANUFACTURER_ID,
                                 self._device_id,
                                 self._product_model_id_byte(),
                                 80,
                                 0,
                                 16) + tuple(challenge1)) + tuple(challenge2)) + (247,))
            self._send_midi(dongle_message)
            message = (((self.__class__.__name__ + ': Got response from controller, version ' + str(((version_bytes[0] << 4) + version_bytes[1]))) + '.') + str(((version_bytes[2] << 4) + version_bytes[3])))
            self.log_message(message)
        elif (midi_bytes[4] == 81):
            assert (midi_bytes[1] == MANUFACTURER_ID)
            assert (midi_bytes[2] == self._device_id)
            assert (midi_bytes[3] == self._product_model_id_byte()) # PRODUCT_MODEL_ID)
            assert (midi_bytes[5] == 0)
            assert (midi_bytes[6] == 16)
            response = [long(0),
                        long(0)]
            for index in range(8):
                response[0] += (long((midi_bytes[(7 + index)] & 15)) << (4 * (7 - index)))
                response[1] += (long((midi_bytes[(15 + index)] & 15)) << (4 * (7 - index)))

            expected_response = Live.Application.encrypt_challenge(self._dongle_challenge[0], self._dongle_challenge[1])
            if ((long(expected_response[0]) == response[0]) and (long(expected_response[1]) == response[1])):
                self._suppress_session_highlight = False
                for component in self.components:
                    component.set_enabled(True)

                self._on_selected_track_changed()

    def _update_hardware(self):
        self._suppress_send_midi = True
        self._suppress_session_highlight = True
        self.set_suppress_rebuild_requests(True)
        for component in self.components:
            component.set_enabled(False)
        self.set_suppress_rebuild_requests(False)
        self._suppress_send_midi = False
        self._send_midi((240, 126, 0, 6, 1, 247)) #(0xF0, 0x7E, 0x00, 0x06, 0x01, 0xF7) = Standard MMC Device Enquiry

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight:
            self._suppress_session_highlight
            ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)
        else:
            self._suppress_session_highlight

    def _send_midi(self, midi_bytes):
        if not self._suppress_send_midi:
            self._suppress_send_midi
            ControlSurface._send_midi(self, midi_bytes)
        else:
            self._suppress_send_midi

    def _send_introduction_message(self, mode_byte=ABLETON_MODE):
        self._send_midi((240, MANUFACTURER_ID, self._device_id, self._product_model_id_byte(), 96, 0, 4, mode_byte, self.application().get_major_version(), self.application().get_minor_version(), self.application().get_bugfix_version(), 247))

    def _activate_combination_mode(self, track_offset, support_devices):
        self._session.link_with_track_offset(track_offset)

    def _setup_session_control(self):
        raise AssertionError, 'Function _setup_session_control must be overridden by subclass'

    def _setup_mixer_control(self):
        raise AssertionError, 'Function _setup_mixer_control must be overridden by subclass'

    def _setup_custom_components(self):
        raise AssertionError, 'Function _setup_custom_components must be overridden by subclass'

    def _product_model_id_byte(self):
        raise AssertionError, 'Function _product_model_id_byte must be overridden by subclass'



