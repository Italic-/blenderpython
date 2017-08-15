##  Thanks to Frankie Hobbins, Joel Daniels, Julien Duroure, Hjalti Hjalmarsson, Bassam Kurdali, Luciano Munoz, Cristian Hasbun and anyone that I left out!
# Latest update: adding Advanced Boomsmash

bl_info = {
    "name": "Animator's Toolbox",
    "description": "A set of tools specifically for animators.",
    "author": "Brandon Ayers (thedaemon)",
    "version": (0, 3),
    "blender": (2, 77, 0),
    "location": "View3D > Toolbar > Animation > Animator's Toolbox",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/thedaemon/Blender-Scripts",
    "tracker_url": "https://github.com/thedaemon/Blender-Scripts/issues",
    "support": "TESTING",
    "category": "Animation"
    }

import os.path
import bpy
from bpy.props import *
from bpy.types import Operator

KEYMAPS = list()

# FEATURE: Jump forward/backward every N frames. Currently hardcoded variable.
class AnimatorsToolboxFrameJump(bpy.types.Operator):

    """Jump a number of frames forward/backwards"""
    bl_idname = "screen.animatorstools_frame_jump"
    bl_label = "Jump Frames"

    forward = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        scene = context.scene
        framedelta = 4
        if self.forward:
            scene.frame_current = scene.frame_current + framedelta
        else:
            scene.frame_current = scene.frame_current - framedelta

        return {"FINISHED"}

# FEATURE: A toggle to keep the animator from selecting something other than the Armature.
class ToggleSelectability(bpy.types.Operator):
    """Turns off selection for all objects leaving only Armatures selectable"""
    bl_idname = "bone.toggleselectability"
    bl_label = "Armature Selection Only"

    def execute(self, context):
        do_i_hide_select = not bpy.context.active_object.hide_select
        if bpy.context.selected_objects == []:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    ob.hide_select = True
            else:
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        ob.hide_select = do_i_hide_select
        else:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        do_i_hide_select2 = not ob.hide_select
                        for ob in bpy.context.scene.objects:
                            ob.hide_select = do_i_hide_select2
                        break
                bpy.context.object.hide_select = False
            else:
                for ob in bpy.context.selected_objects:
                    ob.hide_select = not ob.hide_select
        return{'FINISHED'}

