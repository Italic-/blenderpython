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
    "name": "Load UI to Backround Images",
    "author": "MKBreuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "location": "View3D > Property Shelf [N] > Backround Images Panel",
    "description": "Add the Load UI Button to the Bottom of the Backround Images Panel",
    "warning": "",
    "wiki_url": "https://github.com/mkbreuer/ToolPlus-Load-UI",
    "tracker_url": "https://github.com/mkbreuer/ToolPlus-Load-UI",
    "category": "User Interface"}


import bpy
from bpy import*
from bpy.props import *
  

def load_ui_to_bg_images(self,context):
    layout = self.layout
    
    col = layout.row(1)
    col.prop(context.user_preferences.filepaths, "use_load_ui", text= "Save & Load UI")
    col.operator("view3d.background_images_fast_import", text= "", icon ="IMAGE_COL")# when installed


def register():

    bpy.types.VIEW3D_PT_background_image.append(load_ui_to_bg_images)    

    #bpy.utils.register_module(__name__)

def unregister():
    
    bpy.types.VIEW3D_PT_background_image.remove(load_ui_to_bg_images)  
    
    #bpy.utils.unregister_module(__name__)
   
if __name__ == "__main__":
    register()  





