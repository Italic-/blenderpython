# space_view_3d_display_tools.py Copyright (C) 2014, Jordi Vall-llovera
#
# Multiple display tools for fast navigate/interact with the viewport
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "AF: Display Tools",
    "author": "Jordi Vall-llovera Medina, Jhon Wallace",
    "version": (1, 6, 0),
    "blender": (2, 7, 0),
    "location": "Toolshelf",
    "description": "Display tools for fast navigate/interact with the viewport",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/"
                "3D_interaction/Display_Tools",
    "tracker_url": "",
    "category": "Addon Factory"}

# Import From Files
if "bpy" in locals():
    import importlib
    importlib.reload(display_mode)
    importlib.reload(fast_navigate)
    importlib.reload(modifier_tools)
    importlib.reload(scene_vis)
    importlib.reload(shading_menu)

else:
    from . import display_mode
    from . import fast_navigate
    from . import modifier_tools
    from . import scene_vis
    from . import shading_menu

import bpy
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        AddonPreferences,
        PointerProperty,
        )
from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        StringProperty,
        )

from bpy_extras import view3d_utils

# define base dummy class for inheritance
class BasePollCheck:
    @classmethod
    def poll(cls, context):
        return True


class DisplayToolsPanel(bpy.types.Panel):
    bl_label = 'Display Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Display'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        DISPLAYDROP = scene.UTDisplayDrop
        SHADINGDROP = scene.UTShadingDrop
        SCENEDROP = scene.UTSceneDrop
        MODIFIERDROP = scene.UTModifierDrop
        FASTNAVDROP = scene.UTFastnavDrop
        view = context.space_data
        toolsettings = context.tool_settings
        layout = self.layout
        ob = context.object
        # Display options
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTDisplayDrop", icon="TRIA_DOWN")
        if not DISPLAYDROP:
            row.prop(ob, "show_name", text="", icon='SORTALPHA')
            row.prop(ob, "show_texture_space", text="", icon='FACESEL_HLT')
            row.menu("VIEW3D_MT_Shade_menu", icon='SOLID', text="" )
        if DISPLAYDROP:
            col = box1.column(align=True)
            row = col.row(align=True)
            row.operator("view3d.display_draw_change", text="Textured",
                         icon='TEXTURE_SHADED').drawing = 'TEXTURED'
            row.operator("view3d.display_draw_change", text="Solid",
                        icon='SOLID').drawing = 'SOLID'
            col = box1.column(align=True)
            col.alignment = 'EXPAND'
            row = col.row()
            row.operator("view3d.display_draw_change", text="Wire",
                         icon='WIRE').drawing = 'WIRE'
            row.operator("view3d.display_draw_change", text="Bounds",
                         icon='BBOX').drawing = 'BOUNDS'

        # Shading options
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTShadingDrop", icon="TRIA_DOWN")
        if not SHADINGDROP:
            row.operator("view3d.display_wire_all1", text="", icon='WIRE')
        if SHADINGDROP:
            scene = context.scene
            layout = self.layout
            col = box1.column(align=True)
            col.alignment = 'EXPAND'
            row = col.row()
            row.operator("view3d.display_shade_smooth_flat",
                        text="Smooth").smoothing = True
            row.operator("view3d.display_shade_smooth_flat",
                        text="Flat").smoothing = False

            row = col.row()
            row.operator("view3d.display_shadeless_switch", "Shadeless On",
                          icon='SOLID').shades = True
            row.operator("view3d.display_shadeless_switch",
                         "Shadeless Off", icon='SOLID').shades = False

            row = col.row()
            row.operator("view3d.display_wire_switch", "Wire On",
                        icon='WIRE').wires = True
            row.operator("view3d.display_wire_switch", "Wire Off",
                        icon='WIRE').wires = False

            row = col.row()
            row.operator("view3d.display_bounds_switch", "Bounds On",
                        icon='BBOX').bounds = True
            row.operator("view3d.display_bounds_switch", "Bounds Off",
                        icon='BBOX').bounds = False

            row = col.row()
            row.operator("view3d.display_double_sided_switch",
                         "DSided On", icon='MESH_DATA').double_side = True
            row.operator("view3d.display_double_sided_switch",
                         "DSided Off", icon='MESH_DATA').double_side = False

            row = col.row()
            row.operator("view3d.display_x_ray_switch",
                         "XRay On", icon='GHOST_ENABLED').xrays = True
            row.operator("view3d.display_x_ray_switch",
                         "XRay Off", icon='GHOST_ENABLED').xrays = False

            row = col.row()
            scene = context.scene.display_tools
            row.prop(scene, "BoundingMode")
            row = col.row()

        # Scene options
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
        scene = context.scene
