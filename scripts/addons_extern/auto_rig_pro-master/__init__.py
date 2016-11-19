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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "Auto-Rig Pro",
    "author": "Artell",
    "version": (2, 7),
    "blender": (2, 7, 5),
    "location": "3D View > Properties> Auto-Rig Pro",
    "description": "Automatic rig creation based on reference bones. Includes IK-FK snap and Proxy picker addons.",
    "tracker_url": "https://cgcookiemarkets.com/all-products/artell-auto-rig/?ref=46",    
    "category": "Animation"} 


if "bpy" in locals():
    import importlib
    if "snap_ikfk" in locals():
        importlib.reload(snap_ikfk)
    if "auto_rig" in locals():
        importlib.reload(auto_rig)


import bpy
from bpy.app.handlers import persistent
#import script files
from . import snap_ikfk
from . import auto_rig




def register():
    #register classes
    bpy.utils.register_module(__name__)
    #register properties and misc
    auto_rig.register()

  

def unregister():
    #unregister classes
    bpy.utils.unregister_module(__name__)
    #unregister properties and misc
    auto_rig.unregister()

   


if __name__ == "__main__":
    register()