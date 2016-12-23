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
    'name': 'Bool Tool',
    'author': 'chromoly',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'View3D',
    'description': '',
    'wiki_url': '',
    'category': '3D View',
}


import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(registerinfo)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import registerinfo


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}


class Preferences(
        addongroup.AddonGroupPreferences,
        registerinfo.AddonRegisterInfo,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


classes = [
    Preferences,
]


@Preferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, translation_dict)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = Preferences.get_keymap('Mesh')
        # kmi = km.keymap_items.new('mesh.intersect_cutoff', 'B', 'PRESS',
        #                           shift=True, ctrl=True, alt=True, oskey=True)


@Preferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
