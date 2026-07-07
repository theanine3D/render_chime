import bpy
import os
import platform
import shutil
import subprocess
from bpy.app.handlers import persistent


bl_info = {
    "name": "Render Chime",
    "blender": (2, 80, 0),
    "author": "Theanine3D",
    "category": "Render",
    "version": (1, 2, 0),
    "description": "Plays a chime after rendering.",
    "support": "COMMUNITY"
}

try:
    import winsound
except ImportError:
    winsound = None

try:
    import aud
except ImportError:
    aud = None

# Keep references to the audio device and playback handle at module level.
# If they get garbage collected, the sound cuts off immediately
_aud_device = None
_aud_handle = None


def play_chime(filepath):
    global _aud_device, _aud_handle

    if not filepath:
        print("Render Chime: no sound effect file configured.")
        return

    filepath = bpy.path.abspath(filepath)
    if not os.path.exists(filepath):
        print("Render Chime: sound effect file not found: " + filepath)
        return

    # Preferred method: Blender's bundled Audaspace engine ("aud"). Works the
    # same on every OS and inside sandboxed builds (Flatpak/Snap), with no
    # external programs needed. Skipped when Blender's audio device is
    # disabled or running headless, since playback would be silent
    use_aud = aud is not None and not bpy.app.background
    try:
        if str(bpy.context.preferences.system.audio_device).upper() in {"NONE", "NULL"}:
            use_aud = False
    except Exception:
        pass

    if use_aud:
        try:
            if _aud_device is None:
                _aud_device = aud.Device()
            _aud_handle = _aud_device.play(aud.Sound(filepath))
            return
        except Exception as e:
            print(f"Render Chime: Blender audio device unavailable ({e}). Trying fallback players...")

    if platform.system() == "Windows" and winsound is not None:
        try:
            winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            print("Render Chime: couldn't play the sound effect. Using system beep as fallback...")
            winsound.MessageBeep()
        return

    # Linux and macOS fallbacks. Arguments are passed as a list (no shell), so
    # paths with spaces are safe, and Popen keeps the UI from blocking
    fallback_players = (
        ["pw-play"],       # PipeWire
        ["paplay"],        # PulseAudio
        ["afplay"],        # macOS
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"],
        ["aplay", "-q"],   # bare ALSA
    )
    for player in fallback_players:
        if shutil.which(player[0]):
            try:
                subprocess.Popen(player + [filepath],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                return
            except Exception:
                continue

    print("Render Chime: no working audio playback method was found on this system.")


def get_default_sound_path():
    # Get the path to the addon
    addon_path = os.path.dirname(os.path.abspath(__file__))
    default_sound_path = os.path.join(addon_path, "default.wav")
    return default_sound_path if os.path.exists(default_sound_path) else None


def get_sound_path():
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    return addon_prefs.sound_file_path if addon_prefs.sound_file_path else get_default_sound_path()


@persistent
def render_complete(scene, context=None):
    play_chime(get_sound_path())


@persistent
def bake_complete(scene, context=None):
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.affect_bakes:
        play_chime(get_sound_path())


class RenderChimePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    sound_file_path: bpy.props.StringProperty(
        name="Sound File Path",
        subtype='FILE_PATH',
        description="File path to the sound to be played after rendering",
        default="")

    affect_bakes: bpy.props.BoolProperty(
        name="Affect Bakes",
        description="If enabled, completed texture bakes will also trigger the sound effect",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "sound_file_path")
        layout.prop(self, "affect_bakes")


class ViewportRenderChime(bpy.types.Operator):
    """Performs a viewport render with animation enabled, but with a sound effect played when the render finishes"""
    bl_idname = "render.viewport_render_chime"
    bl_label = "Viewport Render Animation (Chime)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.render.opengl(animation=True)

        sound_file_path = get_sound_path()
        play_chime(sound_file_path)

        return {'FINISHED'}


classes = (
    RenderChimePreferences,
    ViewportRenderChime
)


def menu_func(self, context):
    self.layout.operator(ViewportRenderChime.bl_idname)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    if render_complete not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(render_complete)
    if bpy.app.version >= (3, 0, 0):
        if bake_complete not in bpy.app.handlers.object_bake_complete:
            bpy.app.handlers.object_bake_complete.append(bake_complete)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    if render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(render_complete)
    if bpy.app.version >= (3, 0, 0):
        if bake_complete in bpy.app.handlers.object_bake_complete:
            bpy.app.handlers.object_bake_complete.remove(bake_complete)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()
