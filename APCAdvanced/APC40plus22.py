# http://remotescripts.blogspot.com

import Live
from APC import APC
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.MixerComponent import MixerComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from EncoderMixerModeSelectorComponent import EncoderMixerModeSelectorComponent
from RingedEncoderElement import RingedEncoderElement
from DetailViewControllerComponent import DetailViewControllerComponent
from ShiftableDeviceComponent import ShiftableDeviceComponent
from ShiftableTransportComponent import ShiftableTransportComponent
from ShiftableTranslatorComponent import ShiftableTranslatorComponent
from PedaledSessionComponent import PedaledSessionComponent
from SpecialMixerComponent import SpecialMixerComponent

# Additional imports from APC20.py:
from ShiftableSelectorComponent import ShiftableSelectorComponent
from SliderModesComponent import SliderModesComponent

# Import added from Launchpad scripts - needed for Note Mode:
from ConfigurableButtonElement import ConfigurableButtonElement 

# New components
from MatrixModesComponent import MatrixModesComponent
from EncoderUserModesComponent import EncoderUserModesComponent
from ShiftableEncoderSelectorComponent import ShiftableEncoderSelectorComponent
from EncoderEQComponent import EncoderEQComponent
from EncoderDeviceComponent import EncoderDeviceComponent

#from ShiftableLooperComponent import ShiftableLooperComponent
from LooperComponent import LooperComponent
from RepeatComponent import RepeatComponent


