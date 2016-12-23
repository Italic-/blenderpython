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

bl_info = {
    "name": "Procedural Dupli Spin",
    "description": "This script create a procedural dupli spin using the array modifier.",
    "author": "Omar ahmed",
    "version": (1, 0),
    "blender": (2, 72, 0),
    "location": "View3D > Tools > Add",
    "warning": "addon is beta",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"
                "Scripts/My_Script",
    "category": "Mesh"}


import bpy
import bmesh


class procedural_dupli_spin(bpy.types.Operator):
    bl_idname = "object.procedural_dupli_spin"
    bl_label = "Procedural Dupli Spin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # enableing the auto execute

        bpy.context.user_preferences.system.use_scripts_auto_execute = True

        # saving the orignal object name
        object_name = bpy.context.active_object.name
        object_new_name = "Spin_" + object_name
        # separating objects If needed
        obj = bpy.context.active_object
        if bpy.context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(obj.data)
            selected_vertex = [v.index for v in bm.verts if v.select]
        else:
            selected_vertex = [v.index for v in obj.data.vertices if v.select]

        selected_vertex = len(selected_vertex)
        total_vertex = (len(obj.data.vertices))
        # If we need separation
        if total_vertex - selected_vertex > 0:
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.data.objects[object_name].select = False
            for obj in bpy.context.scene.objects:
                obj.select = (obj == bpy.context.scene.objects.active)
            active_object = bpy.context.active_object
            active_object.name = object_new_name
        # If we don't need separation
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            active_object = bpy.context.active_object
            active_object.name = object_new_name

        # Apply rotation and scale
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        # set the origin of the object to the 3d cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # add the main empty(the one which is going to be rotated with the driver)
        bpy.ops.object.empty_add(type='PLAIN_AXES')

        # rename the main empty
        active_object = bpy.context.active_object
        active_object.name = "Object offset_main"

        # add the array offset object_child
        bpy.ops.object.empty_add(type='PLAIN_AXES')

        # change the name of the array offset object_child
        active_object = bpy.context.active_object
        active_object.name = "Object offset_child"

        # add the array offset object_parent
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        ctx = bpy.context.copy()
                        ctx['area'] = area
                        ctx['region'] = region
                        bpy.ops.object.empty_add(ctx, type='PLAIN_AXES', view_align=True)

        # change the name of the array offset_parent
        active_object = bpy.context.active_object
        active_object.name = "Object offset_parent"

        # add the copy rotation constraint

        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["Object offset_main"]
        bpy.context.object.constraints["Copy Rotation"].use_x = False
        bpy.context.object.constraints["Copy Rotation"].use_y = False
        bpy.context.object.constraints["Copy Rotation"].use_z = True
        bpy.context.object.constraints["Copy Rotation"].owner_space = 'LOCAL'

        # make the parent relation

        child_object = bpy.data.objects["Object offset_child"]
        parent_object = bpy.data.objects["Object offset_parent"]

        bpy.ops.object.select_all(action='DESELECT')

        child_object.select = True
        parent_object.select = True

        bpy.context.scene.objects.active = parent_object

        bpy.ops.object.parent_set()

        # select the spin object
        bpy.context.scene.objects.active = bpy.data.objects[object_new_name]
        for obj in bpy.context.scene.objects:
            obj.select = (obj == bpy.context.scene.objects.active)

        # add the array modifier
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].use_relative_offset = False
        bpy.context.object.modifiers["Array"].use_object_offset = True
        bpy.context.object.modifiers["Array"].offset_object = bpy.data.objects["Object offset_child"]

        # add the array count custom property
        active_object = bpy.context.active_object
        active_object["Array count"] = 6
        active_object["_RNA_UI"] = {"Array count": {"min": 2}}

        # add the driver to the array count
        myDriver = bpy.context.object.driver_add('modifiers["Array"].count')
        myDriver.driver.expression = "Array_count"
        newVar = myDriver.driver.variables.new()
        newVar.name = "Array_count"
        newVar.type = 'SINGLE_PROP'
        newVar.targets[0].id = bpy.data.objects[object_new_name]
        newVar.targets[0].data_path = '["Array count"]'

        # select the main empty
        bpy.context.scene.objects.active = bpy.data.objects["Object offset_main"]
        for obj in bpy.context.scene.objects:
            obj.select = (obj == bpy.context.scene.objects.active)

        # add the driver to the main empty

        myDriver = bpy.context.object.driver_add('rotation_euler', 2)
        myDriver.driver.expression = "360/Array * pi/180"
        newVar = myDriver.driver.variables.new()
        newVar.name = "Array"
        newVar.type = 'SINGLE_PROP'
        newVar.targets[0].id = bpy.data.objects[object_new_name]
        newVar.targets[0].data_path = 'modifiers["Array"].count'

        # select the spin object
        bpy.context.scene.objects.active = bpy.data.objects[object_new_name]
        for obj in bpy.context.scene.objects:
            obj.select = (obj == bpy.context.scene.objects.active)

        # cleaning the scene

        bpy.data.objects["Object offset_main"].hide = True
        bpy.data.objects["Object offset_child"].hide = True

        return {'FINISHED'}

# Creating Panel

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(procedural_dupli_spin)


def unregister():
    bpy.utils.unregister_class(procedural_dupli_spin)


if __name__ == "__main__":
    register()
