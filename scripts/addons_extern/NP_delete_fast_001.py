
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



# DESCRIPTION
# 
# Deletes objects without confirmation pop-up.
#
# It's main advantage is speed and behaviour standard. Intended for production workflows that include various applications along with blender. Also intended for design processes heavily burdened with decision-making through multiple add and delete operations. Many thanks to lukas_t who introduced this simple function.
# 
# INSTALATION
# 
# Two ways:
# 
# A. Paste the the .py file to text editor and run (ALT+P)
# B. Unzip and place .py file to addons_contrib. In User Preferences / Addons tab search under Testing / NP Delete Fast and check the box.
# 
# Now you have the operator in your system. If you press Save User Preferences, you will have it at your disposal every time you run Bl.
# 
# SHORTCUTS
# 
# After succesful instalation of the addon, or it's activation from the text editor, the NP Delete Fast operator should be registered in your system. Enter User Preferences / Input, and under that 3DView / Object Mode. Search for definition assigned to simple Delete key (without SHIFT or CTRL) and instead object.delete type object.np_delete_fast_xxx (xxx being the number of the version). I suggest asigning it to the the Delete key without much explanation and regret.
# 
# USAGE
# 
# Select one or more objects. 
# Run operator (spacebar search - NP Delete Fast, or keystroke if you assigned it)
# 
# IMPORTANT PERFORMANCE NOTES
#
# Should be key-mapped only for object-mode. Other modes use specific delete functions and should not be replaced.
#
# WISH LIST
#
# None so far
#
# WARNINGS
#
# None so far



bl_info={
  'name':'NP Delete Fast 001',
  'author':'lukas_t, Okavango',
  'version':(0,0,1),
  'blender':(2,68,0),
  'location':'View3D',
  'description':'Delete objects without confirmation - install, assign shortcut, save user settings',
  'category':'3D View'}

import bpy

class NPDeleteFast001(bpy.types.Operator):
    bl_idname='object.np_delete_fast_001'
    bl_label='NP Delete Fast 001'
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):
        bpy.ops.object.delete('EXEC_DEFAULT')
        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
       
if __name__ == "__main__":
    register()