class APC40plus22(APC):
    __doc__ = " Script for Akai's APC40 Controller with extra features added "
    def __init__(self, c_instance):
        self._c_instance = c_instance
        self._shift_modes = None #added from APC20 script
        self._encoder_modes = None #added
        self._slider_modes = None #added
        APC.__init__(self, c_instance)
        self.show_message("APC40_22 script loaded")
        
        # Disabling the scene launch buttons and assigning them to the first 5 repeats on Master
        self._device_buttons = []
        self.setup_device_buttons()

    def disconnect(self): #this is from the APC20 script
        for button in self._device_buttons:
            button.remove_value_listener(self._device_toggle)
        self._device_buttons = None
        self._shift_modes = None
        self._encoder_modes = None
        self._slider_modes = None
        APC.disconnect(self)        

    def setup_device_buttons(self):
      repeat = RepeatComponent(self)
      repeat.set_shift_button(self._shift_button)

    def _setup_session_control(self):
        is_momentary = True
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 98)        
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 96)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 97)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 94)
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 95)
        right_button.name = 'Bank_Select_Right_Button'
        left_button.name = 'Bank_Select_Left_Button'
        up_button.name = 'Bank_Select_Up_Button'
        down_button.name = 'Bank_Select_Down_Button'
        self._session = PedaledSessionComponent(8, 5)
        self._session.name = 'Session_Control'
        self._session.set_track_bank_buttons(right_button, left_button)
        self._session.set_scene_bank_buttons(down_button, up_button)
        self._matrix = ButtonMatrixElement() #was: matrix = ButtonMatrixElement()
        self._matrix.name = 'Button_Matrix' #was: matrix.name = 'Button_Matrix'
        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, (index + 82)) for index in range(5) ]
        #self._track_stop_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 52) for index in range(8) ]
        self._track_stop_buttons = [ ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 52) for index in range(8) ]
        for index in range(len(scene_launch_buttons)):
            scene_launch_buttons[index].name = 'Scene_'+ str(index) + '_Launch_Button'
        for index in range(len(self._track_stop_buttons)):
            self._track_stop_buttons[index].name = 'Track_' + str(index) + '_Stop_Button'
        stop_all_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 81)
        stop_all_button.name = 'Stop_All_Clips_Button'
        self._session.set_stop_all_clips_button(stop_all_button)
        self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        self._session.set_stop_track_clip_value(2)
        for scene_index in range(5):
            scene = self._session.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            scene.set_launch_button(scene_launch_buttons[scene_index])
            scene.set_triggered_value(2)
            for track_index in range(8):
                #button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track_index, (scene_index + 53)) 
                button = ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, track_index, (scene_index + 53)) #use Launchpad configurable button instead
                button.name = str(track_index) + '_Clip_' + str(scene_index) + '_Button'
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_triggered_to_play_value(2)
                clip_slot.set_triggered_to_record_value(4)
                clip_slot.set_stopped_value(3)
                clip_slot.set_started_value(1)
                clip_slot.set_recording_value(5)
                clip_slot.set_launch_button(button)
            self._matrix.add_row(tuple(button_row)) #matrix.add_row(tuple(button_row))

        # Removing the launch selected clip footpedal option
        #self._session.set_slot_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 67))


        self._session.selected_scene().name = 'Selected_Scene'
        self._session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 64))
        self._session_zoom = SessionZoomingComponent(self._session) #use APC20 Zooming instead      
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_button_matrix(self._matrix) #was: self._session_zoom.set_button_matrix(matrix)
        self._session_zoom.set_zoom_button(self._shift_button) #set in MatrixModesComponent instead
        self._session_zoom.set_nav_buttons(up_button, down_button, left_button, right_button)
        self._session_zoom.set_scene_bank_buttons(tuple(scene_launch_buttons))
        self._session_zoom.set_stopped_value(3)
        self._session_zoom.set_selected_value(5)
        return None

    def _setup_mixer_control(self):
        is_momentary = True
        self._mixer = SpecialMixerComponent(self, 8) #added self for parent
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        master_select_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 80)
        master_select_button.name = 'Master_Select_Button'
        self._mixer.master_strip().set_select_button(master_select_button) #set in ShiftableSelectorComponent instead if used for Note Mode
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        select_buttons = [] #added
        arm_buttons = [] #added
        sliders = [] #added     
        for track in range(8):
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            #volume_control = SliderElement(MIDI_CC_TYPE, track, 7) #set in ShiftableSelectorComponent instead
            #arm_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 48) #see below
            solo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 49)
            solo_button.name = str(track) + '_Solo_Button'
            strip.set_solo_button(solo_button)

            if track < 4:
              mute_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 50)
              mute_button.name = str(track) + '_Mute_Button'
              strip.set_mute_button(mute_button)
              strip.set_invert_mute_feedback(True)

            strip.set_shift_button(self._shift_button)
            select_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 51)) #added
            select_buttons[-1].name = str(track) + '_Select_Button' #added            
            #strip.set_select_button(select_buttons[-1]) #added 
            arm_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 48)) #added
            arm_buttons[-1].name = str(track) + '_Arm_Button' #added
            sliders.append(SliderElement(MIDI_CC_TYPE, track, 7)) #added
            sliders[-1].name = str(track) + '_Volume_Control' #added

        self._crossfader = SliderElement(MIDI_CC_TYPE, 0, 15)
        master_volume_control = SliderElement(MIDI_CC_TYPE, 0, 14)
        self._prehear_control = EncoderElement(MIDI_CC_TYPE, 0, 47, Live.MidiMap.MapMode.relative_two_compliment)
        self._crossfader.name = 'Crossfader' #not used in APC20
        master_volume_control.name = 'Master_Volume_Control'
        self._prehear_control.name = 'Prehear_Volume_Control'
        self._mixer.set_shift_button(self._shift_button) #added for shifting prehear
        self._mixer.set_crossfader_control(self._crossfader) #not used in APC20
        self._mixer.set_prehear_volume_control(self._prehear_control) #functionality overridden in SpecialMixerComponent
        self._mixer.master_strip().set_volume_control(master_volume_control)
        self._slider_modes = SliderModesComponent(self._mixer, tuple(sliders)) #added from APC20 script
        self._slider_modes.name = 'Slider_Modes' #added from APC20 script
        matrix_modes = MatrixModesComponent(self._matrix, self._session, self._session_zoom, tuple(self._track_stop_buttons), self) #added new
        matrix_modes.name = 'Matrix_Modes' #added new
        # Original method args for ShiftableSelectorComponent: (self, select_buttons, master_button, arm_buttons, matrix, session, zooming, mixer, transport, slider_modes, mode_callback)
        #self._shift_modes = ShiftableSelectorComponent(tuple(select_buttons), master_select_button, tuple(arm_buttons), self._matrix, self._session, self._session_zoom, self._mixer, transport, slider_modes, self._send_introduction_message)
        self._shift_modes = ShiftableSelectorComponent(self, tuple(select_buttons), master_select_button, tuple(arm_buttons), self._matrix, self._session, self._session_zoom, self._mixer, self._slider_modes, matrix_modes) #, self._send_introduction_message) #also added self for _parent
        self._shift_modes.name = 'Shift_Modes'
        self._shift_modes.set_mode_toggle(self._shift_button)

    def _setup_custom_components(self):
        self._setup_looper_control()
        self._setup_device_and_transport_control()
        self._setup_global_control()    

    def _setup_looper_control(self):
        is_momentary = True
        #pedal = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 67)
        loop_on = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 4, 50)
        loop_start = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 5, 50)
        halve = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 6, 50)
        double = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 7, 50)
        looper = LooperComponent(self)
        looper.set_shift_button(self._shift_button)
        looper.set_loop_toggle_button(loop_on)
        looper.set_loop_start_button(loop_start)
        looper.set_loop_double_button(double) 
        looper.set_loop_halve_button(halve) 

    def _setup_device_and_transport_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        bank_button_labels = ('Clip_Track_Button', 'Device_On_Off_Button', 'Previous_Device_Button', 'Next_Device_Button', 'Detail_View_Button', 'Rec_Quantization_Button', 'Midi_Overdub_Button', 'Device_Lock_Button', 'Metronome_Button')
        for index in range(8):
            device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 58 + index))
            device_bank_buttons[-1].name = bank_button_labels[index]
            ring_mode_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 24 + index)
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 0, 16 + index, Live.MidiMap.MapMode.absolute)
            ringed_encoder.set_ring_mode_button(ring_mode_button)
            ringed_encoder.set_feedback_delay(-1) #added from Axiom DirectLink example
            ringed_encoder.name = 'Device_Control_' + str(index)
            ring_mode_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            device_param_controls.append(ringed_encoder)
        self._device = ShiftableDeviceComponent()
        self._device.name = 'Device_Component'
        self._device.set_bank_buttons(tuple(device_bank_buttons))
        self._device.set_shift_button(self._shift_button)
        self._device.set_parameter_controls(tuple(device_param_controls))
        self._device.set_on_off_button(device_bank_buttons[1])
        self.set_device_component(self._device)
        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_shift_button(self._shift_button)
        detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])
        detail_view_toggler.set_detail_toggle_button(device_bank_buttons[4])
        detail_view_toggler.set_device_nav_buttons(device_bank_buttons[2], device_bank_buttons[3])
        transport = ShiftableTransportComponent()
        transport.name = 'Transport'
        play_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 91)
        stop_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 92)
        record_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 93)
        nudge_up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 100)
        nudge_down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 101)
        tap_tempo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 99)
        play_button.name = 'Play_Button'
        stop_button.name = 'Stop_Button'
        record_button.name = 'Record_Button'
        nudge_up_button.name = 'Nudge_Up_Button'
        nudge_down_button.name = 'Nudge_Down_Button'
        tap_tempo_button.name = 'Tap_Tempo_Button'
        transport.set_shift_button(self._shift_button)
        transport.set_play_button(play_button)
        transport.set_stop_button(stop_button)
        transport.set_record_button(record_button)
        transport.set_nudge_buttons(nudge_up_button, nudge_down_button)
        transport.set_undo_button(nudge_down_button) #shifted nudge
        transport.set_redo_button(nudge_up_button) #shifted nudge
        transport.set_tap_tempo_button(tap_tempo_button)
        self._device.set_lock_button(tap_tempo_button) #shifted tap tempo
        transport.set_quant_toggle_button(device_bank_buttons[5])
        transport.set_overdub_button(device_bank_buttons[6])
        transport.set_metronome_button(device_bank_buttons[7])
        transport.set_tempo_encoder(self._prehear_control) #shifted prehear
        bank_button_translator = ShiftableTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(device_bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)


    def _setup_global_control(self):
        is_momentary = True
        self._global_bank_buttons = []
        self._global_param_controls = []
        for index in range(8):
            ring_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, 0, 56 + index)
            ringed_encoder = RingedEncoderElement(MIDI_CC_TYPE, 0, 48 + index, Live.MidiMap.MapMode.absolute)
            ringed_encoder.name = 'Track_Control_' + str(index)
            ringed_encoder.set_feedback_delay(-1)
            ring_button.name = ringed_encoder.name + '_Ring_Mode_Button'
            ringed_encoder.set_ring_mode_button(ring_button)
            self._global_param_controls.append(ringed_encoder)
        self._global_bank_buttons = []
        global_bank_labels = ('Pan_Button', 'Send_A_Button', 'Send_B_Button', 'Send_C_Button')
        for index in range(4):
            self._global_bank_buttons.append(ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 87 + index))#(not is_momentary, MIDI_NOTE_TYPE, 0, 87 + index))
            self._global_bank_buttons[-1].name = global_bank_labels[index]
        self._encoder_modes = EncoderMixerModeSelectorComponent(self._mixer)
        self._encoder_modes.name = 'Track_Control_Modes'
        #self._encoder_modes.set_modes_buttons(self._global_bank_buttons) # set in ShiftableEncoderSelectorComponent
        self._encoder_modes.set_controls(tuple(self._global_param_controls))
        #self._encoder_device_modes = EncoderDeviceModeSelectorComponent(self._mixer, self._device) #new
        self._encoder_device_modes = EncoderDeviceComponent(self._mixer, self._device, self)
        self._encoder_device_modes.name = 'Alt_Device_Control_Modes' #new
        self._encoder_eq_modes = EncoderEQComponent(self._mixer, self)#EncoderEQModeSelectorComponent(self._mixer) #new
        self._encoder_eq_modes.name = 'EQ_Control_Modes' #new
        global_translation_selector = ChannelTranslationSelector() #translate track encoders to channels 1 through 4, based on button selection (pan = 1, send A = 2, send B = 3, send C = 4)
        global_translation_selector.name = 'Global_Translations'
        global_translation_selector.set_controls_to_translate(tuple(self._global_param_controls))
        global_translation_selector.set_mode_buttons(tuple(self._global_bank_buttons))
        encoder_user_modes = EncoderUserModesComponent(self, self._encoder_modes, tuple(self._global_param_controls), tuple(self._global_bank_buttons), self._mixer, self._device, self._encoder_device_modes, self._encoder_eq_modes) #self._mixer, tuple(sliders)) #added
        encoder_user_modes.name = 'Encoder_User_Modes' #added   
        self._encoder_shift_modes = ShiftableEncoderSelectorComponent(self, tuple(self._global_bank_buttons), encoder_user_modes, self._encoder_modes, self._encoder_eq_modes, self._encoder_device_modes) #tuple(select_buttons), master_select_button, tuple(arm_buttons), self._matrix, self._session, self._session_zoom, self._mixer, slider_modes, matrix_modes) #, self._send_introduction_message) #also added self for _parent
        self._encoder_shift_modes.name = 'Encoder_Shift_Modes'
        self._encoder_shift_modes.set_mode_toggle(self._shift_button)     


    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        #self._slider_modes.update() #added to update alternate slider assignments
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if device_to_select == None and len(track.devices) > 0:
            device_to_select = track.devices[0]
        if device_to_select != None:
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)
        return None

    def _product_model_id_byte(self):
        return 115
