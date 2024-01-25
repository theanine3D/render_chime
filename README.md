![Untitled](https://github.com/theanine3D/render_chime/assets/88953117/a5f20952-b2e0-4752-84dd-b0c78359820d)

# Render Chime

Render Chime is a Blender (2.8x / 3.x / 4.x) addon that plays a sound effect when your render or bake task has completed.

## Features
- Sound effect is customizeable. Most .WAV files should work.
- Works on Windows and Linux.
- Sound is triggered by completed renders, and on Blender versions 3.0 or higher, texture bake tasks as well
 
## Notes
- You may set a custom sound file (must be .wav format) in the addon's preferences, which can be accessed in the same preferences panel where you enable the addon.
- Linux users must have at least 1 of the following audio packages installed in your distribution: PulseAudio, ALSA, or beep. The addon will attempt to play a sound using these packages in this order, using 'beep' as a fallback if the first two fail. If you hear no sound, check to make sure that the "paplay", "aplay", or "beep" commands are working properly via the command line.

## Installation
1. Press the big green Code button above and choose "Download ZIP"
2. Open Blender Preferences and click on the "Addons" tab
3. Click on the "install" button and select your newly downloaded ZIP