# Useless because blender already has this freaking command but I programmed it anyways. I may use it for specific axis template.
class ClearAllTransforms(bpy.types.Operator):
    """Clears all transforms on the bone I hope"""
    bl_idname = "pose.clearall"
    bl_label = "Clear Transforms"

    def execute(self,context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                bpy.ops.pose.rot_clear()
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.scale_clear()
        return{'FINISHED'}

# FEATURE: A toggle for OpenSubdiv on all objects in scene with a Subdivision Surface Modifier.
class ToggleOpensubdiv(bpy.types.Operator):
    """Toggles OpenSubdiv for all Objects for improved animation playback speed"""
    bl_idname = "mesh.opensubdiv"
    bl_label = "Mesh OpenSubdiv"
    # Does nothing, testing.
    my_bool = bpy.props.BoolProperty(name="Toggle Option")

    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            if mm.use_opensubdiv == True:
                mm.use_opensubdiv = False
            else:
                if mm.use_opensubdiv == False:
                    mm.use_opensubdiv = True
        return{'FINISHED'}

# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface Modifiers for improved viewport performance.
class OpensubdivOn(bpy.types.Operator):
    bl_idname = "opensubdiv.on"
    bl_label = "OpenSubdiv On"

    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = True
        return{'FINISHED'}

# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface Modifiers for improved viewport performance.
class OpensubdivOff(bpy.types.Operator):
    bl_idname = "opensubdiv.off"
    bl_label = "OpenSubdiv Off"

    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = False
        return{'FINISHED'}

# FEATURE: Simple X-Ray toggle for Armature
class ToggleXray(bpy.types.Operator):
    """Toggles X-Ray mode for bones"""
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                obj.show_x_ray = not obj.show_x_ray
        return{'FINISHED'}


## UI ##
from bpy.types import PropertyGroup, Panel
from bpy.props import *

class animatorstoolboxData(PropertyGroup):
    bl_idname = 'animatorstoolboxDataUI'
    """
    UI property group for the add-on  WORK IN PROGRESS

    Options to adjust how the panel is displayed.

    bpy > types > WindowManager > animatorstoolboxDataUI
    bpy > context > window_manager > animatorstoolboxDataUI
    """
    displayMode = BoolProperty(name='Display Mode', description="Use this to hi"
                               "de many of the options below that are generally"
                               " needed while rigging. (Useful for animating.)",
                               default=False)

# Animator's Toolbox Main Panel
def draw_animatorstoolbox_panel(context, layout):
#--Defining shortcuts for commands
    obj = context.object
    userpref = context.user_preferences
    obj = context.object
    edit = userpref.edit
    toolsettings = context.tool_settings
    scene = context.scene
    screen = context.screen
    rd = scene.render
    cscene = scene.cycles
#--Keying
    col = layout.column(align=True)
    col.label(text="Keyframes:")
    row = layout.row(align=True)
    row.prop(toolsettings, "use_keyframe_insert_auto", text="", toggle=True)
    if toolsettings.use_keyframe_insert_auto:
        row.prop(toolsettings, "use_keyframe_insert_keyingset", text="", toggle=True)
        if screen.is_animation_playing:
            subsub = row.row()
            subsub.prop(toolsettings, "use_record_with_nla", toggle=True)
    row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
    row.operator("screen.animation_play", text="", icon='PLAY')
    row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
    row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
#--Pose Tools
    col = layout.column(align=True)
    col.label(text="Pose:")
    row = col.row(align=True)
    row.operator("pose.copy", text="Copy")
    row.operator("pose.paste", text="Paste")
    row.operator("pose.paste", text="Flipped").flipped = True
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.breakdown", text="Breakdowner")
    row.operator("pose.push", text="Push")
    row.operator("pose.relax", text="Relax")
    col = layout.column(align=True)
    row = col.row()
    row.prop(context.active_object.data, "use_auto_ik", text="Auto IK")
    row.prop(obj, "show_x_ray", text="X Ray")
#--Reset Transforms
    col = layout.column(align=True)
    col.label(text="Reset Transforms:")
    row = layout.row(align=True)
    row.operator("pose.loc_clear", text="Location")
    row.operator("pose.rot_clear", text="Rotation")
    row.operator("pose.scale_clear", text="Scale")
    col = layout.column(align=True)
    row = col.row()
    row.operator("pose.transforms_clear", text="Reset All")
#--Optimizations
    col = layout.column(align=True)
    col.label(text="Optimizations:")
    #col.layout.column(align=True)
    #col.label(text="OpenSubdiv")
    row = layout.row(align=True)
    row.label(text="OpenSubdiv")
    row.operator("opensubdiv.on", text="On")
    row.operator("opensubdiv.off", text="Off")
    row = layout.row(align=True)
    row.operator("bone.toggleselectability", text="Select Armature Only")
#--Simplify
    col = layout.column(align=True)
    col.label(text="Simplify:")
    row = layout.row(align=True)
    row.prop(rd, "use_simplify", text="Use Simplify")
    #layout.active = rd.use_simplify
    split = layout.split()
    col = split.column()
    col.label(text="Viewport:")
    col.prop(rd, "simplify_subdivision", text="Subdivision")
    col.prop(rd, "simplify_child_particles", text="Child Particles")
    col = split.column()
    col.label(text="Render:")
    col.prop(rd, "simplify_subdivision_render", text="Subdivision")
    col.prop(rd, "simplify_child_particles_render", text="Child Particles")
    col = layout.column()
    col.prop(cscene, "use_camera_cull")
    subsub = col.column()
    subsub.active = cscene.use_camera_cull
    subsub.prop(cscene, "camera_cull_margin")
#--Motion Path
    pchan = context.active_pose_bone
    mpath = pchan.motion_path if pchan else None
    col = layout.column(align=True)
    col.label(text="Motion Paths:")
    if mpath:
        row = col.row(align=True)
        row.operator("pose.paths_update", text="Update")
        row.operator("pose.paths_clear", text="", icon='X')
    else:
        col.operator("pose.paths_calculate", text="Calculate")
#--New Key Type
    col = layout.column(align=True)
    col.label(text="New Key Type:")
    col.prop(edit, "keyframe_new_interpolation_type", text='Keys')
    col.prop(edit, "keyframe_new_handle_type", text="Handles")

# Animator's ToolBox Draw Calls
class AnimatorsToolBox(bpy.types.Panel):
    """Creates a custom Animator Panel in the 3D View"""
    bl_label = "Animator's Toolbox"
    bl_idname = "ANIM_TOOLBOX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animation"
#--Header
    def draw_header(self, context):
        layout = self.layout
        #animatorstoolboxDataUIProps = context.window_manager.animatorstoolboxDataUI
        #layout.prop('animatorstoolboxDataUI', "displayMode", text="")
        DoBTN = self.layout

#--Draw Toolboxes
    def draw(self, context):
        layout = self.layout
        #animatorstoolboxData = context.window_manager.animatorstoolboxDataUI
        draw_animatorstoolbox_panel(context, layout)


classes = [
    AnimatorsToolboxFrameJump,
    ToggleSelectability,
    ClearAllTransforms,
    ToggleOpensubdiv,
    OpensubdivOn,
    OpensubdivOff,
    ToggleXray,
    AnimatorsToolBox,
    animatorstoolboxData
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="Frames")
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump", "RIGHT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = True
    KEYMAPS.append((km, kmi))
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump", "LEFT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = False
    KEYMAPS.append((km, kmi))

def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()

if __name__ == "__main__":
    register()
