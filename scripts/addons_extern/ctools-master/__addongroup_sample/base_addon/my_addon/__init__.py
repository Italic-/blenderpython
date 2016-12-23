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
    'name': 'My Addon',
    'version': (0, 1),
    'description': 'Addon group test',
    'category': '3D View',
}


if 'bpy' in locals():
    import importlib
    importlib.reload(addongroup)
    MyAddonPreferences.reload_sub_modules()
else:
    from . import addongroup

import bpy


class MyAddonPreferences(
        addongroup.AddonGroupPreferences,
        bpy.types.AddonPreferences if '.' not in __name__ else
        bpy.types.PropertyGroup):
    bl_idname = __name__

    sub_modules = None

    prop = bpy.props.IntProperty(name='MyAddon Prop')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'prop')

        layout.separator()
        super().draw(context)

    @classmethod
    def register(cls):
        super().register()

    @classmethod
    def unregister(cls):
        super().unregister()


classes = [
    MyAddonPreferences,
]


@MyAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = MyAddonPreferences.get_instance()
    value = prefs.prop  # value of bpy.props.IntProperty(name='MyAddon Prop')


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
