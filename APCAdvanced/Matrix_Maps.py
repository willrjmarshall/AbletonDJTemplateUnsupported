# http://remotescripts.blogspot.com
# Mappings for APC40_21 USER MODE/NOTE MODE are defined in this file
# Values may be edited with any text editor, but avoid using tabs for indentation

#---------- Page 1 is Clip Launch

#---------- Page 2 is Session Overview

#---------- Page 3 is User Mode 1

#set USE_STOP_MODE to True in order to use Track Stop buttons as part of Note Mode/User Mode grid, otherwise set to False.
USE_STOP_ROW_1 = True 

#set IS_NOTE_MODE to True for Note Mode (sends MIDI notes), or set to False for User Mode (does not send MIDI notes)
IS_NOTE_MODE_1 = True

# The PATTERN array represents the colour values for each button in the grid; there are 6 rows and 8 columns
# The LED colour values are: 0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
# The last row represents the Track Stop buttons; these values will be ignored unless USE_STOP_ROW is set to True
# The Track Stop buttons can be set to 0=off or 1-127=green
PATTERN_1 = ((3, 3, 3, 3, 5, 5, 5, 5), #Row 1
             (3, 3, 3, 3, 5, 5, 5, 5), #Row 2
             (1, 1, 1, 1, 1, 1, 1, 1), #Row 3
             (1, 1, 1, 1, 3, 3, 3, 3), #Row 4
             (1, 1, 1, 1, 3, 3, 3, 3), #Row 5
             (1, 1, 1, 1, 1, 1, 1, 1), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

# The CHANNEL value sets the MIDI Channel for the entire grid. 
# Values 0 through 15 correspond to MIDI channels 1 through 16. 
# Channels 0 through 8 should be avoided, to prevent conflict with the APC40's native mappings
CHANNEL_1 = 9

# The NOTEMAP array represents the MIDI note values for each button in the grid; there are 6 rows and 8 columns
# Valid note values are 0 through 127
# The last row represents the Track Stop buttons; these values will be ignored unless USE_STOP_ROW is set to True
NOTEMAP_1 = ((56, 57, 58, 59, 80, 81, 82, 83), #Row 1
             (52, 53, 54, 55, 76, 77, 78, 79), #Row 2
             (48, 49, 50, 51, 72, 73, 74, 75), #Row 3
             (44, 45, 46, 47, 68, 69, 70, 71), #Row 4
             (40, 41, 42, 43, 64, 65, 66, 67), #Row 5
             (36, 37, 38, 39, 60, 61, 62, 63), #Clip Stop Row
             )

#---------- Page 4 is User Mode 2

USE_STOP_ROW_2 = True
IS_NOTE_MODE_2 = True

PATTERN_2 = ((5, 5, 5, 5, 5, 5, 5, 5), #Row 1
             (1, 1, 1, 1, 5, 5, 5, 5), #Row 2
             (1, 1, 1, 1, 1, 1, 1, 1), #Row 3
             (3, 3, 3, 3, 3, 3, 3, 3), #Row 4
             (1, 1, 1, 1, 3, 3, 3, 3), #Row 5
             (1, 1, 1, 1, 1, 1, 1, 1), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

CHANNEL_2 = 10

NOTEMAP_2 = ((76, 77, 78, 79, 80, 81, 82, 83), #Row 1
             (68, 69, 70, 71, 72, 73, 74, 75), #Row 2
             (60, 61, 62, 63, 64, 65, 66, 67), #Row 3
             (52, 53, 54, 55, 56, 57, 58, 59), #Row 4
             (44, 45, 46, 47, 48, 49, 50, 51), #Row 5
             (36, 37, 38, 39, 40, 41, 42, 43), #Clip Stop Row
             )

#---------- Page 5 is User Mode 3

USE_STOP_ROW_3 = True
IS_NOTE_MODE_3 = True

PATTERN_3 = ((5, 5, 0, 5, 0, 5, 0, 5), #Row 1
             (0, 1, 0, 1, 5, 0, 5, 0), #Row 2
             (1, 0, 1, 0, 1, 1, 0, 1), #Row 3
             (3, 3, 0, 3, 0, 3, 0, 3), #Row 4
             (0, 1, 0, 1, 3, 0, 3, 0), #Row 5
             (1, 0, 1, 0, 1, 1, 0, 1), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

CHANNEL_3 = 11

NOTEMAP_3 = ((76, 77, 78, 79, 80, 81, 82, 83), #Row 1
             (68, 69, 70, 71, 72, 73, 74, 75), #Row 2
             (60, 61, 62, 63, 64, 65, 66, 67), #Row 3
             (52, 53, 54, 55, 56, 57, 58, 59), #Row 4
             (44, 45, 46, 47, 48, 49, 50, 51), #Row 5
             (36, 37, 38, 39, 40, 41, 42, 43), #Clip Stop Row
             )

#---------- Page 6 is User Mode 4

USE_STOP_ROW_4 = False
IS_NOTE_MODE_4 = True

PATTERN_4 = ((5, 1, 5, 1, 3, 1, 3, 1), #Row 1
             (1, 5, 1, 5, 1, 3, 1, 3), #Row 2
             (5, 1, 5, 1, 3, 1, 3, 1), #Row 3
             (1, 5, 1, 5, 1, 3, 1, 3), #Row 4
             (5, 1, 5, 1, 3, 1, 3, 1), #Row 5
             (1, 1, 1, 1, 1, 1, 1, 1), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

CHANNEL_4 = 12

NOTEMAP_4 = ((56, 57, 58, 59, 80, 81, 82, 83), #Row 1
             (52, 53, 54, 55, 76, 77, 78, 79), #Row 2
             (48, 49, 50, 51, 72, 73, 74, 75), #Row 3
             (44, 45, 46, 47, 68, 69, 70, 71), #Row 4
             (40, 41, 42, 43, 64, 65, 66, 67), #Row 5
             (36, 37, 38, 39, 60, 61, 62, 63), #Clip Stop Row
             )

#---------- Page 7 is User Mode 5

USE_STOP_ROW_5 = True
IS_NOTE_MODE_5 = True

PATTERN_5 = ((1, 5, 3, 1, 5, 3, 1, 5), #Row 1
             (1, 5, 3, 1, 5, 3, 1, 5), #Row 2
             (1, 5, 3, 1, 5, 3, 1, 5), #Row 3
             (1, 5, 3, 1, 5, 3, 1, 5), #Row 4
             (1, 5, 3, 1, 5, 3, 1, 5), #Row 5
             (1, 1, 1, 1, 1, 1, 1, 5), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

CHANNEL_5 = 13

NOTEMAP_5 = ((41, 47, 53, 59, 65, 71, 77, 83), #Row 1
             (40, 46, 52, 58, 64, 70, 76, 82), #Row 2
             (39, 45, 51, 57, 63, 69, 75, 81), #Row 3
             (38, 44, 50, 56, 62, 68, 74, 80), #Row 4
             (37, 43, 49, 55, 61, 67, 73, 79), #Row 5
             (36, 42, 48, 54, 60, 66, 72, 78), #Clip Stop Row
             )

#---------- Page 8 is User Mode 6

USE_STOP_ROW_6 = True
IS_NOTE_MODE_6 = False

PATTERN_6 = ((3, 3, 3, 3, 3, 3, 3, 3), #Row 1
             (5, 5, 5, 5, 5, 5, 5, 5), #Row 2
             (1, 1, 1, 1, 1, 1, 1, 1), #Row 3
             (3, 3, 3, 3, 3, 3, 3, 3), #Row 4
             (5, 5, 5, 5, 5, 5, 5, 5), #Row 5
             (1, 1, 1, 1, 1, 1, 1, 1), #Clip Stop Row
             ) #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green

CHANNEL_6 = 14

NOTEMAP_6 = ((56, 57, 58, 59, 80, 81, 82, 83), #Row 1
             (52, 53, 54, 55, 76, 77, 78, 79), #Row 2
             (48, 49, 50, 51, 72, 73, 74, 75), #Row 3
             (44, 45, 46, 47, 68, 69, 70, 71), #Row 4
             (40, 41, 42, 43, 64, 65, 66, 67), #Row 5
             (36, 37, 38, 39, 60, 61, 62, 63), #Clip Stop Row
             )

#---------- Pad Translations for Drum Rack

# The PAD_TRANSLATIONS array represents a 4 x 4 Drum Rack
# Each slot in the rack is identified using X,Y coordinates, and mapped to a MIDI note and MIDI channel:
# (pad_x, pad_y, note, channel)
# Only one drum rack can be used at a time; maximum grid size is 4 x 4 (LiveAPI limitation)
PAD_TRANSLATIONS = ((0, 0, 48, 9), (1, 0, 49, 9), (2, 0, 50, 9), (3, 0, 51, 9), 
                    (0, 1, 44, 9), (1, 1, 45, 9), (2, 1, 46, 9), (3, 1, 47, 9),
                    (0, 2, 40, 9), (1, 2, 41, 9), (2, 2, 42, 9), (3, 2, 43, 9),
                    (0, 3, 36, 9), (1, 3, 37, 9), (2, 3, 38, 9), (3, 3, 39, 9),
                    ) #(pad_x, pad_y, note, channel)