#        row.alignment = 'CENTER'
        row.prop(scene, "UTSceneDrop", icon="TRIA_DOWN")

        if SCENEDROP:
            layout = self.layout
            scene = context.scene
            render = scene.render
            space = context.space_data
            layout.prop(space, "show_manipulator")
            layout.prop(space, "show_outline_selected")
            layout.prop(space, "show_only_render")
            layout.prop(space, "show_textured_solid")
            layout.prop(space, "show_backface_culling")
            layout.prop(space, "show_all_objects_origin")
            layout.prop(render, "use_simplify", "Simplify")

            if scene.render.use_simplify is True:
                layout.label("Settings :")
                row = layout.row()
                box = row.box()
                box.prop(render, "simplify_subdivision", "Subdivision")
                box.prop(render, "simplify_shadow_samples", "Shadow Samples")
                box.prop(render, "simplify_child_particles", "Child Particles")
                box.prop(render, "simplify_ao_sss", "AO and SSS")
                layout.operator("view3d.display_simplify")

        # Modifier options
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTModifierDrop", icon="TRIA_DOWN")

        if MODIFIERDROP:
            layout = self.layout
            col = box1.column(align=True)
            col.alignment = 'EXPAND'
            row = col.row()
            row.operator("view3d.display_modifiers_render_switch", text="On",
                          icon='RENDER_STILL').mod_render = True
            row.operator("view3d.display_modifiers_render_switch",
                          text="Off").mod_render = False
            row.operator("view3d.display_modifiers_viewport_switch", text="On",
                         icon='RESTRICT_VIEW_OFF').mod_switch = True
            row.operator("view3d.display_modifiers_viewport_switch",
                        text="Off").mod_switch = False
            col = box1.column(align=True)
            row = col.row()
            row.operator("view3d.display_modifiers_edit_switch", text="On",
                        icon='EDITMODE_HLT').mod_edit = True
            row.operator("view3d.display_modifiers_edit_switch",
                        text="Off").mod_edit = False
            row.operator("view3d.display_modifiers_cage_set", text="On",
                         icon='EDITMODE_HLT').set_cage = True
            row.operator("view3d.display_modifiers_cage_set",
                         text="Off").set_cage = False
            row = col.row(align=True)
            row.operator("view3d.display_modifiers_expand_collapse", text="Expand",
                        icon='TRIA_DOWN').expands = True
            row.operator("view3d.display_modifiers_expand_collapse", text="Collapse",
                        icon='TRIA_RIGHT').expands = False
            row = col.row(align=True)
            row.operator("view3d.display_modifiers_apply", icon='MODIFIER')
            row.operator("view3d.display_modifiers_delete", icon='X')

            row = col.row(align=True)
            row.operator("view3d.display_modifiers_set_dummy",
                         icon='OUTLINER_OB_ARMATURE')
            row.operator("view3d.display_modifiers_delete_dummy",
                         icon='X')
            row = col.row(align=True)

            row.label("Subdivision Level", icon='MOD_SUBSURF')

            row = col.row(align=True)
            row.operator("view3d.modifiers_subsurf_level_set", text="0").level = 0
            row.operator("view3d.modifiers_subsurf_level_set", text="1").level = 1
            row.operator("view3d.modifiers_subsurf_level_set", text="2").level = 2
            row.operator("view3d.modifiers_subsurf_level_set", text="3").level = 3
            row.operator("view3d.modifiers_subsurf_level_set", text="4").level = 4
            row.operator("view3d.modifiers_subsurf_level_set", text="5").level = 5
            row.operator("view3d.modifiers_subsurf_level_set", text="6").level = 6

        # fast nav options
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTFastnavDrop", icon="TRIA_DOWN")

        if FASTNAVDROP:
            layout = self.layout
            scene = context.scene.display_tools
            row = layout.row(align=True)
            row.alignment = 'LEFT'
            row.operator("view3d.fast_navigate_operator")
            row.operator("view3d.fast_navigate_stop")
            layout.label("Settings :")
            row = layout.row()
            box = row.box()
            box.prop(scene, "OriginalMode")
            box.prop(scene, "FastMode")
            box.prop(scene, "EditActive", "Edit mode")
            box.prop(scene, "Delay")
            box.prop(scene, "DelayTimeGlobal", "Delay time")
            box.alignment = 'LEFT'
            box.prop(scene, "ShowParticles")
            box.prop(scene, "ParticlesPercentageDisplay")





