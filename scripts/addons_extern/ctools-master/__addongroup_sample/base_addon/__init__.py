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
    'name': 'Base Addon',
    'author': 'Anonymous',
    'version': (1, 0),
    'blender': (2, 78, 0),
    'location': 'View3D > Tool Shelf',
    'description': 'Addon group test',
    'warning': '',
    'wiki_url': '',
    'category': '3D View',
    }

if 'bpy' in locals():
    import importlib
    importlib.reload(addongroup)
    BaseAddonPreferences.reload_sub_modules()
else:
    from . import addongroup

import bpy


class BaseAddonPreferences(
        addongroup.AddonGroupPreferences, bpy.types.AddonPreferences):

    bl_idname = __name__

    sub_modules = [
        'my_addon',
        'space_view3d_other_addon',
        '_hidden_addon'
    ]


classes = [
    BaseAddonPreferences,
]


@BaseAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
