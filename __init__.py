import bpy
import os
import platform
from bpy.app.handlers import persistent


bl_info = {
    "name": "Render Chime",
    "blender": (2, 80, 0),
    "author": "Theanine3D",
    "category": "Render",
    "version": (1, 1, 0),
    "author": "Theanine3D",
    "description": "Plays a chime after rendering.",
    "support": "COMMUNITY"
}

try:
    import winsound
except ImportError:
    winsound = None

def play_chime(filepath):
    sound_played = False

    if os.path.exists(filepath):

        if winsound and platform.system() == "Windows":
            try:
                winsound.PlaySound(filepath, winsound.SND_FILENAME)
                sound_played = True
            except:
                print("Couldn't play specified sound effect. Using system beep as fallback...")
                winsound.MessageBeep()

        elif platform.system() == "Linux":
            # Try using paplay
            if os.system(f"which paplay") == 0:
                os.system(f"paplay {filepath}")
                sound_played = True
            # If paplay is not available, try aplay
            elif os.system(f"which aplay") == 0:
                os.system(f"aplay {filepath}")
                sound_played = True
            # If all else fails, try beep
            elif os.system(f"which beep") == 0:
                os.system('beep')
                sound_played = True
            else:
                sound_played = False
        if not sound_played:
            print("Chime sound feature is not supported on this operating system.")
    else:
        print("Sound effect file not found.")

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
def render_complete(scene, context):
    sound_file_path = get_sound_path()
    play_chime(sound_file_path)

class RenderChimePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    sound_file_path: bpy.props.StringProperty(
        name="Sound File Path",
        subtype='FILE_PATH',
        description="File path to the .wav sound to be played after rendering",
        default="")
    
    affect_bakes: bpy.props.BoolProperty(
        name="Affect Bakes",
        description="If enabled, completed texture bakes will also trigger the sound effect",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "sound_file_path")

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
        if render_complete not in bpy.app.handlers.object_bake_complete:
            bpy.app.handlers.object_bake_complete.append(render_complete)
    bpy.types.VIEW3D_MT_view.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.utils.unregister_class(RenderChimePreferences)
    if render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(render_complete)
    if bpy.app.version >= (3, 0, 0):
        if render_complete in bpy.app.handlers.object_bake_complete:
            bpy.app.handlers.object_bake_complete.remove(render_complete)
    bpy.types.VIEW3D_MT_view.remove(menu_func)

if __name__ == "__main__":
    register()