# define scene props
class display_tools_scene_props(PropertyGroup):
    # Init delay variables
    Delay = BoolProperty(
            default=False,
            description="Activate delay return to normal viewport mode"
            )
    DelayTime = IntProperty(
            default=30,
            min=1,
            max=500,
            soft_min=10,
            soft_max=250,
            description="Delay time to return to normal viewport"
                        "mode after move your mouse cursor"
            )
    DelayTimeGlobal = IntProperty(
            default=30,
            min=1,
            max=500,
            soft_min=10,
            soft_max=250,
            description="Delay time to return to normal viewport"
                        "mode after move your mouse cursor"
            )
    # Init variable for fast navigate
    EditActive = BoolProperty(
            default=True,
            description="Activate for fast navigate in edit mode too"
            )

    # Init properties for scene
    FastNavigateStop = BoolProperty(
            name="Fast Navigate Stop",
            description="Stop fast navigate mode",
            default=False
            )
    OriginalMode = EnumProperty(
            items=[('TEXTURED', 'Texture', 'Texture display mode'),
                   ('SOLID', 'Solid', 'Solid display mode')],
            name="Normal",
            default='SOLID'
            )
    BoundingMode = EnumProperty(
            items=[('BOX', 'Box', 'Box shape'),
                   ('SPHERE', 'Sphere', 'Sphere shape'),
                   ('CYLINDER', 'Cylinder', 'Cylinder shape'),
                   ('CONE', 'Cone', 'Cone shape')],
            name="BB Mode"
            )
    FastMode = EnumProperty(
            items=[('WIREFRAME', 'Wireframe', 'Wireframe display'),
                   ('BOUNDBOX', 'Bounding Box', 'Bounding Box display')],
            name="Fast"
            )
    ShowParticles = BoolProperty(
            name="Show Particles",
            description="Show or hide particles on fast navigate mode",
            default=True
            )
    ParticlesPercentageDisplay = IntProperty(
            name="Display",
            description="Display only a percentage of particles",
            default=25,
            min=0,
            max=100,
            soft_min=0,
            soft_max=100,
            subtype='FACTOR'
            )
    InitialParticles = IntProperty(
            name="Count for initial particle setting before enter fast navigate",
            description="Display a percentage value of particles",
            default=100,
            min=0,
            max=100,
            soft_min=0,
            soft_max=100
            )
    Symplify = IntProperty(
            name="Integer",
            description="Enter an integer"
            )

    bpy.types.Scene.UTDisplayDrop = bpy.props.BoolProperty(
        name="Display",
        default=False,
        description="Disply Tools")
    bpy.types.Scene.UTShadingDrop = bpy.props.BoolProperty(
        name="Shading",
        default=False,
        description="Shading Display")
    bpy.types.Scene.UTSceneDrop = bpy.props.BoolProperty(
        name="Scene",
        default=False,
        description="Scene Display")
    bpy.types.Scene.UTModifierDrop = bpy.props.BoolProperty(
        name="Modifiers",
        default=False,
        description="Modifier Display")
    bpy.types.Scene.UTFastnavDrop = bpy.props.BoolProperty(
        name="Fast Nav",
        default=False,
        description="Fast Nav")
# Addons Preferences Update Panel
panels = [
        DisplayToolsPanel
        ]


def update_panel(self, context):
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)
    except:
        print("Display Tools: Updating panel locations has failed")
        pass

    for panel in panels:
        try:
            panel.bl_category = context.user_preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)
        except:
            print("Display Tools: Updating panel locations has failed")
            pass


class DisplayToolsPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    category = StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Display",
            update=update_panel)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "category", text="")


# register the classes and props
def register():
    bpy.utils.register_module(__name__)
    # Register Scene Properties


    bpy.types.Scene.display_tools = bpy.props.PointerProperty(
                                            type=display_tools_scene_props
                                            )
    update_panel(None, bpy.context)


def unregister():
    del bpy.types.Scene.display_tools
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
