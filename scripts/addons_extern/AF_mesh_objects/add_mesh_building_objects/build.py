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
# Contributed to by
# SAYproductions, meta-androcto, jambay, brikbot#

bl_info = {
    "name": "Building Objects",
    "author": "Multiple Authors",
    "version": (0, 2),
    "blender": (2, 71, 0),
    "location": "View3D > Add > Mesh > Cad Objects",
    "description": "Add building object types",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://developer.blender.org/T32711",
    "category": "Add Mesh"}


if "bpy" in locals():
    import importlib
    importlib.reload(add_mesh_balcony)
    importlib.reload(add_mesh_sove)
    importlib.reload(Wallfactory)
    importlib.reload(stairbuilder)
    importlib.reload(Blocks)
    importlib.reload(general)
    importlib.reload(post)
    importlib.reload(rail)
    importlib.reload(retainer)
    imprtlib.reload(stringer)
    importlib.reload(tread)

else:
    from . import add_mesh_balcony
    from . import add_mesh_sove
    from . import Wallfactory
    from . import stairbuilder
    from . import Blocks
    from . import general
    from . import post
    from . import rail
    from . import retainer
    from . import stringer
    from . import tread

import bpy


class INFO_MT_mesh_objects_add(bpy.types.Menu):
    # Define the "mesh objects" menu
    bl_idname = "INFO_MT_cad_objects_add"
    bl_label = "Building Objects"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("INFO_MT_mesh_beambuilder_add",
                    text="Beam Builder")
        layout.operator("mesh.add_say3d_balcony",
                        text="Balcony")
        layout.operator("mesh.add_say3d_sove",
                        text="Sove")
        layout.operator("mesh.wall_add",
                        text="Wall Factory")
        layout.operator("mesh.stairs",
                        text="Stair Builder")


# Register all operators and panels

# Define "Extras" menu
def menu(self, context):
    self.layout.menu("INFO_MT_cad_objects_add", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)

    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)

    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
