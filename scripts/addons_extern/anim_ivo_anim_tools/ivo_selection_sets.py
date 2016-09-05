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

#
#  Written by Ivo Grigull
#  http://ivogrigull.com
#  http://character-rigger.com
#

import bpy
from bpy.props import *


class bone_selection_set_entry(bpy.types.PropertyGroup):

    @classmethod
    def register(bone_selection_set_entry):

        from bpy.props import PointerProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

        bone_selection_set_entry.bone_name = StringProperty(name="Name", description="", maxlen=40, default="")


class bone_selection_set(bpy.types.PropertyGroup):

    @classmethod
    def register(bone_selection_set):

        from bpy.props import PointerProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

        bone_selection_set.name = StringProperty(name="Name", description="", maxlen=40, default="")
        #~ bone_selection_set.list = CollectionProperty(type=StringProperty, name="entry", description="")
        bone_selection_set.list = CollectionProperty(type=bone_selection_set_entry, name="entries", description="")
        #~ bone_selection_set.list = []


class c_bone_selection_sets(bpy.types.PropertyGroup):

    @classmethod
    def register(c_bone_selection_sets):

        from bpy.props import PointerProperty, StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty

        c_bone_selection_sets.index = IntProperty(name="Index", description="", default=0, min=-1, max=65535)
        c_bone_selection_sets.sets = CollectionProperty(type=bone_selection_set, name="List", description="List of bones for quicker selecting")
        c_bone_selection_sets.use_replace = BoolProperty(name="Replace selection", description="", default=True)

        bpy.types.Object.bone_selection_sets = PointerProperty(type=c_bone_selection_sets, name="Selection Sets", description="List of bones for quicker selecting")
#~ bpy.types.Scene.network_render = PointerProperty(type=NetRenderSettings, name="Network Render", description="Network Render Settings")


def deselect_all_posebones_here():
    ob = bpy.context.active_object
    for n in ob.pose.bones:
        n.bone.select = False


def select_posebone_here(bone):

    ob = bpy.context.active_object

    if type(bone) == bpy.types.PoseBone:
        bone = bone.bone  # get bone instead of posebone
    elif type(bone) == type(str()):  # string type
        try:
            bone = ob.data.bones[bone]
        except:
            return

    #~ deselect_all_posebones()
    bone.select = True
    ob.data.bones.active = bone


class bone_selection_sets_add(bpy.types.Operator):
    '''Add selection set'''
    bl_idname = "object.bone_selection_sets_add"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        sets = ob.bone_selection_sets.sets

        sets.add()
        new_set = sets[len(sets) - 1]
        new_set.name = 'group%d' % len(sets)

        ob.bone_selection_sets.index = len(sets) - 1

        return {'FINISHED'}


class bone_selection_sets_remove(bpy.types.Operator):
    '''Remove selection set'''
    bl_idname = "object.bone_selection_sets_remove"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        sets = ob.bone_selection_sets.sets

        sets.remove(index)

        if index > len(sets) - 1:
            index -= 1

        return {'FINISHED'}


class bone_selection_set_assign(bpy.types.Operator):
    '''Assign bones to active selection set'''
    bl_idname = "object.bone_selection_set_assign"  # this is important since its how bpy.ops.export.some_data is constructed
    bl_label = "Assign"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:
                set.list.add()
                entry = set.list[len(set.list) - 1]
                entry.bone_name = n.name

        return {'FINISHED'}


class bone_selection_set_remove(bpy.types.Operator):
    '''Remove bones from active selection set'''
    bl_idname = "object.bone_selection_set_remove"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):

        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        for n in ob.data.bones:
            if n.select:

                name = n.name

                remove_list = []
                for i in range(len(set.list)):
                    if set.list[i].bone_name == name:
                        #~ remove_list.append(i)
                        set.list.remove(i)
                        break

                #~ for i in range( len(remove_list) ):
                    #~ set.list.remove(i)

                #~ set.list.add()
                #~ entry = set.list[ len(set.list)-1 ]
                #~ entry.bone_name = n.name

        return {'FINISHED'}


class bone_selection_set_select(bpy.types.Operator):
    '''Select bones from active selection set'''
    bl_idname = "object.bone_selection_set_select"
    bl_label = "Select"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        ob = context.active_object
        index = ob.bone_selection_sets.index
        set = ob.bone_selection_sets.sets[index]

        if ob.bone_selection_sets.use_replace:
            deselect_all_posebones_here()

        for n in set.list:
            try:
                select_posebone_here(ob.data.bones[n.bone_name])
            except:
                pass

        context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


class deselect_all_bones(bpy.types.Operator):
    '''Deselect all bones'''
    bl_idname = "object.deselect_all_bones"
    bl_label = "Deselect all bones"

    @classmethod
    def poll(cls, context):
        return context.object != None

    def execute(self, context):
        ob = context.active_object

        if ob.type == 'ARMATURE':
            for n in ob.data.bones:
                n.select = False

            ob.data.bones.active = None
            context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}


class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Animation'


class VIEW3D_PT_tools_bone_selection_sets(View3DPanel, bpy.types.Panel):
    bl_context = "posemode"
    bl_label = "Bone selection sets"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #~ row = layout.row()
        #~ row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.template_list(obj.bone_selection_sets, "sets", obj.bone_selection_sets, "index", rows=5)

        col = row.column()
        sub = col.column(align=True)
        sub.operator("object.bone_selection_sets_add", icon='ZOOMIN', text="")
        sub.operator("object.bone_selection_sets_remove", icon='ZOOMOUT', text="")

        row = layout.row()
        #~ if len(obj.bone_selection_sets.sets) <= 0:
        #~ obj.bone_selection_sets.sets.add()
        #~ obj.bone_selection_sets.sets[ len(obj.bone_selection_sets.sets)-1 ].name = "group1"
        try:
            row.prop(obj.bone_selection_sets.sets[obj.bone_selection_sets.index], "name")
        except:
            pass

        row = layout.row()
        #~ col = row.column()

        row.prop(obj.bone_selection_sets, "use_replace")
        row.operator('object.deselect_all_bones')

        row = layout.row()
        row.operator('object.bone_selection_set_assign')
        row.operator('object.bone_selection_set_remove')

        row = layout.row()
        row.operator('object.bone_selection_set_select')


def register():
    pass


def unregister():
    pass


if __name__ == "__main__":
    register()
