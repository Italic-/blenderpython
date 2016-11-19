 
 

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
# Measures distance using start and end points.
#
# Emulates the functionality of the standard 'distance' command in CAD applications, with start and end points. 
# 
# INSTALATION
# 
# Two ways:
# 
# A. Paste the the .py file to text editor and run (ALT+P)
# B. Unzip and place .py file to addons_contrib. In User Preferences / Addons tab search under Testing / NP Point Distance and check the box.
# 
# Now you have the operator in your system. If you press Save User Preferences, you will have it at your disposal every time you run Bl.
# 
# SHORTCUTS
# 
# After succesful instalation of the addon, or it's activation from the text editor, the NP Poind Distance operator should be registered in your system. Enter User Preferences / Input, and under that, 3DView / Object Mode. Search for definition assigned to simple M key (provided that you don't use it for placing objects into layers, instead of now almost-standard 'Layer manager' addon) and instead object.move_to_layer, type object.np_point_distance_xxx (xxx being the number of the version). I suggest asigning hotkey only for the Object Mode because the addon doesn't work in other modes. Also, this way the basic G command should still be available and at your disposal.
# 
# USAGE
# 
# 
# Run operator (spacebar search - NP Point Distance, or keystroke if you assigned it)
# Select a point anywhere in the scene (holding CTRL enables snapping). This will be your start point.
# Move your mouse anywhere in the scene, in relation to the start point (again CTRL - snap). The addon will show the distance between your start and end points.
# Middle mouse button (MMB) enables axis constraint, numpad keys enable numerical input of distance, and RMB and ESC key interrupt the operation. 
#
# IMPORTANT PERFORMANCE NOTES
#
# Should be key-mapped only for Object Mode. Other modes are not supported and key definitions should not be replaced.
#
# WISH LIST
#
# X/Y/Z distance components
# Custom colors, fonts and unit formats
# Navigation enabled during use
# Smarter code and faster performance
#
# WARNINGS
#
# None so far



bl_info={
  'name':'NP Point Distance 014',
  'author':'Okavango with CoDEmanX, lukas_t, matali',
  'version':(0,1,4),
  'blender':(2,75,0),
  'location':'View3D',
  'description':'Measure distances using start and end points - install, assign shortcut, save user settings',
  'category':'3D View'}

import bpy
import bgl
import blf
import mathutils
from bpy_extras import view3d_utils
from bpy.app.handlers import persistent
from mathutils import Vector, Matrix

# Defining the main class - the macro:
class NPPointDistance014(bpy.types.Macro):
    bl_idname='object.np_point_distance_014'
    bl_label='NP Point Distance 014'
    bl_options={'REGISTER','UNDO'}

# Defining the storage class that will serve as a varable-bank for exchange among the classes. Later, this bank will recieve more variables with their values for safe keeping, as the program goes on:
class Storage:

    startloc3d=(0.0,0.0,0.0)
    endloc3d=(0.0,0.0,0.0)
    mode=0
    start=None
    end=None

# Defining the first of the operational classes for aquiring the list of selected objects and storing them for later re-call:    
class NPPDGetSelection(bpy.types.Operator):
    bl_idname='object.np_pd_get_selection'
    bl_label='NP PD Get Selection'
    bl_options={'INTERNAL'}
    
    def execute(self,context):
        # First, storing all of the system preferences set by the user, that will be changed during the process, in order to restore them when the operation is completed:
        Storage.use_snap=bpy.context.tool_settings.use_snap 
        Storage.snap_element=bpy.context.tool_settings.snap_element
        Storage.snap_target=bpy.context.tool_settings.snap_target
        Storage.pivot_point=bpy.context.space_data.pivot_point
        Storage.trans_orient=bpy.context.space_data.transform_orientation
        Storage.acob=bpy.context.active_object
        if bpy.context.mode == 'OBJECT':
            Storage.edit_mode='OBJECT'
        elif bpy.context.mode in ('EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_TEXT', 'EDIT_ARMATURE', 'EDIT_METABALL', 'EDIT_LATTICE'):
            Storage.edit_mode='EDIT'
        elif bpy.context.mode == 'POSE':
            Storage.edit_mode='POSE'
        elif bpy.context.mode == 'SCULPT':
            Storage.edit_mode='SCULPT'
        elif bpy.context.mode == 'PAINT_WEIGHT':
            Storage.edit_mode='WEIGHT_PAINT'
        elif bpy.context.mode == 'PAINT_TEXTURE':
            Storage.edit_mode='TEXTURE_PAINT'
        elif bpy.context.mode == 'PAINT_VERTEX':
            Storage.edit_mode='VERTEX_PAINT'
        elif bpy.context.mode == 'PARTICLE':
            Storage.edit_mode='PARTICLE_EDIT'            
        Storage.mode=0
        #Storage.curloc=bpy.context.scene.cursor_location
        #print('curloc',Storage.curloc)      
        # Reading and storing the selection:
        selob=bpy.context.selected_objects
        Storage.selob=selob
        # Deselecting objects in prepare for other proceses in the script:
        for ob in selob:
            ob.select=False
        return {'FINISHED'}

