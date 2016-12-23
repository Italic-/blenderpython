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
    from . import registerinfo

import bpy


class MyAddonPreferences(
        addongroup.AddonGroupPreferences,
        registerinfo.AddonRegisterInfo,
        bpy.types.AddonPreferences if '.' not in __name__ else
        bpy.types.PropertyGroup):
    bl_idname = __name__

    sub_modules = []

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


@MyAddonPreferences.register_addon
def register():
    MyAddonPreferences.register_module()

    km = MyAddonPreferences.get_keymap('Screen Editing')
    if km:
        km.keymap_items.new('wm.splash', 'ZERO', 'PRESS', shift=True,
                            ctrl=True, alt=True, oskey=True)


@MyAddonPreferences.unregister_addon
def unregister():
    MyAddonPreferences.unregister_module()
