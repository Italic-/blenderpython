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
    "name": "Display Tools",
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

"""
Additional links:
    Author Site: http://www.jordiart.com
"""

import bpy
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        AddonPreferences,
        )
from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        StringProperty,
        )


# define base dummy class for inheritance
class BasePollCheck:
    @classmethod
    def poll(cls, context):
        return True


# Fast Navigate toggle function
def trigger_fast_navigate(trigger):
    scene = bpy.context.scene.display_tools
    scene.FastNavigateStop = False

    trigger = not trigger


# Control how to display particles during fast navigate
def display_particles(mode):
    scene = bpy.context.scene.display_tools

    if mode is True:
        for particles in bpy.data.particles:
            if particles.type == 'EMITTER':
                particles.draw_method = 'DOT'
                particles.draw_percentage = 100
            else:
                particles.draw_method = 'RENDER'
                particles.draw_percentage = 100
    else:
        for particles in bpy.data.particles:
            if particles.type == 'EMITTER':
                particles.draw_method = 'DOT'
                particles.draw_percentage = scene.ParticlesPercentageDisplay
            else:
                particles.draw_method = 'RENDER'
                particles.draw_percentage = scene.ParticlesPercentageDisplay


# Fast Navigate operator
class FastNavigate(Operator):
    bl_idname = "view3d.fast_navigate_operator"
    bl_label = "Fast Navigate"
    bl_description = "Operator that runs Fast navigate in modal mode"

    trigger = BoolProperty(default=False)
    mode = BoolProperty(default=False)

    def modal(self, context, event):
        scene = context.scene.display_tools

        if scene.FastNavigateStop is True:
            self.cancel(context)
            return {'FINISHED'}

        if scene.EditActive is True:
            self.fast_navigate_stuff(context, event)
            return {'PASS_THROUGH'}
        else:
            obj = context.active_object
            if obj:
                if obj.mode != 'EDIT':
                    self.fast_navigate_stuff(context, event)
                    return {'PASS_THROUGH'}
                else:
                    return {'PASS_THROUGH'}
            else:
                self.fast_navigate_stuff(context, event)
                return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        trigger_fast_navigate(self.trigger)
        scene = context.scene.display_tools
        scene.DelayTime = scene.DelayTimeGlobal
        return {'RUNNING_MODAL'}

    # Do repetitive fast navigate related stuff
    def fast_navigate_stuff(self, context, event):
        scene = context.scene.display_tools
        view = context.space_data

        if context.area.type != 'VIEW_3D':
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'ESC' or event.type == 'RET' or event.type == 'SPACE':
            self.cancel(context)
            return {'CANCELLED'}

        if scene.FastNavigateStop is True:
            self.cancel(context)
            return {'CANCELLED'}

        # fast navigate while orbit/panning
        if event.type == 'MIDDLEMOUSE':
            if scene.Delay is True:
                if scene.DelayTime < scene.DelayTimeGlobal:
                    scene.DelayTime += 1
            view.viewport_shade = scene.FastMode
            self.mode = False

        # fast navigate while transform operations
        if event.type == 'G' or event.type == 'R' or event.type == 'S':
            if scene.Delay is True:
                if scene.DelayTime < scene.DelayTimeGlobal:
                    scene.DelayTime += 1
            view.viewport_shade = scene.FastMode
            self.mode = False

        # fast navigate while menu popups or duplicates
        if event.type == 'W' or event.type == 'D' or event.type == 'L'\
          or event.type == 'U' or event.type == 'I' or event.type == 'M'\
          or event.type == 'A' or event.type == 'B':
            if scene.Delay is True:
                if scene.DelayTime < scene.DelayTimeGlobal:
                    scene.DelayTime += 1
            view.viewport_shade = scene.FastMode
            self.mode = False

        # fast navigate while numpad navigation
        if (event.type == 'NUMPAD_PERIOD' or event.type == 'NUMPAD_1' or
           event.type == 'NUMPAD_2' or event.type == 'NUMPAD_3' or
           event.type == 'NUMPAD_4' or event.type == 'NUMPAD_5' or
           event.type == 'NUMPAD_6' or event.type == 'NUMPAD_7' or
           event.type == 'NUMPAD_8' or event.type == 'NUMPAD_9'):

            if scene.Delay is True:
                if scene.DelayTime < scene.DelayTimeGlobal:
                    scene.DelayTime += 1
            view.viewport_shade = scene.FastMode
            self.mode = False

        # fast navigate while zooming with mousewheel too
        if event.type == 'WHEELUPMOUSE' or event.type == 'WHEELDOWNMOUSE':
            scene.DelayTime = scene.DelayTimeGlobal
            view.viewport_shade = scene.FastMode
            self.mode = False

        if event.type == 'MOUSEMOVE':
            if scene.Delay is True:
                if scene.DelayTime == 0:
                    scene.DelayTime = scene.DelayTimeGlobal
                    view.viewport_shade = scene.OriginalMode
                    self.mode = True
            else:
                view.viewport_shade = scene.OriginalMode
                self.mode = True

        if scene.Delay is True:
            scene.DelayTime -= 1
            if scene.DelayTime == 0:
                scene.DelayTime = scene.DelayTimeGlobal
                view.viewport_shade = scene.OriginalMode
                self.mode = True

        if scene.ShowParticles is False:
            for particles in bpy.data.particles:
                if particles.type == 'EMITTER':
                    particles.draw_method = 'NONE'
                else:
                    particles.draw_method = 'NONE'
        else:
            display_particles(self.mode)

    def cancel(self, context):
        scene = context.scene.display_tools
        for particles in bpy.data.particles:
            particles.draw_percentage = scene.InitialParticles