# Defining the operator that will add a dummy object on the original point of cursor location. 3D cursor will leave this position, go to the pointer, serve as an anchor generation location and come back, so there needs to be an object to safeguard his original position. After that, this dummy gets deleted:
class NPPDReadMouseLoc(bpy.types.Operator):
    bl_idname='object.np_pd_read_mouse_loc'
    bl_label='NP PD Read Mouse Loc'
    bl_options={'INTERNAL'}    
    
    def modal(self,context, event):
        region = context.region
        rv3d = context.region_data
        co2d = ((event.mouse_region_x, event.mouse_region_y))
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d) 
        pointloc = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d) + view_vector/5
        print(pointloc)
        Storage.pointloc=pointloc

        #print('020')         
        return{'FINISHED'}
    
    def invoke(self,context,event):
        #print("START_____")
        args=(self,context)
      
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}    
    
# Defining the operator that will generate a one-vertex mesh i call anchor, at the spot marked by 3d cursor:
class NPPDAddPoint(bpy.types.Operator):
    bl_idname='object.np_pd_add_point'
    bl_label='NP PD Add Point'
    bl_options={'INTERNAL'}    
    
    def execute(self, context):

        pointloc=Storage.pointloc
        if bpy.context.mode not in ('OBJECT'):
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.add(type='MESH',location=pointloc)
        start=bpy.context.object
        start.name='NP_PD_start'
        Storage.start=start
        bpy.ops.object.add(type='MESH',location=pointloc)
        end=bpy.context.object
        end.name='NP_PD_end'
        Storage.end=end
        start.select=True
        end.select=True       
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='MEDIAN_POINT'
        bpy.context.space_data.transform_orientation='GLOBAL' 
        return{'FINISHED'}
    
# Deleting dummy object and activating anchor for it's use in the select-point process:
class NPPDActivatePoint(bpy.types.Operator):
    bl_idname='object.np_pd_activate_point'
    bl_label='NP PD Activate Point'
    bl_options={'INTERNAL'}    
    
    def execute(self,context):
        point=Storage.point
        bpy.context.scene.objects.active=point
        point.select=True
        # Preparing for the move operator, that will enable us to carry the anchor to desired point for the translation. For this, we need to enable the specific snap parameters:
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='MEDIAN_POINT'
        bpy.context.space_data.transform_orientation='GLOBAL'        
        #print('050')
        return{'FINISHED'}
    
# Defining the operator that will let the user translate the anchor to the desired point. It also uses some listening operators that clean up the leftovers should the user interrupt the command. Many thanks to CoDEmanX and lukas_t:

