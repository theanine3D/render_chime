# Render Chime
Render Chime is a Blender (2.8x+ / 3.x / 4.x) addon that plays a sound effect when your render or bake task has completed.

## Features
- Sound effect is customizeable. Most .WAV files should work.
- Works on Windows and Linux.
- Sound is triggered by both completed renders and texture bake tasks.

## Notes
- You may set a custom sound file (must be .wav format) in the addon's preferences, which can be accessed in the same preferences panel where you enable the addon.
- Linux users must have at least 1 of the following audio packages installed in your distribution: PulseAudio, ALSA, or beep. The addon will attempt to play a sound using these packages in this order, using 'beep' as a fallback if the first two fail.

## Installation
1. Press the big green Code button above and choose "Download ZIP"
2. Open Blender Preferences and click on the "Addons" tab
3. Click on the "install" button and select your newly downloaded ZIP
