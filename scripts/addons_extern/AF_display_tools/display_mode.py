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

class View3D_AF_Display_DrawWire(bpy.types.Operator):
    """Draw Type Wire"""
    bl_idname = "af_ops.draw_wire"
    bl_label = "Draw Type Wire"

    def execute(self, context):
        bpy.context.object.draw_type = 'WIRE'       
        return {'FINISHED'}


class View3D_AF_Display_DrawSolid(bpy.types.Operator):
    """Draw Type Solid"""
    bl_idname = "af_ops.draw_solid"
    bl_label = "Draw Type Solid"

    def execute(self, context):
        bpy.context.object.draw_type = 'SOLID'       
        return {'FINISHED'}


class View3D_AF_Wire_All(bpy.types.Operator):
    """Wire on all objects in the scene"""
    bl_idname = "af_ops.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False            
            else:
                obj.show_all_edges = True
                obj.show_wire = True
                             
        return {'FINISHED'} 

class View3D_AF_Wire_On(bpy.types.Operator):
    '''Wire on'''
    bl_idname = "af_ops.wire_on"
    bl_label = "Wire on"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
         
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = True
                obj.show_all_edges = True
                
        else:
            for obj in selection:
                obj.show_wire = True
                obj.show_all_edges = True 
        return {'FINISHED'}


class View3D_AF_Wire_Off(bpy.types.Operator):
    '''Wire off'''
    bl_idname = "af_ops.wire_off"
    bl_label = "Wire off"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        selection = bpy.context.selected_objects  
        
        if not(selection): 
            for obj in bpy.data.objects:
                obj.show_wire = False
                obj.show_all_edges = False
                
        else:
            for obj in selection:
                obj.show_wire = False
                obj.show_all_edges = False   

        return {'FINISHED'}


class VIEW3D_OT_Display_Wire_All1(Operator):
    """Display Wire on All Objects"""
    bl_label = "Wire on All Objects"
    bl_idname = "view3d.display_wire_all1"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False
            else:
                obj.show_all_edges = True
                obj.show_wire = True

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



# register the classes and props
def register():
    bpy.utils.register_module(__name__)
    # Register Scene Properties


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
