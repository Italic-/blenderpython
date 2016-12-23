# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# by meta-androcto #

bl_info = {
    "name": "Add Object Specials",
    "author": "Meta Androcto, ",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "location": "View3D > Add ",
    "description": "Add Object & Camera extras",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6"
    "/Py/Scripts",
    "tracker_url": "",
    "category": "Addon Factory"}


if "bpy" in locals():
    import importlib
    importlib.reload(pixelate_3d)
    importlib.reload(object_add_chain)
    importlib.reload(drop_to_ground)
    importlib.reload(circle_array)
    importlib.reload(crear_cuerda)
    importlib.reload(dupli_spin)
    importlib.reload(unfold_transition)
    importlib.reload(copy2)
    importlib.reload(MakeStruts)
    importlib.reload(Random_Box_Structure)

else:
    from . import pixelate_3d
    from . import object_add_chain
    from . import oscurart_chain_maker
    from . import drop_to_ground
    from . import circle_array
    from . import crear_cuerda
    from . import dupli_spin
    from . import unfold_transition
    from . import copy2
    from . import MakeStruts
    from . import Random_Box_Structure

import bpy

'''
class create_menu(bpy.types.Panel):
    bl_label = 'Add Factory'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.operator('mesh.primitive_chain_add', icon='LINKED')
        layout.operator('mesh.primitive_oscurart_chain_add', icon='LINKED')
        layout.operator('object.pixelate', icon='MESH_GRID')
        layout.operator("object.drop_on_active",
                        text="Drop To Ground", icon='MESH_PLANE')
        layout.operator("objects.circle_array_operator",
                        text="Circle Array", icon='MOD_ARRAY')
        layout.operator("object.procedural_dupli_spin",
                        text="Dupli Splin", icon='MOD_ARRAY')
'''

class INFO_MT_mesh_chain_add(bpy.types.Menu):
    # Define the "mesh objects" menu
    bl_idname = "INFO_MT_mesh_chain"
    bl_label = "Chains"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator('mesh.primitive_chain_add', icon='LINKED')
        layout.operator('mesh.primitive_oscurart_chain_add', icon='LINKED')


class INFO_MT_array_mods_add(bpy.types.Menu):
    # Define the "mesh objects" menu
    bl_idname = "INFO_MT_array_mods"
    bl_label = "Array Mods"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.menu("INFO_MT_mesh_chain", icon="LINKED")
        layout.operator("objects.circle_array_operator",
                        text="Circle Array", icon='MOD_ARRAY')
        layout.operator("object.procedural_dupli_spin",
                        text="Dupli Spin", icon='MOD_ARRAY')
        layout.operator("mesh.copy2",
                        text="Copy To Vert/Edge", icon='MOD_ARRAY')


class INFO_MT_quick_tools_add(bpy.types.Menu):
    # Define the "mesh objects" menu
    bl_idname = "INFO_MT_quick_tools"
    bl_label = "Quick Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("object.drop_on_active",
                        text="Drop To Ground")
        layout.operator('object.pixelate', icon='MESH_GRID')
        layout.operator("ball.rope",
                        text="Wrecking Ball", icon='PHYSICS')
        layout.operator("mesh.generate_struts",
                        text="Struts", icon='GRID')
        layout.operator("object.make_structure",
                        text="Random Boxes", icon='SEQ_SEQUENCER')

# Define "Extras" menu
def menu(self, context):

    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.separator()
    self.layout.menu("INFO_MT_array_mods", icon="MOD_ARRAY")
    self.layout.menu("INFO_MT_quick_tools", icon="MOD_BUILD")


# Addons Preferences


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="----Add Menu Advanced----")
        layout.label(text="Quick Tools:")
        layout.label(text="Drop, Pixelate & Wrecking Ball")
        layout.label(text="Array Mods:")
        layout.label(text="Circle Array, Chains, Vert to Edge, Aggregate")

def register():
    bpy.utils.register_module(__name__)
    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_add.append(menu)
    try:
        bpy.types.VIEW3D_MT_AddMenu.prepend(menu)
    except:
        pass

def unregister():

    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_add.remove(menu)
    try:
        bpy.types.VIEW3D_MT_AddMenu.remove(menu)
    except:
        pass
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