# Fast Navigate Stop
def fast_navigate_stop(context):
    scene = context.scene.display_tools
    scene.FastNavigateStop = True


# Fast Navigate Stop Operator
class FastNavigateStop(Operator):
    bl_idname = "view3d.fast_navigate_stop"
    bl_label = "Stop"
    bl_description = "Stop Fast Navigate Operator"

    def execute(self, context):
        fast_navigate_stop(context)
        return {'FINISHED'}


# Change draw type
class DisplayDrawChange(Operator, BasePollCheck):
    bl_idname = "view3d.display_draw_change"
    bl_label = "Draw Type"
    bl_description = "Change Display objects mode"

    drawing = EnumProperty(
            items=[('TEXTURED', 'Texture', 'Texture display mode'),
                   ('SOLID', 'Solid', 'Solid display mode'),
                   ('WIRE', 'Wire', 'Wire display mode'),
                   ('BOUNDS', 'Bounds', 'Bounds display mode'),
                   ],
            name="Draw Type",
            default='SOLID'
            )

    def execute(self, context):
        try:
            view = context.space_data
            view.viewport_shade = 'TEXTURED'
            context.scene.game_settings.material_mode = 'GLSL'
            selection = context.selected_objects

            if not selection:
                for obj in bpy.data.objects:
                    obj.draw_type = self.drawing
            else:
                for obj in selection:
                    obj.draw_type = self.drawing
        except:
            self.report({'ERROR'}, "Setting Draw Type could not be applied")
            return {'CANCELLED'}

        return {'FINISHED'}


