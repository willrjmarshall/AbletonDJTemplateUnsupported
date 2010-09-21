
http://remotescripts.blogspot.com

-------------------
APS40_22 revision 3
-------------------

This set of Python scripts adds APC20/Launchpad-style User Mode/Note Mode functionality to the APC40, with additional shifted control mappings. Compatible with Live 8.1 & higher, on PC or mac.

To use, drop the APC40_22 folder into Ableton's MIDI Remote Scripts directory, and select APC40_22 from the MIDI Preferences dialog. Switch Track Input to "On" for Note Mode, and switch Remote to "On" for User Modes. Consider switching Takeover Mode to "Value Scaling" when using sliders or encoders in User mode.


Modifications and customizations include the following (refer also to APC40_22.jpg for custom control map example):

------
Matrix
------

* Shift + Track Select buttons = Matrix Modes selection. There are 8 Matrix Modes available. The default setup of the Matrix Modes is as follows:

* Shift + Track Select 1 = Clip Launch (default)
* Shift + Track Select 2 = Session Overview
* Shift + Track Select 3 = User 1 -> 8 x 6 Note Mode grid on Channel 10, Drum Rack mapping (4 notes wide)
* Shift + Track Select 4 = User 2 -> 8 x 6 Note Mode grid on Channel 11, notes laid out left to right (8 notes wide)
* Shift + Track Select 5 = User 3 -> 8 x 6 Note Mode grid on Channel 12, same as previous, but with sharps turned off
* Shift + Track Select 6 = User 4 -> 8 x 5 Note Mode grid on Channel 13, double grid 4 notes wide; does not use Clip Stop buttons
* Shift + Track Select 7 = User 5 -> 8 x 6 Note Mode grid on Channel 14, notes ascend in vertical columns
* Shift + Track Select 8 = User 6 -> 8 x 6 user Mode grid on Channel 15, no MIDI notes sent

For each of the User Matrix Modes, the following options are available for customization (by editing the Matrix_Maps.py file):
* LED colour assignment for each button
* MIDI note assignment for each button
* Channel assignment for entire grid
* Stop Track buttons included as part of grid
* Note Mode or User Mode setting (Note Mode sends MIDI notes, except where buttons are mapped; User Mode does not send MIDI notes).

The Drum Rack selection box is automapped to MIDI notes 36 through 72 on Channel 10 (User Mode 1 by default). This is the lower left 4 x 4 grid of User Mode 1, also coloured solid green by default.

-------
Sliders
-------

* Shift + Arm buttons = Slider Reassignment. 8 Slider Modes are available (left to right):

* Shift + Arm button 1 = Volume (default)
* Shift + Arm button 2 = Pan
* Shift + Arm button 3 = Send A
* Shift + Arm button 4 = Send B
* Shift + Arm button 5 = Send C
* Shift + Arm button 6 = User 1
* Shift + Arm button 7 = User 2
* Shift + Arm button 8 = User 3

--------------
Track Encoders
--------------
* Shift + Track Control buttons = Encoder Modes selection. There are 4 Encoder Modes available:

* Shift + Pan = Default (Pan / Send A / Send B / Send C)
* Shift + Send A = Alternate Device Mode. Encoders mirror the currently selected Device. In this mode, the track control buttons operate as follows (left to right):
	* Device Lock/Load - selecting locks the current Device, so that it won't change when switching tracks; deselecting unlocks then loads the new current Device
	* Device On/Off
	* Device Bank Left - select to scroll Left (lights up when there are additional banks available for scroll left)
	* Device Bank Right - select to scroll right (lights up when there are addtional banks available for scroll right)
* Shift + Send B = EQ/Filter Mode. In this mode, Encoders 1 & 5 will map to current track's Device Filter & Cutoff (if track has device with Filter/Cutoff controls); Encoders 2, 3 & 4 will map to track's Send A, Send B & Send C; Encoders 6, 7 & 8 will map to track's first three EQ controls (Low, Mid & High, if track has EQ3). In this mode, the track control buttons operate as follows (left to right):
	*EQ Lock/Load - selecting locks to the current track's EQ/Filter/Pans; deselecting unlocks then loads the new current track's EQ/Filter/Pans
	*EQ Low Cut (lights up when cut is active)
	*EQ Mid Cut (lights up when cut is active)
	*EQ High Cut (lights up when cut is active)
* Shift + Send C = User Mode. Encoders and track buttons can be user-mapped.

* In Default Mode, pressing and holding the Pan button switches between Pan control and Volume control for the 8 encoders.

-----
Other
-----

* Shift + Tap Tempo = Device Lock.
* Shift + Nudge- = Undo.
* Shift + Nudge+ = Redo.
* Shift + Cue Volume = Tempo Control.

----------------
Revision History
----------------

2010-08-10
* APC40_22 revision 3 - Added Press & Hold feature for Pan button (to switch between Pan and Volume control modes); fixed bug where manual MIDI-mapping of Pan encoders would prevent Send modes from operating; fixed bug where either sliders or encoders (but not both) would follow session highlight (aka "red box") when mapped to same control.

2010-07-15
* APC40_22 revision 2 - Fixed bug: Encoder LEDs now update without lag, when device parameters are being controlled by another element (such as sliders).

2010-06-29
* APC40_22 revision 1 - Fixed bug: Track Encoders in EQ/Filter Mode (Shift + Send B) would sometimes would not fully release parameters.

2010-06-28 
* Initial APC40_22 release, built on APC40_21 script rev.0

Visit http://remotescripts.blogspot.com for the latest updates and more information


----------
DISCLAIMER
----------

THESE FILES ARE PROVIDED AS-IS, WITHOUT ANY WARRANTY, EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO FITNESS FOR ANY PARTICULAR PURPOSE.