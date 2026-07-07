# Render Chime

Render Chime is a Blender (2.8x / 3.x / 4.x / 5.x) addon that plays a sound effect when your render or bake task has completed.

Finding this addon useful? Please consider starring it ⭐, or [donating](https://ko-fi.com/theanine3d) 🙂<br>

## Features
- Sound effect is customizeable. Most common audio formats (WAV, OGG, FLAC, MP3) should work.
- Works on Windows, Linux, and macOS.
- Sound is triggered by completed renders, and on Blender versions 3.0 or higher, texture bake tasks as well
 
## Notes
- You may set a custom sound file in the addon's preferences, which can be accessed in the same preferences panel where you enable the addon.
- The sound is played through Blender's own audio engine, so no external audio packages are required, and it works in sandboxed Blender builds (Flatpak / Snap) too.
- If Blender's audio device is disabled (Preferences → System → Audio Device set to "None"), the addon falls back to an external command-line player: pw-play (PipeWire), paplay (PulseAudio), afplay (macOS), ffplay, or aplay (ALSA) — whichever is found first.

## Installation
1. Press the big green Code button above and choose "Download ZIP"
2. Open Blender Preferences and click on the "Addons" tab
3. Click on the "install" button and select your newly downloaded ZIP