def draw_callback_px(self, context):
    sel=bpy.context.selected_objects
    mode=Storage.mode
    startloc3d=Storage.startloc3d
    endloc3d=Storage.endloc3d  
    region = context.region
    rv3d = context.region_data
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    if startloc2d == None:
        startloc2d=(0.0,0.0)
        endloc2d=(0.0,0.0)
    print(startloc2d, endloc2d)
    
    dist = (mathutils.Vector(endloc3d) - mathutils.Vector(startloc3d))
    dist = dist.length
    dist = str(abs(round(dist,2)))    
    numloc = []
    numloc.append((startloc2d[0]+endloc2d[0])/2)
    numloc.append((startloc2d[1]+endloc2d[1])/2)
    
    if mode==0:
        main='SELECT START POINT'
        
    if mode==1:
        main='SELECT END POINT'    
           
    bgl.glEnable(bgl.GL_BLEND)
    # First color is for lighter themes, second for default and darker themes:       
    #bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    bgl.glLineWidth(1.35)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f(*startloc2d)
    bgl.glVertex2f(*endloc2d)
    bgl.glEnd()
    
    bgl.glColor4f(0.1, 0.1, 0.1, 1.0) 
    if mode == 1:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, numloc[0], numloc[1], 0)
        blf.draw(font_id, dist)   
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)           
                          
    font_id=0
    bgl.glColor4f(1,1,1,0.25)
    blf.size(font_id,88,72)
    blf.position(font_id,5,75,0)
    blf.draw(font_id,'N')
    blf.size(font_id,28,72)    
    blf.position(font_id,22,75,0)
    blf.draw(font_id,'P')    
    bgl.glColor4f(1,1,1,1)
    blf.position(font_id,75,125,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    bgl.glColor4f(0,0.5,0,1)
    blf.size(font_id,11,72)
    blf.position(font_id,75,105,0)
    blf.draw(font_id,'LMB - select, CTRL - snap')
    blf.position(font_id,75,90,0)
    blf.draw(font_id,'MMB - change axis')
    #blf.position(font_id,75,75,0)
    #blf.draw(font_id,'NUMPAD - value')
    bgl.glColor4f(1,0,0,1)
    blf.position(font_id,75,75,0)
    blf.draw(font_id,'ESC, RMB - quit')
    
def scene_update(context):
    
    
    
    #a = 'vozdra'
    if bpy.data.objects.is_updated:
        mode = Storage.mode
        print('mode',mode)
        start = Storage.start
        end = Storage.end
        if mode == 1:
            startloc3d = start.location      
            endloc3d = end.location
            Storage.startloc3d=startloc3d
            Storage.endloc3d=endloc3d
        #print('startloc3d', Storage.startloc3d)  
        #print('endloc3d', Storage.endloc3d)
        
    
class NPPDRunTranslate(bpy.types.Operator):
    bl_idname='object.np_pd_run_translate'
    bl_label='NP PD Run Translate'
    bl_options={'INTERNAL'}

    count=0
       
    def modal(self,context,event):
        context.area.tag_redraw()        
        self.count+=1
        selob=Storage.selob
        start=Storage.start
        end=Storage.end
        mode=Storage.mode
        #print('080')
        
        if self.count == 1:
            bpy.ops.transform.translate('INVOKE_DEFAULT')
                     
        elif event.type in ('LEFTMOUSE','RET','NUMPAD_ENTER','SPACE') and event.value=='RELEASE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
  
            #Storage.startloc3d=point.location   
            #print('self.endloc3d',self.endloc3d)
            #print('Storage.startloc3d', Storage.startloc3d)
            #print('Storage.endloc3d', Storage.endloc3d)              
            return{'FINISHED'}
        elif event.type in ('ESC','RIGHTMOUSE'):
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.select_all(action='DESELECT')
            start.select=True                      
            end.select=True
            bpy.ops.object.delete('EXEC_DEFAULT') 
            for ob in selob:
                ob.select=True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.mode=0                   
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            bpy.context.scene.objects.active=Storage.acob
            bpy.ops.object.mode_set(mode = Storage.edit_mode)
            
            return{'CANCELLED'}
        return{'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')       
            selob = bpy.context.selected_objects
            Storage.selob = selob
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'} 

# Reselecting the objects from the list of originaly selected objects:    
class NPPDChangeModeOne(bpy.types.Operator):
    bl_idname = "object.np_pd_change_mode_one"
    bl_label = "NP PD Change Mode One"
    bl_options={'INTERNAL'} 
        
    def execute(self, context):
        Storage.mode=1
        start=Storage.start
        end=Storage.end
        startloc3d = start.location      
        endloc3d = end.location
        Storage.startloc3d=startloc3d
        Storage.endloc3d=endloc3d
        #loc=end.location
        #bpy.ops.mesh.primitive_cube_add(location=loc)       
        #ob=bpy.context.object
        #Storage.startloc3d=ob.location
        bpy.ops.object.select_all(action='DESELECT')
        #ob.select=True
        #bpy.ops.object.delete('EXEC_DEFAULT')
        end.select=True     
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='ACTIVE_ELEMENT'
        bpy.context.space_data.transform_orientation='GLOBAL'            
        return {'FINISHED'}

# Deleting the anchor after succesfull translation:    
class NPPDDeletePoint(bpy.types.Operator):
    bl_idname = "object.np_pd_delete_point"
    bl_label = "NP PD Delete Point"
    bl_options={'INTERNAL'}
        
    def execute(self, context):
        selob=Storage.selob
        start=Storage.start
        end=Storage.end
        bpy.ops.object.select_all(action='DESELECT')                       
        start.select=True
        end.select=True
        bpy.ops.object.delete('EXEC_DEFAULT')
        for ob in selob:
            ob.select=True
        Storage.startloc3d=(0.0,0.0,0.0)
        Storage.endloc3d=(0.0,0.0,0.0)
        Storage.mode=0        
        bpy.context.tool_settings.use_snap=Storage.use_snap
        bpy.context.tool_settings.snap_element=Storage.snap_element
        bpy.context.tool_settings.snap_target=Storage.snap_target
        bpy.context.space_data.pivot_point=Storage.pivot_point
        bpy.context.space_data.transform_orientation=Storage.trans_orient
        bpy.context.scene.objects.active=Storage.acob
        bpy.ops.object.mode_set(mode = Storage.edit_mode)
        return {'FINISHED'}
    
# This is the actual addon process, the algorithm that defines the order of operator activation inside the main macro: 
def register():
    
    bpy.utils.register_module(__name__)
    bpy.app.handlers.scene_update_post.append(scene_update)    
    
    NPPointDistance014.define('OBJECT_OT_np_pd_get_selection')
    NPPointDistance014.define('OBJECT_OT_np_pd_read_mouse_loc')
    NPPointDistance014.define('OBJECT_OT_np_pd_add_point')
    #NPPointDistance014.define('OBJECT_OT_np_pd_activate_point')
    NPPointDistance014.define('OBJECT_OT_np_pd_run_translate')
    NPPointDistance014.define('OBJECT_OT_np_pd_change_mode_one')
    NPPointDistance014.define('OBJECT_OT_np_pd_run_translate')
    #NPPointDistance014.define('OBJECT_OT_np_pd_change_mode_two')
    NPPointDistance014.define('OBJECT_OT_np_pd_delete_point')  

def unregister():
 
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.scene_update_post.remove(scene_update)       
       
if __name__ == "__main__":
    register()