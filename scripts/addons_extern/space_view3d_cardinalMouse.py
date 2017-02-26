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
    "name": "CardinalMouse",
    "author": "Sean Olson",
    "version": (1, 0),
    "blender": (2, 71, 0),
    "location": "Hotkeys",
    "description": "Add shortcuts to mouse to move camera to orthogonal directions",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/3D_interaction/CardinalMouse",
    "tracker_url": "",
    "category": "3D View"}

import bpy
default_keybind = 'EVT_TWEAK_M'

def register():
        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', default_keybind, 'NORTH', False, False, False, True, False)
        kmi.properties.type='BOTTOM'

        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', default_keybind, 'SOUTH', False, False, False, True, False)
        kmi.properties.type='TOP'
        
        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', default_keybind, 'EAST', False, False, False, True, False)
        kmi.properties.type='LEFT'

        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', default_keybind, 'WEST', False, False, False, True, False)
        kmi.properties.type='RIGHT'

        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', 'MIDDLEMOUSE', 'CLICK', False, False, False, True, False)
        kmi.properties.type='FRONT'

        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        kmi=km.keymap_items.new('view3d.viewnumpad', 'MIDDLEMOUSE', 'DOUBLE_CLICK', False, False, False, True, False)
        kmi.properties.type='BACK'
def unregister():
        #remove keybinds
        km = bpy.context.window_manager.keyconfigs.active.keymaps['3D View']
        for kmi in km.keymap_items:
                if kmi.idname == 'view3d.viewnumpad':
                        if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==True and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                                km.keymap_items.remove(kmi)
                               




