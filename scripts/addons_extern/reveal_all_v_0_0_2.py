'''
Copyright (C) 2016 Lepiller cedric
pitiwazou@gmail.com

Created by Lepiller cedric

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


bl_info = {
    "name": "Reveal All",
    "description": "Reveal all the hidden objects and keeps the current selection",
    "author": "Pitiwazou",
    "version": (0, 0, 2),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Object" }
    


import bpy
import bmesh

class RevealAllPrefs(bpy.types.AddonPreferences):
    """Creates the tools in a Panel, in the scene context of the properties editor"""
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        
        box=layout.box()
        box.label(text="Info :")
        box.label(text="This Addon reveal all hidden objects")
        box.label(text="Deactivate the 'Clear Restrict View' in the preferences Inputs")
        box.operator("wm.url_open", text="Instructions").url = "http://pitiwazou.com/Photoshop_2016-12-16_10-34-28.jpg"
        
        box=layout.box()
        box.label(text="Links :")
        row=box.row(align=True)
        row.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
        row.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
        row.operator("wm.url_open", text="BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/"
        
        box=layout.box()
        box.label(text="Addons :")
        box.operator("wm.url_open", text="Asset Management").url = "https://gumroad.com/l/kANV"
        box.operator("wm.url_open", text="Speedflow").url = "https://gumroad.com/l/speedflow"
        box.operator("wm.url_open", text="SpeedSculpt").url = "https://gumroad.com/l/SpeedSculpt"
        box.operator("wm.url_open", text="SpeedRetopo").url = "https://gumroad.com/l/speedretopo "


class RevealAllKeepSelection(bpy.types.Operator):
    bl_idname = "object.reveal_all_keep_selection"
    bl_label = "Reveal All and Keep Selection"
    bl_description = "Reveal all the hidden objects and keeps the selection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        #Object selection
        obj_active = context.active_object
        selection_active = [obj for obj in bpy.context.selected_objects]
        
        #Object Mode
        if context.object is not None and bpy.context.object.mode == "OBJECT":
            if len(bpy.context.selected_objects) >= 1:
                
                bpy.ops.object.hide_view_clear()
                bpy.ops.object.select_all(action='DESELECT')
                
                for obj in selection_active:
                    bpy.context.scene.objects.active = obj 
                    obj.select=True
                    
                    #Select the previous active object
                    bpy.context.scene.objects.active = obj_active
                    
                del(selection_active[:])      
        
        elif context.object is None :
                bpy.ops.object.hide_view_clear()
                bpy.ops.object.select_all(action='DESELECT') 
        
        
        #Edit Mode
        elif bpy.context.object.mode == "EDIT":
            #Faces selection 
            obj = context.object
            bm = bmesh.from_edit_mesh(obj.data)
            selected_faces = [f for f in bm.faces if f.select]
            selected_vertices = [v for v in bm.verts if v.select]
            selected_edges = [e for e in bm.edges if e.select]
            
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action='DESELECT')
            
    
            #Vertex            
            if tuple (bpy.context.tool_settings.mesh_select_mode) == (True, False, False) :
                for v in selected_vertices:
                    if selected_vertices:
                        v.select=True 
            
            #Edges            
            elif tuple (bpy.context.tool_settings.mesh_select_mode) == (False, True, False) :
                for e in selected_edges:
                    if selected_edges:
                        e.select=True   
            
            #Faces
            else:
                for f in selected_faces :
                    if selected_faces:
                        f.select=True               
        
            del(selected_faces[:])  
            del(selected_vertices[:]) 
            del(selected_edges[:])              
        
                     
        return {"FINISHED"}    

addon_keymaps = []
def register():
    bpy.utils.register_module(__name__)
    wm = bpy.context.window_manager
    
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(RevealAllKeepSelection.bl_idname, 'H', 'PRESS', alt= True)
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_module(__name__)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]

if __name__ == "__main__":
    register()