# Shade smooth/flat
class DisplayShadeSmoothFlat(Operator, BasePollCheck):
    bl_idname = "view3d.display_shade_smooth_flat"
    bl_label = "Smooth/Flat"
    bl_description = "Toggle shade smooth/flat shading"

    smoothing = BoolProperty(default=True)

    def execute(self, context):
        try:
            selection = bpy.context.selected_objects
            if not selection:
                for obj in bpy.data.objects:
                    bpy.ops.object.select_all(action='TOGGLE')
                    if self.smoothing:
                        bpy.ops.object.shade_smooth()
                    else:
                        bpy.ops.object.shade_flat()
                    bpy.ops.object.select_all(action='TOGGLE')
            else:
                obj = context.active_object
                if obj.mode == 'OBJECT':
                    for obj in selection:
                        if self.smoothing:
                            bpy.ops.object.shade_smooth()
                        else:
                            bpy.ops.object.shade_flat()
                else:
                    if self.smoothing:
                        bpy.ops.mesh.faces_shade_smooth()
                    else:
                        bpy.ops.mesh.faces_shade_flat()
        except:
            self.report({'ERROR'}, "Setting Smooth/Flat shading failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Shadeless switch
class DisplayShadelesSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_shadeless_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide shadeless material"

    shades = BoolProperty(default=False)

    def execute(self, context):
        try:
            selection = bpy.context.selected_objects

            if not(selection):
                for obj in bpy.data.materials:
                    obj.use_shadeless = self.shades
            else:
                for sel in selection:
                    if sel.type == 'MESH':
                        materials = sel.data.materials
                        for mat in materials:
                            mat.use_shadeless = self.shades
        except:
            self.report({'ERROR'}, "Display/Hide shadeless material failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Wireframe switch
class DisplayWireframeSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_wire_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide wireframe overlay"

    wires = BoolProperty(default=False)

    def execute(self, context):
        try:
            selection = bpy.context.selected_objects

            if not(selection):
                for obj in bpy.data.objects:
                    obj.show_wire = self.wires
                    obj.show_all_edges = self.wires
            else:
                for obj in selection:
                    obj.show_wire = self.wires
                    obj.show_all_edges = self.wires
        except:
            self.report({'ERROR'}, "Display/Hide wireframe overlay failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Bounds switch
class DisplayBoundsSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_bounds_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide Bounding box overlay"

    bounds = BoolProperty(default=False)

    def execute(self, context):
        try:
            scene = context.scene.display_tools
            selection = context.selected_objects

            if not selection:
                for obj in bpy.data.objects:
                    obj.show_bounds = self.bounds
                    if self.bounds:
                        obj.draw_bounds_type = scene.BoundingMode
            else:
                for obj in selection:
                    obj.show_bounds = self.bounds
                    if self.bounds:
                        obj.draw_bounds_type = scene.BoundingMode
        except:
            self.report({'ERROR'}, "Display/Hide Bounding box overlay failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Double Sided switch
class DisplayDoubleSidedSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_double_sided_switch"
    bl_label = "On/Off"
    bl_description = "Turn on/off face double shaded mode"

    double_side = BoolProperty(default=False)

    def execute(self, context):
        try:
            selection = bpy.context.selected_objects

            if not selection:
                for mesh in bpy.data.meshes:
                    mesh.show_double_sided = self.double_side
            else:
                for sel in selection:
                    if sel.type == 'MESH':
                        mesh = sel.data
                        mesh.show_double_sided = self.double_side
        except:
            self.report({'ERROR'}, "Turn on/off face double shaded mode failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# XRay switch
class DisplayXRayOn(Operator, BasePollCheck):
    bl_idname = "view3d.display_x_ray_switch"
    bl_label = "On"
    bl_description = "X-Ray display on/off"

    xrays = BoolProperty(default=False)

    def execute(self, context):
        try:
            selection = context.selected_objects

            if not selection:
                for obj in bpy.data.objects:
                    obj.show_x_ray = self.xrays
            else:
                for obj in selection:
                    obj.show_x_ray = self.xrays
        except:
            self.report({'ERROR'}, "Turn on/off X-ray mode failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Set Render Settings
def set_render_settings(context):
    scene = context.scene
    render = scene.render
    render.simplify_subdivision = 0
    render.simplify_shadow_samples = 0
    render.simplify_child_particles = 0
    render.simplify_ao_sss = 0


class DisplaySimplify(Operator, BasePollCheck):
    bl_idname = "view3d.display_simplify"
    bl_label = "Reset"
    bl_description = "Display scene simplified"

    Mode = EnumProperty(
        items=[('WIREFRAME', 'Wireframe', ''),
                 ('BOUNDBOX', 'Bounding Box', '')],
        name="Mode"
        )
    ShowParticles = BoolProperty(
        name="ShowParticles",
        description="Show or hide particles on fast navigate mode",
        default=True
        )
    ParticlesPercentageDisplay = IntProperty(
        name="Display",
        description="Display a percentage value of particles",
        default=25,
        min=0,
        max=100,
        soft_min=0,
        soft_max=100,
        subtype='FACTOR'
        )

    def execute(self, context):
        set_render_settings(context)
        return {'FINISHED'}


# Display Modifiers Render Switch
class DisplayModifiersRenderSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_render_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide modifiers on render"

    mod_render = BoolProperty(default=True)

    def execute(self, context):
        try:
            if self.mod_render:
                scene = context.scene.display_tools
                scene.Simplify = 1

            selection = context.selected_objects

            if not selection:
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        mod.show_render = self.mod_render
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        mod.show_render = self.mod_render
        except:
            self.report({'ERROR'}, "Display/Hide all modifiers for render failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Display Modifiers Viewport switch
class DisplayModifiersViewportSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_viewport_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide modifiers in the viewport"

    mod_switch = BoolProperty(default=True)

    def execute(self, context):
        try:
            selection = context.selected_objects

            if not(selection):
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        mod.show_viewport = self.mod_switch
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        mod.show_viewport = self.mod_switch
        except:
            self.report({'ERROR'}, "Display/Hide modifiers in the viewport failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Display Modifiers Edit Switch
class DisplayModifiersEditSwitch(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_edit_switch"
    bl_label = "On/Off"
    bl_description = "Display/Hide modifiers during edit mode"

    mod_edit = BoolProperty(default=True)

    def execute(self, context):
        try:
            selection = context.selected_objects

            if not(selection):
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        mod.show_in_editmode = self.mod_edit
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        mod.show_in_editmode = self.mod_edit
        except:
            self.report({'ERROR'}, "Display/Hide all modifiers failed")
            return {'CANCELLED'}

        return {'FINISHED'}


class DisplayModifiersCageSet(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_cage_set"
    bl_label = "On/Off"
    bl_description = "Display modifiers editing cage during edit mode"

    set_cage = BoolProperty(default=True)

    def execute(self, context):
        selection = context.selected_objects
        try:
            if not selection:
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        mod.show_on_cage = self.set_cage
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        mod.show_on_cage = self.set_cage
        except:
            self.report({'ERROR'}, "Setting Editing Cage all modifiers failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Display Modifiers Expand
class DisplayModifiersExpandCollapse(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_expand_collapse"
    bl_label = "Expand/Collapse"
    bl_description = "Expand/Collapse all modifiers on modifier stack"

    expands = BoolProperty(default=True)

    def execute(self, context):
        selection = context.selected_objects
        try:
            if not selection:
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        mod.show_expanded = self.expands
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        mod.show_expanded = self.expands

            # update Properties
            for area in context.screen.areas:
                if area.type in ('PROPERTIES'):
                    area.tag_redraw()
        except:
            self.report({'ERROR'}, "Expand/Collapse all modifiers failed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Apply modifiers
class DisplayModifiersApply(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_apply"
    bl_label = "Apply All"
    bl_description = "Apply modifiers"

    def execute(self, context):
        selection = context.selected_objects
        try:
            if not selection:
                bpy.ops.object.select_all(action='TOGGLE')
                bpy.ops.object.convert(target='MESH', keep_original=False)
                bpy.ops.object.select_all(action='TOGGLE')
            else:
                for mesh in selection:
                    if mesh.type == "MESH":
                        bpy.ops.object.convert(target='MESH', keep_original=False)
        except:
            self.report({'ERROR'}, "Apply modifiers could not be executed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Delete modifiers
class DisplayModifiersDelete(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_delete"
    bl_label = "Delete All"
    bl_description = "Delete modifiers"

    def execute(self, context):
        selection = context.selected_objects
        try:
            if not(selection):
                for obj in bpy.data.objects:
                    for mod in obj.modifiers:
                        bpy.context.scene.objects.active = obj
                        bpy.ops.object.modifier_remove(modifier=mod.name)
            else:
                for obj in selection:
                    for mod in obj.modifiers:
                        bpy.context.scene.objects.active = obj
                        bpy.ops.object.modifier_remove(modifier=mod.name)
        except:
            self.report({'ERROR'}, "Delete modifiers could not be executed")
            return {'CANCELLED'}

        return {'FINISHED'}


# Put dummy modifier for boost subsurf
def modifiers_set_dummy(context):
    selection = context.selected_objects

    if not(selection):
        for obj in bpy.data.objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
            value = 0
            for mod in obj.modifiers:
                if mod != 0:
                    if mod.type == 'SIMPLE_DEFORM':
                        value = value + 1
                        mod.factor = 0
                    if value > 1:
                        bpy.ops.object.modifier_remove(modifier="SimpleDeform")
    else:
        for obj in selection:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
            value = 0
            for mod in obj.modifiers:
                if mod.type == 'SIMPLE_DEFORM':
                    value = value + 1
                    mod.factor = 0
                if value > 1:
                    bpy.ops.object.modifier_remove(modifier="SimpleDeform")


# Delete dummy modifier
def modifiers_delete_dummy(context):
    selection = context.selected_objects

    if not(selection):
        for obj in bpy.data.objects:
            bpy.context.scene.objects.active = obj
            for mod in obj.modifiers:
                if mod.type == 'SIMPLE_DEFORM':
                    bpy.ops.object.modifier_remove(modifier="SimpleDeform")
                    bpy.ops.object.modifier_remove(modifier="SimpleDeform.001")
    else:
        for obj in selection:
            bpy.context.scene.objects.active = obj
            for mod in obj.modifiers:
                if mod.type == 'SIMPLE_DEFORM':
                    bpy.ops.object.modifier_remove(modifier="SimpleDeform")
                    bpy.ops.object.modifier_remove(modifier="SimpleDeform.001")


class DisplayAddDummy(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_set_dummy"
    bl_label = "Put Dummy"
    bl_description = ("Add a dummy simple deform modifier to boost "
                     "subsurf modifier viewport performance")

    def execute(self, context):
        modifiers_set_dummy(context)
        return {'FINISHED'}


class DisplayDeleteDummy(Operator, BasePollCheck):
    bl_idname = "view3d.display_modifiers_delete_dummy"
    bl_label = "Delete Dummy"
    bl_description = ("Delete a dummy simple deform modifier to boost "
                      "subsurf modifier viewport performance")

    def execute(self, context):
        modifiers_delete_dummy(context)
        return {'FINISHED'}


class ModifiersSubsurfLevel_Set(Operator, BasePollCheck):
    bl_idname = "view3d.modifiers_subsurf_level_set"
    bl_label = "Set Subsurf level"
    bl_description = "Change subsurf modifier level"

    level = IntProperty(
        name="Subsurf Level",
        description="Change subsurf modifier level",
        default=1,
        min=0,
        max=10,
        soft_min=0,
        soft_max=6
        )

    def execute(self, context):
        selection = context.selected_objects
        try:
            if not selection:
                for obj in bpy.data.objects:
                    context.scene.objects.active = obj
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    value = 0
                    for mod in obj.modifiers:
                        if mod.type == 'SUBSURF':
                            value = value + 1
                            mod.levels = self.level
                        if value > 1:
                            bpy.ops.object.modifier_remove(modifier="Subsurf")
            else:
                for obj in selection:
                    bpy.ops.object.subdivision_set(level=self.level, relative=False)
                    for mod in obj.modifiers:
                        if mod.type == 'SUBSURF':
                            mod.levels = self.level
        except:
            self.report({'ERROR'}, "Setting the Subsurf level could not be applied")
            return {'CANCELLED'}

        return {'FINISHED'}




# register the classes and props
def register():
    bpy.utils.register_module(__name__)
    # Register Scene Properties



def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
