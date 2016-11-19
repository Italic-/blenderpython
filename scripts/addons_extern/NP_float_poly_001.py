 
 

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

"""

DESCRIPTION:
 
Draws a polyline using snap points. Emulates the functionality of the standard 'polyline' command in CAD applications, with vertex snapping. Extrudes and bevels the shape afterwards.


INSTALLATION:
 
Two ways:
 
A. Paste the the .py file to text editor and run (ALT+P)
B. Unzip and place .py file to addons_contrib. In User Preferences / Addons tab search under Testing / NP Float Poly and check the box.
 
Now you have the operator in your system. If you press Save User Preferences, you will have it at your disposal every time you run Blender.
 

SHORTCUTS:
 
After successful installation of the addon, or it's activation from the text editor, the NP Float Poly operator should be registered in your system. Enter User Preferences / Input, and under that, 3DView / Object mode. At the bottom of the list click the 'Add new' button. In the operator field type object.np_float_poly_xxx (xxx being the number of the version) and assign a key of your preference. At the moment i am using 'P' for 'polyline'.


USAGE:
 
You can run the operator with spacebar search - NP Float Poly, or keystroke if you assigned it.
Select a point anywhere in the scene (holding CTRL enables snapping). This will be your start point.
Move your mouse and click to a point anywhere in the scene with the left mouse button (LMB), in relation to the start point (again CTRL - snap). The addon will make a line from the first to the second point. You can continue adding other points in the same way. When you want to finish the poly, press ESC or if you want to close it, press right mouse button (RMB). After the closure of the poly, the command will automatically start the extrusion of the poly into 3D. You can confirm this with the LMB or avoid the extrusion with ESC. This will restrict the poly to 2D surface.
If at any point you lose sight of the next point you want to snap to, you can press SPACE to go to NAVIGATION mode in which you can change the point of view. When your next point is clearly in your field of view, you return to normal mode by pressing SPACE again or LMB. 
Middle mouse button (MMB) enables axis constraint during snapping, while numpad keys enable numerical input poly segment length.
After the extrusion, if you enabled the bevel function in the addon options, the script will start the bevel operation which you control as usual - LMB for the amount and MMB scroll for the number of segments.


ADDON SETTINGS:

Below the addon name in the user preferences / addon tab, you can find a couple of settings that control the behavior of the addon:

Unit scale: Distance multiplier for various unit scenarios
Suffix: Unit abbreviation after the numerical distance
Custom colors: Default or custom colors for graphical elements
Mouse badge: Option to display a small cursor label
Point markers: Option to display graphical markers for the start and segment points
Bevel: Option to automatically start a bevel operation after the extrusion
Base material: Option to add a basic material to the poly object
Smooth shading: Option to turn on smooth shading for the poly object
Wire contour: Option to turn on wireframe over the solid


IMPORTANT PERFORMANCE NOTES:

Unfortunately, this addon is effected by blender development and in linux 2.77 and 2.78 it shows a strange bug as viewport fps falls dramatically after the command. However, pressing 2xTAB solves the issue. I am not sure what causes the problem, i found no similar issues in version 2.76 and 2.75 in which the addon was made and used.


"""



bl_info={
  'name':'NP Float Poly 001',
  'author':'Okavango with Blenderartists community',
  'version':(0,0,1),
  'blender':(2,75,0),
  'location':'View3D',
  'description':'Draw lines and closed polygons using vertex snap - install, assign shortcut, save user settings',
  'category':'3D View'}

import bpy
import copy
import bmesh
import bgl
import blf
import mathutils
from bpy_extras import view3d_utils
from bpy.app.handlers import persistent
from mathutils import Vector, Matrix
from blf import ROTATION
from math import radians


# Defining the main class - the macro:

class NPFloatPoly001(bpy.types.Macro):
    bl_idname='object.np_float_poly_001'
    bl_label='NP Float Poly 001'
    bl_options={'REGISTER','UNDO'}

# Defining the storage class that will serve as a variable-bank for exchange among the classes. Later, this bank will receive more variables with their values for safe keeping, as the program goes on:

class Storage:

    startloc3d = (0.0,0.0,0.0)
    endloc3d = (0.0,0.0,0.0)
    phase = 0
    first = None
    start = None
    end = None
    dist = None
    polyob = None
    flag ='TRANSLATE'
    flash = [[18, 37], [21, 37], [23, 33], [26, 33]]


# Defining the first of the operational classes for acquiring the list of selected objects and storing them for later re-call:

class NPFPGetSelection(bpy.types.Operator):
    bl_idname='object.np_fp_get_selection'
    bl_label='NP FP Get Selection'
    bl_options={'INTERNAL'}
    
    def execute(self,context):
      
        # First, storing all of the system preferences set by the user, that will be changed during the process, in order to restore them when the operation is completed:
        
        print('01_get_selection_START')
        Storage.use_snap=bpy.context.tool_settings.use_snap 
        Storage.snap_element=bpy.context.tool_settings.snap_element
        Storage.snap_target=bpy.context.tool_settings.snap_target
        Storage.pivot_point=bpy.context.space_data.pivot_point
        Storage.trans_orient=bpy.context.space_data.transform_orientation
        Storage.acob=bpy.context.active_object
        print ('Storage.acob =', Storage.acob)
        print (bpy.context.mode)
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
        Storage.phase=0 
        # Reading and storing the selection:
        selob=bpy.context.selected_objects
        Storage.selob=selob
        # De-selecting objects in prepare for other processes in the script:
        for ob in selob:
            ob.select=False
        print('01_get_selection_END')
        return {'FINISHED'}

# Defining the operator that will read the mouse position in 3D when the command is activated and store it as a location for placing the start and end points under the mouse:

class NPFPReadMouseLoc(bpy.types.Operator):
    bl_idname='object.np_fp_read_mouse_loc'
    bl_label='NP FP Read Mouse Loc'
    bl_options={'INTERNAL'}    
    
    def modal(self,context, event):
        print('02_read_mouse_loc_START')
        region = context.region
        rv3d = context.region_data
        co2d = ((event.mouse_region_x, event.mouse_region_y))
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d) 
        pointloc = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d) + view_vector/5
        print(pointloc)
        Storage.pointloc=pointloc
        print('02_read_mouse_loc_END')
        return{'FINISHED'}
    
    def invoke(self,context,event):
        print('02_read_mouse_loc_INVOKE_a')
        #print("START_____")
        args=(self,context)     
        context.window_manager.modal_handler_add(self)
        print('02_read_mouse_loc_INVOKE_b')
        return {'RUNNING_MODAL'}    
    
# Defining the operator that will generate start and end points at the spot marked by mouse and select them, preparing for translation:

class NPFPAddPoints(bpy.types.Operator):
    bl_idname='object.np_fp_add_points'
    bl_label='NP FP Add Points'
    bl_options={'INTERNAL'}    
    
    def execute(self, context):
        print('03_add_points_START')  
        pointloc=Storage.pointloc
        if bpy.context.mode not in ('OBJECT'):
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.add(type='MESH',location=pointloc)
        start=bpy.context.object
        start.name='NP_FP_start'
        Storage.start=start
        bpy.ops.object.add(type='MESH',location=pointloc)
        end=bpy.context.object
        end.name='NP_FP_end'
        Storage.end=end
        start.select=True
        end.select=True       
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='MEDIAN_POINT'
        bpy.context.space_data.transform_orientation='GLOBAL'
        print('03_add_points_END')
        return{'FINISHED'}

    
# Defining the operator that will draw the OpenGL line across the screen together with the numerical distance and the on-screen instructions in normal, translation mode:

def draw_callback_px_TRANS(self, context):
    
    print('04_callback_TRANS_START')
    
    
    addon_prefs = context.user_preferences.addons[__name__].preferences

    scale = addon_prefs.scale
    badge = addon_prefs.badge
    point_size = addon_prefs.point_size
    badge_size = addon_prefs.badge_size

    
    polyob = Storage.polyob
    phase = Storage.phase
    start = Storage.start
    end = Storage.end
    startloc3d = start.location
    endloc3d = end.location
    endloc = end.location
    region = context.region
    rv3d = context.region_data
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    mouseloc = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc)
    #print(end, endloc, mouseloc)
    
    if addon_prefs.col_line_main_DEF == False:
        col_line_main = addon_prefs.col_line_main
    else:
        col_line_main = (1.0, 1.0, 1.0, 1.0) 

    if addon_prefs.col_line_shadow_DEF == False:
        col_line_shadow = addon_prefs.col_line_shadow
    else:
        col_line_shadow = (0.1, 0.1, 0.1, 0.25)
    
    if addon_prefs.col_num_main_DEF == False:
        col_num_main = addon_prefs.col_num_main
    else:
        col_num_main = (0.1, 0.1, 0.1, 0.75) 
    
    if addon_prefs.col_num_shadow_DEF == False:
        col_num_shadow = addon_prefs.col_num_shadow
    else:
        col_num_shadow = (1.0, 1.0, 1.0, 1.0)
        
    if addon_prefs.point_color_DEF == False:
        col_pointromb = addon_prefs.point_color
    else:
        col_pointromb = (0.3, 0.3, 0.3, 1.0)        

    if addon_prefs.suffix == 'None':
        suffix=None

    elif addon_prefs.suffix == 'km':
        suffix=' km'
        
    elif addon_prefs.suffix == 'm':
        suffix=' m'
        
    elif addon_prefs.suffix == 'cm':
        suffix=' cm'
        
    elif addon_prefs.suffix == 'mm':
        suffix=' mm'
        
    elif addon_prefs.suffix == 'nm':
        suffix=' nm'
        
    elif addon_prefs.suffix == "'":
        suffix="'"
        
    elif addon_prefs.suffix == '"':
        suffix='"'
        
    elif addon_prefs.suffix == 'thou':
        suffix=' thou'           
    #print('0')
    #sel=bpy.context.selected_objects

    if startloc2d == None:
        startloc2d = (0.0,0.0)
        endloc2d = (0.0,0.0)
    print(startloc2d, endloc2d)
    #print('1')
    dist = (mathutils.Vector(endloc3d) - mathutils.Vector(startloc3d))
    dist = dist.length*scale
    print('dist =', dist)
    if suffix is not None:
        dist = str(abs(round(dist,2)))+suffix
    else:
        dist = str(abs(round(dist,2)))
    print('dist =', dist)
    Storage.dist = dist
    #print('2')
    #This is for correcting the position of the numerical on the screen if the endpoints are far out of screen:    
    numloc = []
    startx = startloc2d[0]
    starty = startloc2d[1]
    endx = endloc2d[0]
    endy = endloc2d[1]
    if startx > region.width:
        startx = region.width
    if startx < 0:
        startx = 0
    if starty > region.height:
        starty = region.height
    if starty < 0:
        starty = 0        
    if endx > region.width:
        endx = region.width
    if endx < 0:
        endx = 0
    if endy > region.height:
        endy = region.height
    if endy < 0:
        endy = 0        
    numloc.append((startx+endx)/2)
    numloc.append((starty+endy)/2) 
    #print('3')
    if phase == 0:
        main='PLACE START POINT'
        
    if phase > 0:
        main='PLACE NEXT POINT'
           

    #Drawing:
           
    bgl.glEnable(bgl.GL_BLEND)
    
    #LINE:
    
    bgl.glColor4f(*col_line_shadow)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f((startloc2d[0]-1),(startloc2d[1]-1))
    bgl.glVertex2f((endloc2d[0]-1),(endloc2d[1]-1))
    bgl.glEnd()
    
    bgl.glColor4f(*col_line_main)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f(*startloc2d)
    bgl.glVertex2f(*endloc2d)
    bgl.glEnd()
    #print('4')
    
    #POINT MARKERS:
    markersize = point_size
    triangle = [[0, 0], [-1, 1], [1, 1]]    
    romb = [[-1, 0], [0, 1], [1, 0], [0, -1]]    
    if phase > 0 and polyob is None:
        polylist2d = []
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + startloc2d[0]
            co[1] = round((co[1] * markersize * 3),0) + startloc2d[1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for co in pointromb:    
            co[0] = round((co[0] * markersize),0) + endloc2d[0]
            co[1] = round((co[1] * markersize),0) + endloc2d[1]
        if phase == 2:
            print ('pointromb', pointromb)
            bgl.glColor4f(*col_pointromb)
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for x,y in pointromb:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
    if polyob is not None:
        print ('polyob not None')
        polyloc = polyob.location
        polyme = polyob.data
        polylist3d = []
        for me in polyme.vertices:
            polylist3d.append(me.co + polyloc)
        print ('polylist3d = ', polylist3d)
        polylist2d = []
        for p3d in polylist3d:
            p2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p3d)
            polylist2d.append(p2d)
        print ('polylist2d = ', polylist2d)
        #triangle for the first point
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + polylist2d[0][0]
            co[1] = round((co[1] * markersize * 3),0) + polylist2d[0][1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        #rombs for the other points
        i = 0
        for p2d in polylist2d:
            if i > 0:
                pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
                for co in pointromb:    
                    co[0] = round((co[0] * markersize),0) + p2d[0]
                    co[1] = round((co[1] * markersize),0) + p2d[1]
                print ('pointromb', pointromb)
                bgl.glColor4f(*col_pointromb)
                bgl.glBegin(bgl.GL_TRIANGLE_FAN)
                for x,y in pointromb:
                    bgl.glVertex2f(x,y)
            i = i + 1
            bgl.glEnd()
            
    #NUMERICAL DISTANCE:
    
    print('numloc = ' ,numloc, 'dist = ', dist)
    
    bgl.glColor4f(*col_num_shadow) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, (numloc[0]-1), (numloc[1]-1), 0)
        blf.draw(font_id, dist)
        
    bgl.glColor4f(*col_num_main) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, numloc[0], numloc[1], 0)
        blf.draw(font_id, dist)        
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)           
    #print('5')
    #ON-SCREEN INSTRUCTIONS:
    
    font_id=0
    
    bgl.glColor4f(1,1,1,0.35)
    blf.size(font_id,88,72)
    blf.position(font_id,5,74,0)
    blf.draw(font_id,'N')
    blf.size(font_id,28,72)    
    blf.position(font_id,22,74,0)
    blf.draw(font_id,'P')
    
    blf.enable(font_id, ROTATION)
    bgl.glColor4f(1,1,1,0.40)    
    ang = radians(90)
    blf.size(font_id,19,72)
    blf.rotation(font_id,ang)
    blf.position(font_id,78,73,0)
    blf.draw(font_id,'FP 001')
    blf.disable(font_id, ROTATION)
    
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    blf.position(font_id,93,124,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(1,1,1,1)
    blf.position(font_id,94,125,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(0,0.5,0,1)
    blf.size(font_id,11,72)
    blf.position(font_id,93,105,0)
    blf.draw(font_id,'CTRL - snap, LMB - confirm, MMB - lock axis, NUMPAD - value')
    #bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
    blf.position(font_id,93,90,0)
    blf.draw(font_id,'RMB - close poly and extrude, ENTER - close poly and stop')
    #bgl.glColor4f(0.5, 0.75, 0.0, 1.0)
    blf.position(font_id,93,75,0)
    blf.draw(font_id,'SPACE - navigate')
    #print('6')
    #blf.position(font_id,75,75,0)
    #blf.draw(font_id,'NUMPAD - value')
    
    bgl.glColor4f(1,0,0,1)
    blf.position(font_id,93,60,0)
    blf.draw(font_id,'ESC - stop poly now')

    # Drawing the small badge near the cursor with the basic instructions:

    if badge == True:
        square = [[17, 30], [17, 40], [27, 40], [27, 30]]
        rectangle = [[27, 30], [27, 40], [67, 40], [67, 30]]        
        flash = copy.deepcopy(Storage.flash)
        print ('flash', flash)
        size = badge_size
        ipx = 29
        ipy = 33
      
        for co in square:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]
        for co in rectangle:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]
        for co in flash:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]

        ipx = round((ipx * size),0) -(size*10) + mouseloc[0]
        ipy = round((ipy * size),0) -(size*25) + mouseloc[1]
        ipsize = int(6* size)            
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in square:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in rectangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINE_STRIP) 
        for x,y in flash:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(font_id,ipx,ipy,0)
        blf.size(font_id,ipsize,72)
        blf.draw(font_id,'CTRL+SNAP')         
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    #print('7')
    print('04_callback_TRANS_END')
    
def scene_update(context):
    #print('00_scene_update_START')
    #print('up1')
    if bpy.data.objects.is_updated:
        phase = Storage.phase
        flag = Storage.flag
        print(flag)
        start = Storage.start
        end = Storage.end
        if phase == 1:
            #print('up2')
            startloc3d = start.location      
            endloc3d = end.location
            Storage.startloc3d = startloc3d
            Storage.endloc3d = endloc3d
        if flag == 'EXTRUDE':
            polyob = Storage.polyob
            polyme = polyob.data
            i = len(polyme.vertices)
            print('A')
            print('i', i)
            j = i / 2
            j = int(j)
            print(i,j)
            print(polyme.vertices[0].co)
            Storage.startloc3d = polyme.vertices[0].co
            Storage.endloc3d = polyme.vertices[j].co
            print('Ss3d, Se3d', Storage.startloc3d, Storage.endloc3d)
    #print('up3')
    #print('00_scene_update_END')

# Defining the operator that will let the user translate start and end to the desired point. It also uses some listening operators that clean up the leftovers should the user interrupt the command. Many thanks to CoDEmanX and lukas_t:
    
class NPFPRunTranslate(bpy.types.Operator):
    bl_idname='object.np_fp_run_translate'
    bl_label='NP FP Run Translate'
    bl_options={'INTERNAL'}

    print('04_run_TRANS_START')
    count=0
       
    def modal(self,context,event):
        context.area.tag_redraw()        
        self.count+=1
        selob=Storage.selob
        start=Storage.start
        end=Storage.end
        phase=Storage.phase
        polyob = Storage.polyob
        
        if self.count == 1:
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            print('04_run_TRANS_count_1_INVOKE_DEFAULT')
                     
        elif event.type in ('LEFTMOUSE','RET','NUMPAD_ENTER') and event.value=='RELEASE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            Storage.flag = 'PASS'
            print('04_run_TRANS_left_release_FINISHED')
            return{'FINISHED'}

        elif event.type == 'SPACE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            start.hide=True
            end.hide=True
            Storage.flag = 'NAVIGATE'
            print('04_run_TRANS_space_FINISHED_flag_NAVIGATE')
            return{'FINISHED'}

        elif event.type == 'RIGHTMOUSE' and phase > 1:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            end.location = start.location
            start.hide=True
            end.hide=True
            Storage.flag = 'CLOSE'
            print('04_run_TRANS_space_FINISHED_flag_NAVIGATE')
            return{'FINISHED'}       

        elif event.type == 'RIGHTMOUSE' and phase < 2:
        #this actually begins when user RELEASES esc or rightmouse, PRESS is taken by transform.translate operator        
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.select_all(action='DESELECT')
            start.select=True                      
            end.select=True
            bpy.ops.object.delete('EXEC_DEFAULT') 
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('04_run_TRANS_esc_right_CANCELLED')
  
        elif event.type == 'ESC':
        #this actually begins when user RELEASES esc or rightmouse, PRESS is taken by transform.translate operator        
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.select_all(action='DESELECT')
            start.select=True                      
            end.select=True
            bpy.ops.object.delete('EXEC_DEFAULT') 
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('04_run_TRANS_esc_right_CANCELLED')
            return{'CANCELLED'}
  
        print('04_run_TRANS_PASS_THROUGH')
        return{'PASS_THROUGH'}

    def invoke(self, context, event):
        flag = Storage.flag
        print('04_run_TRANS_INVOKE_a')
        print('flag=', flag)
        if flag == 'TRANSLATE':
            if context.area.type == 'VIEW_3D':           
                args = (self, context)
                self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px_TRANS, args, 'WINDOW', 'POST_PIXEL')      
                context.window_manager.modal_handler_add(self)
                print('04_run_TRANS_INVOKE_a_RUNNING_MODAL')
                return {'RUNNING_MODAL'}
            else:
                self.report({'WARNING'}, "View3D not found, cannot run operator")
                print('04_run_TRANS_INVOKE_a_CANCELLED')
                return {'CANCELLED'}
        else:
            print('04_run_TRANS_INVOKE_a_FINISHED')
            return {'FINISHED'}    

# Defining the operator that will draw the graphicall reprezentation of distance in navigation mode if user calls it:

def draw_callback_px_NAV(self, context):
    
    print('05_callback_NAV_START')
    
    addon_prefs = context.user_preferences.addons[__name__].preferences

    scale = addon_prefs.scale
    badge = addon_prefs.badge
    point_size = addon_prefs.point_size
    badge_size = addon_prefs.badge_size
    
    polyob = Storage.polyob
    phase = Storage.phase
    start = Storage.start
    end = Storage.end
    startloc3d = start.location
    endloc3d = end.location
    endloc = end.location
    region = context.region
    rv3d = context.region_data
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    mouseloc = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc)
    
    if addon_prefs.col_line_main_DEF == False:
        col_line_main = addon_prefs.col_line_main
    else:
        col_line_main = (1.0, 1.0, 1.0, 1.0) 

    if addon_prefs.col_line_shadow_DEF == False:
        col_line_shadow = addon_prefs.col_line_shadow
    else:
        col_line_shadow = (0.1, 0.1, 0.1, 0.25)
    
    if addon_prefs.col_num_main_DEF == False:
        col_num_main = addon_prefs.col_num_main
    else:
        col_num_main = (0.1, 0.1, 0.1, 0.75) 
    
    if addon_prefs.col_num_shadow_DEF == False:
        col_num_shadow = addon_prefs.col_num_shadow
    else:
        col_num_shadow = (1.0, 1.0, 1.0, 1.0)
        
    if addon_prefs.point_color_DEF == False:
        col_pointromb = addon_prefs.point_color
    else:
        col_pointromb = (0.3, 0.3, 0.3, 1.0)         

    if addon_prefs.suffix == 'None':
        suffix=None

    elif addon_prefs.suffix == 'km':
        suffix=' km'
        
    elif addon_prefs.suffix == 'm':
        suffix=' m'
        
    elif addon_prefs.suffix == 'cm':
        suffix=' cm'
        
    elif addon_prefs.suffix == 'mm':
        suffix=' mm'
        
    elif addon_prefs.suffix == 'nm':
        suffix=' nm'
        
    elif addon_prefs.suffix == "'":
        suffix="'"
        
    elif addon_prefs.suffix == '"':
        suffix='"'
        
    elif addon_prefs.suffix == 'thou':
        suffix=' thou'
        
    # Calculating the 3d points for the graphical line while in NAVIGATE flag:
   
    co2d = self.co2d
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d) 
    pointloc = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d) + view_vector/5
    
    print('phase=', phase)
    if phase == 0 or phase == 3:
        startloc3d=(0.0,0.0,0.0)
        endloc3d=(0.0,0.0,0.0)    
    
    if phase == 1:
        startloc3d = Storage.startloc3d
        endloc3d = pointloc
        
    if phase == 2:
        startloc3d = Storage.startloc3d
        endloc3d = pointloc   

    # Calculating the 2D points for the graphical line while in NAVIGATE flag from 3D points:
    
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    
    if startloc2d == None:
        startloc2d=(0.0,0.0)
        endloc2d=(0.0,0.0)
    print(startloc2d, endloc2d)
    
    dist = (mathutils.Vector(endloc3d) - mathutils.Vector(startloc3d))
    dist = dist.length*scale
    print(dist)
    
    if suffix is not None:
        dist = str(abs(round(dist,2)))+suffix
    else:
        dist = str(abs(round(dist,2)))
        
    Storage.dist = dist
    print(dist)
    
    #This is for correcting the position of the numerical on the screen if the endpoints are far out of screen:    
    numloc = []
    startx=startloc2d[0]
    starty=startloc2d[1]
    endx=endloc2d[0]
    endy=endloc2d[1]
    if startx > region.width:
        startx = region.width
    if startx < 0:
        startx = 0
    if starty > region.height:
        starty = region.height
    if starty < 0:
        starty = 0        
    if endx > region.width:
        endx = region.width
    if endx < 0:
        endx = 0
    if endy > region.height:
        endy = region.height
    if endy < 0:
        endy = 0        
    numloc.append((startx+endx)/2)
    numloc.append((starty+endy)/2)    
    
    if phase==0:
        main='NAVIGATE FOR BETTER PLACEMENT OF START POINT'
        
    if phase==1:
        main='NAVIGATE FOR BETTER PLACEMENT OF NEXT POINT' 
        
    if phase==2:
        main='NAVIGATE FOR BETTER PLACEMENT OF NEXT POINT'
        
    if phase==3:
        main='NAVIGATE FOR BETTER PLACEMENT OF EXTRUSION HEIGHT'        
                

    #Drawing:
           
    bgl.glEnable(bgl.GL_BLEND)
    
    #LINE:
    
    bgl.glColor4f(*col_line_shadow)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f((startloc2d[0]-1),(startloc2d[1]-1))
    bgl.glVertex2f((endloc2d[0]-1),(endloc2d[1]-1))
    bgl.glEnd()
    
    bgl.glColor4f(*col_line_main)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f(*startloc2d)
    bgl.glVertex2f(*endloc2d)
    bgl.glEnd() 
    
    #POINT MARKERS:
    markersize = point_size
    triangle = [[0, 0], [-1, 1], [1, 1]]    
    romb = [[-1, 0], [0, 1], [1, 0], [0, -1]]    
    if phase > 0 and polyob is None:
        polylist2d = []
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + startloc2d[0]
            co[1] = round((co[1] * markersize * 3),0) + startloc2d[1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for co in pointromb:    
            co[0] = round((co[0] * markersize),0) + endloc2d[0]
            co[1] = round((co[1] * markersize),0) + endloc2d[1]
        if phase == 2:
            print ('pointromb', pointromb)
            bgl.glColor4f(*col_pointromb)
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for x,y in pointromb:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
    if polyob is not None:
        print ('polyob not None')
        polyloc = polyob.location
        polyme = polyob.data
        polylist3d = []
        for me in polyme.vertices:
            polylist3d.append(me.co + polyloc)
        print ('polylist3d = ', polylist3d)
        polylist2d = []
        for p3d in polylist3d:
            p2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p3d)
            polylist2d.append(p2d)
        print ('polylist2d = ', polylist2d)
        #triangle for the first point
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + polylist2d[0][0]
            co[1] = round((co[1] * markersize * 3),0) + polylist2d[0][1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        #rombs for the other points
        i = 0
        for p2d in polylist2d:
            if i > 0:
                pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
                for co in pointromb:    
                    co[0] = round((co[0] * markersize),0) + p2d[0]
                    co[1] = round((co[1] * markersize),0) + p2d[1]
                print ('pointromb', pointromb)
                bgl.glColor4f(*col_pointromb)
                bgl.glBegin(bgl.GL_TRIANGLE_FAN)
                for x,y in pointromb:
                    bgl.glVertex2f(x,y)
            i = i + 1
            bgl.glEnd()
            
    #NUMERICAL DISTANCE:
    
    bgl.glColor4f(*col_num_shadow) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, (numloc[0]-1), (numloc[1]-1), 0)
        blf.draw(font_id, dist)
        
    bgl.glColor4f(*col_num_main) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, numloc[0], numloc[1], 0)
        blf.draw(font_id, dist)        
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)           
    
    #ON-SCREEN INSTRUCTIONS:
    
    font_id=0
    
    bgl.glColor4f(1,1,1,0.35)
    blf.size(font_id,88,72)
    blf.position(font_id,5,74,0)
    blf.draw(font_id,'N')
    blf.size(font_id,28,72)    
    blf.position(font_id,22,74,0)
    blf.draw(font_id,'P')
    
    blf.enable(font_id, ROTATION)
    bgl.glColor4f(1,1,1,0.40)    
    ang = radians(90)
    blf.size(font_id,19,72)
    blf.rotation(font_id,ang)
    blf.position(font_id,78,73,0)
    blf.draw(font_id,'FP 001')
    blf.disable(font_id, ROTATION)
    
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    blf.position(font_id,93,124,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(1,1,1,1)
    blf.position(font_id,94,125,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(0,0.5,0,1)
    blf.size(font_id,11,72)
    blf.position(font_id,93,105,0)
    blf.draw(font_id,'MMB, SCROLL - navigate')
    blf.position(font_id,93,90,0)
    blf.draw(font_id,'LMB, SPACE - leave navigate')
    
    #blf.position(font_id,75,75,0)
    #blf.draw(font_id,'NUMPAD - value')
    
    bgl.glColor4f(1,0,0,1)
    blf.position(font_id,93,75,0)
    blf.draw(font_id,'ESC, RMB - quit')
    
    # Drawing the small badge near the cursor with the basic instructions:

    if badge == True:
        square = [[17, 30], [17, 40], [27, 40], [27, 30]]
        rectangle = [[27, 30], [27, 40], [67, 40], [67, 30]]        
        flash = copy.deepcopy(Storage.flash)
        ipx = 29
        ipy = 33
        size = badge_size
        for co in square:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]
        for co in rectangle:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]
        for co in flash:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]

        ipx = round((ipx * size),0) -(size*10) + co2d[0]
        ipy = round((ipy * size),0) -(size*25) + co2d[1]
        ipsize = int(6* size)
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in square:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(0.5, 0.75, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in rectangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINE_STRIP) 
        for x,y in flash:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(font_id,ipx,ipy,0)
        blf.size(font_id,ipsize,72)
        blf.draw(font_id,'NAVIGATE')
          
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)    
    print('05_callback_NAV_END')


    
# Defining the operator that will enable navigation if user calls it:

class NPFPRunNavigate(bpy.types.Operator):
    bl_idname = "object.np_fp_run_navigate"
    bl_label = "NP FP Run Navigate"
    bl_options={'INTERNAL'}
    
    
    def modal(self, context, event):
        print('05_run_NAV_START')
        context.area.tag_redraw()
        selob = Storage.selob
        start = Storage.start
        end = Storage.end
        phase = Storage.phase
        polyob = Storage.polyob
        
        if event.type == 'MOUSEMOVE':
            print('05_run_NAV_mousemove_a')
            self.co2d = ((event.mouse_region_x, event.mouse_region_y))
            print('05_run_NAV_mousemove_b')
            
        elif event.type in {'LEFTMOUSE', 'SPACE'} and event.value == 'PRESS':
            print('05_run_NAV_left_space_press_START')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            self.co2d = ((event.mouse_region_x, event.mouse_region_y))
            phase=Storage.phase    
            region = context.region
            rv3d = context.region_data
            co2d = self.co2d
            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d) 
            pointloc = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d) + view_vector/5
            start=Storage.start
            end=Storage.end
            start.hide=False
            end.hide=False            
            print('phase=', phase)
            if phase == 0:
                startloc3d=(0.0,0.0,0.0)
                endloc3d=(0.0,0.0,0.0)    
                start.location = pointloc
                end.location = pointloc
                Storage.flag = 'TRANSLATE'
            if phase == 1:
                startloc3d = Storage.startloc3d
                endloc3d = pointloc
                end.location = pointloc
                Storage.flag = 'TRANSLATE'                
            if phase == 2:
                startloc3d = Storage.startloc3d
                endloc3d = pointloc
                end.location = pointloc
                Storage.flag = 'TRANSLATE'                
            if phase == 3:
                startloc3d=(0.0,0.0,0.0)
                endloc3d=(0.0,0.0,0.0)    
                start.location = pointloc
                end.location = pointloc
                Storage.flag = 'EXTRUDE'
                """
            if phase == 3.5:
                startloc3d=(0.0,0.0,0.0)
                endloc3d=(0.0,0.0,0.0)    
                start.location = pointloc
                end.location = pointloc
                Storage.flag = 'EXTRUDE'
                """
            Storage.start=start
            Storage.end=end
            Storage.startloc3d = startloc3d
            Storage.endloc3d = endloc3d

            print('05_run_NAV_left_space_press_FINISHED_flag_TRANSLATE')
            return {'FINISHED'}
        
        elif event.type == 'ESC':
            print('05_run_NAV_esc_right_any_START')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.select_all(action='DESELECT')
            start.hide=False                      
            end.hide=False
            start.select=True                      
            end.select=True
            bpy.ops.object.delete('EXEC_DEFAULT') 
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('05_run_NAV_esc_right_any_CANCELLED')
            return{'CANCELLED'}

        elif event.type == 'RIGHTMOUSE' and phase > 1:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            end.location = start.location
            start.hide=True
            end.hide=True
            Storage.flag = 'CLOSE'
            print('04_run_TRANS_space_FINISHED_flag_NAVIGATE')
            return{'FINISHED'} 


        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            print('05_run_NAV_middle_wheel_any_PASS_THROUGH')
            return {'PASS_THROUGH'}
        print('05_run_NAV_RUNNING_MODAL')
        return {'RUNNING_MODAL'}    

    def invoke(self, context, event):
        print('05_run_NAV_INVOKE_a')
        flag = Storage.flag
        phase = Storage.phase
        print('flag=', flag)
        self.co2d = ((event.mouse_region_x, event.mouse_region_y))
        if flag == 'NAVIGATE':           
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px_NAV, args, 'WINDOW', 'POST_PIXEL')      
            context.window_manager.modal_handler_add(self)
            print('05_run_NAV_INVOKE_a_RUNNING_MODAL')
            return {'RUNNING_MODAL'}
        else:
            print('05_run_NAV_INVOKE_a_FINISHED')
            return {'FINISHED'}     
    
# Changing the mode of operating and leaving start point at the first snap, continuing with just the end point:



class NPFPChangePhase(bpy.types.Operator):
    bl_idname = "object.np_fp_change_phase"
    bl_label = "NP FP Change Phase"
    bl_options={'INTERNAL'} 
        
    def execute(self, context):
        print('06_change_phase_START')
        Storage.phase=1
        print('Storage.phase=', Storage.phase)
        start=Storage.start
        end=Storage.end
        startloc3d = start.location      
        endloc3d = end.location
        Storage.startloc3d=startloc3d
        Storage.endloc3d=endloc3d
        bpy.ops.object.select_all(action='DESELECT')
        end.select=True     
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='ACTIVE_ELEMENT'
        bpy.context.space_data.transform_orientation='GLOBAL'
        Storage.flag = 'TRANSLATE'
        print('06_change_phase_END_flag_TRANSLATE')
        return {'FINISHED'}
      
# Changing the mode of operating and leaving start point at the first snap, continuing with just the end point:

class NPFPMakeSegment(bpy.types.Operator):
    bl_idname = "object.np_fp_make_segment"
    bl_label = "NP FP Make Segment"
    bl_options={'INTERNAL'} 
        
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__name__].preferences
        wire = addon_prefs.wire
        smooth = addon_prefs.smooth
        material = addon_prefs.material       
        
        flag = Storage.flag
        if flag == 'SURFACE':
            return {'FINISHED'}
        print('08_make_segment_START')
        print('Storage.phase =', Storage.phase)
        polyob = Storage.polyob
        start = Storage.start
        end = Storage.end
        startloc3d = start.location      
        endloc3d = end.location
        if Storage.phase < 2:
            polyverts = []
            polyverts.append(startloc3d)
            polyverts.append(endloc3d)
            polyedges = []
            polyedges.append((1,0))
            polyfaces = []
            polyme = bpy.data.meshes.new('float_poly')
            polyme.from_pydata(polyverts,polyedges,polyfaces)
            polyob = bpy.data.objects.new('float_poly',polyme)
            polyob.location = mathutils.Vector((0,0,0))
            scn = bpy.context.scene
            scn.objects.link(polyob)
            scn.objects.active = polyob
            scn.update()
            bpy.ops.object.select_all(action = 'DESELECT')
            polyob.select = True                
            bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
            if wire:
                polyob.show_wire = True
            if material:
                mtl=bpy.data.materials.new('float_poly_material')
                mtl.diffuse_color = (1.0, 1.0, 1.0)
                polyme.materials.append(mtl)
            activelayer = bpy.context.scene.active_layer
            print ('activelayer:', activelayer)
            layers = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
            layers[activelayer] = True
            layers = tuple(layers)
            print(layers)
            bpy.ops.object.move_to_layer(layers = layers)
            bpy.ops.object.select_all(action = 'DESELECT') 
            Storage.polyob = polyob
        else:
            polyme = polyob.data
            bm = bmesh.new()
            bm.from_mesh(polyme)            
            vco = endloc3d - polyob.location
            bmesh.ops.create_vert(bm, co = vco)
            i = len(bm.verts)
            bm.verts.ensure_lookup_table()
            if flag == 'CLOSE':
                verts = [bm.verts[i-1], bm.verts[0]]
                Storage.flag = 'SURFACE'
            else:
                verts = [bm.verts[i-1], bm.verts[i-2]]
            bmesh.ops.contextual_create(bm, geom = verts)
            bm.to_mesh(polyme)
            bm.free()
            bpy.ops.object.select_all(action = 'DESELECT')
            polyob.select = True                
            bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
            Storage.polyob = polyob
        bpy.context.scene.objects.active = polyob
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.context.scene.objects.active = end
        start.location = endloc3d
        end.location = endloc3d
        bpy.ops.object.select_all(action='DESELECT')
        end.select=True
        Storage.start = start
        Storage.end = end
        Storage.phase = 2
        Storage.selob = polyob
        Storage.acob = polyob
        bpy.context.tool_settings.use_snap=False
        bpy.context.tool_settings.snap_element='VERTEX'
        bpy.context.tool_settings.snap_target='ACTIVE'
        bpy.context.space_data.pivot_point='MEDIAN_POINT'
        bpy.context.space_data.transform_orientation='GLOBAL'
        if flag not in {'CLOSE', 'SURFACE'}:
            Storage.flag = 'TRANSLATE'
        print('08_make_segment_END_flag_TRANSLATE')
        return {'FINISHED'}      


# Deleting the anchors after succesfull translation and reselecting previously selected objects:

class NPFPDeletePoints(bpy.types.Operator):
    bl_idname = "object.np_fp_delete_points"
    bl_label = "NP FP Delete Points"
    bl_options={'INTERNAL'}
        
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__name__].preferences
        dist = Storage.dist
        polyob = Storage.polyob
        print('07_delete_points_START')
      
        selob=Storage.selob
        start=Storage.start
        end=Storage.end
        bpy.ops.object.select_all(action='DESELECT')
        start.hide = False
        end.hide = False
        start.select = True
        end.select = True
        bpy.ops.object.delete('EXEC_DEFAULT')
        if selob is not polyob:
            for ob in selob:
                ob.select=True
        else:
            polyob.select = True
        Storage.startloc3d=(0.0,0.0,0.0)
        Storage.endloc3d=(0.0,0.0,0.0)
        Storage.phase = 0
        Storage.flag = 'SURFACE'
        Storage.start = None
        Storage.end = None
        Storage.dist = None
        Storage.polyverts = []
        Storage.polyedges = []
        bpy.context.tool_settings.use_snap=Storage.use_snap
        bpy.context.tool_settings.snap_element=Storage.snap_element
        bpy.context.tool_settings.snap_target=Storage.snap_target
        bpy.context.space_data.pivot_point=Storage.pivot_point
        bpy.context.space_data.transform_orientation=Storage.trans_orient
        if Storage.acob is not None:
            bpy.context.scene.objects.active=Storage.acob
            bpy.ops.object.mode_set(mode = Storage.edit_mode)
        return {'FINISHED'}

     
# Creating a surface on the closed polyline:

class NPFPMakeSurface(bpy.types.Operator):
    bl_idname = "object.np_fp_make_surface"
    bl_label = "NP FP Make Surface"
    bl_options={'INTERNAL'}
        
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__name__].preferences
        smooth = addon_prefs.smooth
        dist = Storage.dist     
        polyob = Storage.polyob
        polyme = polyob.data
        bm = bmesh.new()
        bm.from_mesh(polyme)
        bmesh.ops.contextual_create(bm, geom = bm.edges)
        bm.to_mesh(polyme)
        bm.free()
        bpy.ops.object.select_all(action='DESELECT')
        polyob.select = True
        if smooth:
            bpy.ops.object.shade_smooth()
            print('smooth ON')
        bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')            
        bpy.ops.object.select_all(action='DESELECT')        
        Storage.flag = 'EXTRUDE'
        Storage.phase = 3
        return {'FINISHED'}

def draw_callback_px_NAVEX(self, context):
    
    print('08_callback_NAVEX_START')
    
    addon_prefs = context.user_preferences.addons[__name__].preferences

    scale = addon_prefs.scale
    badge = addon_prefs.badge
    point_size = addon_prefs.point_size
    badge_size = addon_prefs.badge_size
    
    polyob = Storage.polyob
    phase = Storage.phase
    region = context.region
    rv3d = context.region_data    
    co2d = self.co2d

    
    if addon_prefs.col_line_main_DEF == False:
        col_line_main = addon_prefs.col_line_main
    else:
        col_line_main = (1.0, 1.0, 1.0, 1.0) 

    if addon_prefs.col_line_shadow_DEF == False:
        col_line_shadow = addon_prefs.col_line_shadow
    else:
        col_line_shadow = (0.1, 0.1, 0.1, 0.25)
    
    if addon_prefs.col_num_main_DEF == False:
        col_num_main = addon_prefs.col_num_main
    else:
        col_num_main = (0.1, 0.1, 0.1, 0.75) 
    
    if addon_prefs.col_num_shadow_DEF == False:
        col_num_shadow = addon_prefs.col_num_shadow
    else:
        col_num_shadow = (1.0, 1.0, 1.0, 1.0)
        
    if addon_prefs.point_color_DEF == False:
        col_pointromb = addon_prefs.point_color
    else:
        col_pointromb = (0.3, 0.3, 0.3, 1.0)         

    if addon_prefs.suffix == 'None':
        suffix=None

    elif addon_prefs.suffix == 'km':
        suffix=' km'
        
    elif addon_prefs.suffix == 'm':
        suffix=' m'
        
    elif addon_prefs.suffix == 'cm':
        suffix=' cm'
        
    elif addon_prefs.suffix == 'mm':
        suffix=' mm'
        
    elif addon_prefs.suffix == 'nm':
        suffix=' nm'
        
    elif addon_prefs.suffix == "'":
        suffix="'"
        
    elif addon_prefs.suffix == '"':
        suffix='"'
        
    elif addon_prefs.suffix == 'thou':
        suffix=' thou'
        
    # Calculating the 3d points for the graphical line while in NAVIGATE flag:
   
    """
    
    print('phase=', phase)
    if phase == 0 or phase == 3:
        startloc3d=(0.0,0.0,0.0)
        endloc3d=(0.0,0.0,0.0)    
    
    if phase == 1:
        startloc3d = Storage.startloc3d
        endloc3d = pointloc
        
    if phase == 2:
        startloc3d = Storage.startloc3d
        endloc3d = pointloc   
    """
    # Calculating the 2D points for the graphical line while in NAVIGATE flag from 3D points:
    """    
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    
    if startloc2d == None:
        startloc2d=(0.0,0.0)
        endloc2d=(0.0,0.0)
    print(startloc2d, endloc2d)
    
    dist = (mathutils.Vector(endloc3d) - mathutils.Vector(startloc3d))
    dist = dist.length*scale
    print(dist)
    
    if suffix is not None:
        dist = str(abs(round(dist,2)))+suffix
    else:
        dist = str(abs(round(dist,2)))
        
    Storage.dist = dist
    print(dist)
    
    #This is for correcting the position of the numerical on the screen if the endpoints are far out of screen:    
    numloc = []
    startx=startloc2d[0]
    starty=startloc2d[1]
    endx=endloc2d[0]
    endy=endloc2d[1]
    if startx > region.width:
        startx = region.width
    if startx < 0:
        startx = 0
    if starty > region.height:
        starty = region.height
    if starty < 0:
        starty = 0        
    if endx > region.width:
        endx = region.width
    if endx < 0:
        endx = 0
    if endy > region.height:
        endy = region.height
    if endy < 0:
        endy = 0        
    numloc.append((startx+endx)/2)
    numloc.append((starty+endy)/2)    
    
    if phase==0:
        main='NAVIGATE FOR BETTER PLACEMENT OF START POINT'
        
    if phase==1:
        main='NAVIGATE FOR BETTER PLACEMENT OF NEXT POINT' 
        
    if phase==2:
        main='NAVIGATE FOR BETTER PLACEMENT OF NEXT POINT'
        
    if phase==3:
        main='NAVIGATE FOR BETTER PLACEMENT OF EXTRUSION HEIGHT'        
                

    #Drawing:
           
    bgl.glEnable(bgl.GL_BLEND)
    
    #LINE:
    
    bgl.glColor4f(*col_line_shadow)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f((startloc2d[0]-1),(startloc2d[1]-1))
    bgl.glVertex2f((endloc2d[0]-1),(endloc2d[1]-1))
    bgl.glEnd()
    
    bgl.glColor4f(*col_line_main)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f(*startloc2d)
    bgl.glVertex2f(*endloc2d)
    bgl.glEnd() 
    
    #POINT MARKERS:
    markersize = point_size
    triangle = [[0, 0], [-1, 1], [1, 1]]    
    romb = [[-1, 0], [0, 1], [1, 0], [0, -1]]    
    if phase > 0 and polyob is None:
        polylist2d = []
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + startloc2d[0]
            co[1] = round((co[1] * markersize * 3),0) + startloc2d[1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for co in pointromb:    
            co[0] = round((co[0] * markersize),0) + endloc2d[0]
            co[1] = round((co[1] * markersize),0) + endloc2d[1]
        if phase == 2:
            print ('pointromb', pointromb)
            bgl.glColor4f(*col_pointromb)
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            for x,y in pointromb:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
    if polyob is not None:
        print ('polyob not None')
        polyloc = polyob.location
        polyme = polyob.data
        polylist3d = []
        for me in polyme.vertices:
            polylist3d.append(me.co + polyloc)
        print ('polylist3d = ', polylist3d)
        polylist2d = []
        for p3d in polylist3d:
            p2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p3d)
            polylist2d.append(p2d)
        print ('polylist2d = ', polylist2d)
        #triangle for the first point
        for co in triangle:    
            co[0] = round((co[0] * markersize * 3),0) + polylist2d[0][0]
            co[1] = round((co[1] * markersize * 3),0) + polylist2d[0][1]
        print('triangle', triangle)
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in triangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        #rombs for the other points
        i = 0
        for p2d in polylist2d:
            if i > 0:
                pointromb = [[-1, 0], [0, 1], [1, 0], [0, -1]]
                for co in pointromb:    
                    co[0] = round((co[0] * markersize),0) + p2d[0]
                    co[1] = round((co[1] * markersize),0) + p2d[1]
                print ('pointromb', pointromb)
                bgl.glColor4f(*col_pointromb)
                bgl.glBegin(bgl.GL_TRIANGLE_FAN)
                for x,y in pointromb:
                    bgl.glVertex2f(x,y)
            i = i + 1
            bgl.glEnd()
            
    #NUMERICAL DISTANCE:
    
    bgl.glColor4f(*col_num_shadow) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, (numloc[0]-1), (numloc[1]-1), 0)
        blf.draw(font_id, dist)
        
    bgl.glColor4f(*col_num_main) 
    if phase > 0:
        font_id = 0
        blf.size(font_id, 20, 72)
        blf.position(font_id, numloc[0], numloc[1], 0)
        blf.draw(font_id, dist)        
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)           
    """   
    #ON-SCREEN INSTRUCTIONS:
    
    main='NAVIGATE FOR BETTER PLACEMENT OF EXTRUSION HEIGHT'
    
    font_id = 0
    
    bgl.glColor4f(1,1,1,0.35)
    blf.size(font_id,88,72)
    blf.position(font_id,5,74,0)
    blf.draw(font_id,'N')
    blf.size(font_id,28,72)    
    blf.position(font_id,22,74,0)
    blf.draw(font_id,'P')
    
    blf.enable(font_id, ROTATION)
    bgl.glColor4f(1,1,1,0.40)    
    ang = radians(90)
    blf.size(font_id,19,72)
    blf.rotation(font_id,ang)
    blf.position(font_id,78,73,0)
    blf.draw(font_id,'FP 001')
    blf.disable(font_id, ROTATION)
    
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    blf.position(font_id,93,124,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(1,1,1,1)
    blf.position(font_id,94,125,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(0,0.5,0,1)
    blf.size(font_id,11,72)
    blf.position(font_id,93,105,0)
    blf.draw(font_id,'MMB, SCROLL - navigate')
    blf.position(font_id,93,90,0)
    blf.draw(font_id,'LMB, SPACE - leave navigate')
    
    #blf.position(font_id,75,75,0)
    #blf.draw(font_id,'NUMPAD - value')
    
    bgl.glColor4f(1,0,0,1)
    blf.position(font_id,93,75,0)
    blf.draw(font_id,'ESC, RMB - quit')
    
    # Drawing the small badge near the cursor with the basic instructions:

    if badge == True:
        square = [[17, 30], [17, 40], [27, 40], [27, 30]]
        rectangle = [[27, 30], [27, 40], [67, 40], [67, 30]]        
        flash = copy.deepcopy(Storage.flash)
        ipx = 29
        ipy = 33
        size = badge_size
        for co in square:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]
        for co in rectangle:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]
        for co in flash:    
            co[0] = round((co[0] * size),0) -(size*10) + co2d[0]
            co[1] = round((co[1] * size),0) -(size*25) + co2d[1]

        ipx = round((ipx * size),0) -(size*10) + co2d[0]
        ipy = round((ipy * size),0) -(size*25) + co2d[1]
        ipsize = int(6* size)
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in square:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(0.5, 0.75, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in rectangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINE_STRIP) 
        for x,y in flash:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(font_id,ipx,ipy,0)
        blf.size(font_id,ipsize,72)
        blf.draw(font_id,'NAVIGATE')
          
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)    
    print('05_callback_NAVEX_END')

# Defining the operator that will draw the OpenGL the numerical distance and the on-screen instructions while the user extrudes the surface:

class NPFPRunNavEx(bpy.types.Operator):
    bl_idname = "object.np_fp_run_navex"
    bl_label = "NP FP Run NavEx"
    bl_options={'INTERNAL'}
    
    
    def modal(self, context, event):
        print('05_run_NAVEX_START')
        context.area.tag_redraw()
        selob=Storage.selob
        phase=Storage.phase
        
        if event.type == 'MOUSEMOVE':
            print('05_run_NAVEX_mousemove_a')
            self.co2d = ((event.mouse_region_x, event.mouse_region_y))
            print('05_run_NAVEX_mousemove_b')
            
        elif event.type in {'LEFTMOUSE', 'SPACE'} and event.value == 'PRESS':
            print('05_run_NAVEX_left_space_press_START')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            self.co2d = ((event.mouse_region_x, event.mouse_region_y))  
            region = context.region
            rv3d = context.region_data
            co2d = self.co2d
            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d) 
            pointloc = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d) + view_vector/5          
            print('phase=', phase)
            Storage.flag = 'EXTRUDE'
            print('05_run_NAVEX_left_space_press_FINISHED_flag_TRANSLATE')
            return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            print('05_run_NAVEX_esc_right_any_START')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('05_run_NAVEX_esc_right_any_CANCELLED')
            return{'CANCELLED'}

        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            print('05_run_NAVEX_middle_any_PASS_THROUGH')
            return {'PASS_THROUGH'}
	  
        print('05_run_NAVEX_RUNNING_MODAL')
        return {'RUNNING_MODAL'}    

    def invoke(self, context, event):
        print('05_run_NAVEX_a')
        flag = Storage.flag
        print('flag=', flag)
        self.co2d = ((event.mouse_region_x, event.mouse_region_y))
        if flag == 'NAVEX':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px_NAVEX, args, 'WINDOW', 'POST_PIXEL')      
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            print('05_run_NAVEX_INVOKE_a_FINISHED')
            return {'FINISHED'}

def draw_callback_px_EXTRUDE(self, context):
    
    print('10_callback_EXTRUDE_START')
    
    
    addon_prefs = context.user_preferences.addons[__name__].preferences
    scale = addon_prefs.scale
    badge = addon_prefs.badge
    point_size = addon_prefs.point_size
    badge_size = addon_prefs.badge_size    

    
    if addon_prefs.col_line_main_DEF == False:
        col_line_main = addon_prefs.col_line_main
    else:
        col_line_main = (1.0, 1.0, 1.0, 1.0) 

    if addon_prefs.col_line_shadow_DEF == False:
        col_line_shadow = addon_prefs.col_line_shadow
    else:
        col_line_shadow = (0.1, 0.1, 0.1, 0.25)
    
    if addon_prefs.col_num_main_DEF == False:
        col_num_main = addon_prefs.col_num_main
    else:
        col_num_main = (0.1, 0.1, 0.1, 0.75) 
    
    if addon_prefs.col_num_shadow_DEF == False:
        col_num_shadow = addon_prefs.col_num_shadow
    else:
        col_num_shadow = (1.0, 1.0, 1.0, 1.0)

    if addon_prefs.point_color_DEF == False:
        col_pointromb = addon_prefs.point_color
    else:
        col_pointromb = (0.3, 0.3, 0.3, 1.0) 
        
    if addon_prefs.suffix == 'None':
        suffix=None

    elif addon_prefs.suffix == 'km':
        suffix=' km'
        
    elif addon_prefs.suffix == 'm':
        suffix=' m'
        
    elif addon_prefs.suffix == 'cm':
        suffix=' cm'
        
    elif addon_prefs.suffix == 'mm':
        suffix=' mm'
        
    elif addon_prefs.suffix == 'nm':
        suffix=' nm'
        
    elif addon_prefs.suffix == "'":
        suffix="'"
        
    elif addon_prefs.suffix == '"':
        suffix='"'
        
    elif addon_prefs.suffix == 'thou':
        suffix=' thou'           
    #print('0')
    #sel=bpy.context.selected_objects
    flag = Storage.flag
    polyob = Storage.polyob
    polyme = polyob.data
    i = len(polyme.vertices)
    print('extrude_callback')
    print('i', i)
    j = i / 2
    j = int(j)
    print(i,j)
    print(polyme.vertices[0].co)
    startloc3d = polyme.vertices[0].co
    endloc3d = polyme.vertices[j].co
    print('Ss3d, Se3d', startloc3d, endloc3d)
    region = context.region
    rv3d = context.region_data
    startloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, startloc3d)
    endloc2d = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    print(startloc2d, endloc2d)
    #print('1')
    
    dist = (mathutils.Vector(endloc3d) - mathutils.Vector(startloc3d))
    dist = dist.length*scale
    print('dist =', dist)
    if suffix is not None:
        dist = str(abs(round(dist,2)))+suffix
    else:
        dist = str(abs(round(dist,2)))
    print('dist =', dist)
    Storage.dist = dist
    #print('2')
    #This is for correcting the position of the numerical on the screen if the endpoints are far out of screen:    
    numloc = []
    startx = startloc2d[0]
    starty = startloc2d[1]
    endx = endloc2d[0]
    endy = endloc2d[1]
    if startx > region.width:
        startx = region.width
    if startx < 0:
        startx = 0
    if starty > region.height:
        starty = region.height
    if starty < 0:
        starty = 0        
    if endx > region.width:
        endx = region.width
    if endx < 0:
        endx = 0
    if endy > region.height:
        endy = region.height
    if endy < 0:
        endy = 0        
    numloc.append((startx+endx)/2)
    numloc.append((starty+endy)/2) 
    #print('3')
    
    if flag == 'BEVEL':
        main = 'SPECIFY BEVEL AMOUNT'
    else:
        main = 'SPECIFY EXTRUSION HEIGHT'          
    #Drawing:
    """     
    bgl.glEnable(bgl.GL_BLEND)
    
    #LINE:
    
    bgl.glColor4f(*col_line_shadow)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f((startloc2d[0]-1),(startloc2d[1]-1))
    bgl.glVertex2f((endloc2d[0]-1),(endloc2d[1]-1))
    bgl.glEnd()
    
    bgl.glColor4f(*col_line_main)
    bgl.glLineWidth(1.4)    
    bgl.glBegin(bgl.GL_LINE_STRIP) 
    bgl.glVertex2f(*startloc2d)
    bgl.glVertex2f(*endloc2d)
    bgl.glEnd()    
    #print('4')
    #NUMERICAL DISTANCE:
    
    print('numloc = ' ,numloc, 'dist = ', dist)
    
    bgl.glColor4f(*col_num_shadow) 
    font_id = 0
    blf.size(font_id, 20, 72)
    blf.position(font_id, (numloc[0]-1), (numloc[1]-1), 0)
    blf.draw(font_id, dist)
        
    bgl.glColor4f(*col_num_main) 
    font_id = 0
    blf.size(font_id, 20, 72)
    blf.position(font_id, numloc[0], numloc[1], 0)
    blf.draw(font_id, dist)        
            
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0) 
    
    """
    #print('5')
    #ON-SCREEN INSTRUCTIONS:
    
    font_id=0
    
    bgl.glColor4f(1,1,1,0.35)
    blf.size(font_id,88,72)
    blf.position(font_id,5,74,0)
    blf.draw(font_id,'N')
    blf.size(font_id,28,72)    
    blf.position(font_id,22,74,0)
    blf.draw(font_id,'P')
    
    blf.enable(font_id, ROTATION)
    bgl.glColor4f(1,1,1,0.40)    
    ang = radians(90)
    blf.size(font_id,19,72)
    blf.rotation(font_id,ang)
    blf.position(font_id,78,73,0)
    blf.draw(font_id,'FP 001')
    blf.disable(font_id, ROTATION)
    
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    blf.position(font_id,93,124,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(1,1,1,1)
    blf.position(font_id,94,125,0)
    blf.size(font_id,16,72)
    blf.draw(font_id,main)
    
    bgl.glColor4f(0,0.5,0,1)
    blf.size(font_id,11,72)
    if flag == 'BEVEL':
        blf.position(font_id,93,105,0)
        blf.draw(font_id,'LMB, ENTER - confirm, SCROLL - number of segments')
        blf.position(font_id,93,90,0)
        blf.draw(font_id,'M - mode, C - clamp overlap')
        #print('6')
        blf.position(font_id,93,75,0)
        blf.draw(font_id,'NUMPAD - value')
        bgl.glColor4f(1,0,0,1)
        blf.position(font_id,93,60,0)
        blf.draw(font_id,'ESC, RMB - cancel bevel')        
    else:
        blf.position(font_id,93,105,0)
        blf.draw(font_id,'CTRL - snap, LMB - confirm, ENTER - confirm without bevel, MMB - lock axis')
        blf.position(font_id,93,90,0)
        blf.draw(font_id,'SPACE - change to navigate')
        #print('6')
        blf.position(font_id,93,75,0)
        blf.draw(font_id,'NUMPAD - value')
        bgl.glColor4f(1,0,0,1)
        blf.position(font_id,93,60,0)
        blf.draw(font_id,'ESC, RMB - cancel extrusion')    


    # Drawing the small badge near the cursor with the basic instructions:
    mouseloc = view3d_utils.location_3d_to_region_2d(region, rv3d, endloc3d)
    #print(end, endloc, mouseloc)
    """
    if badge == True:
        square = [[17, 30], [17, 40], [27, 40], [27, 30]]
        rectangle = [[27, 30], [27, 40], [67, 40], [67, 30]]
        flash = copy.deepcopy(Storage.flash)     
        size = 2
        ipx = 29
        ipy = 33
        size = badge_size        
        for co in square:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]
        for co in rectangle:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]
        for co in flash:    
            co[0] = round((co[0] * size),0) -(size*10) + mouseloc[0]
            co[1] = round((co[1] * size),0) -(size*25) + mouseloc[1]
        ipx = round((ipx * size),0) -(size*10) + mouseloc[0]
        ipy = round((ipy * size),0) -(size*25) + mouseloc[1]
        ipsize = int(6*size)            
        bgl.glColor4f(0.0, 0.0, 0.0, 0.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in square:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 0.5, 0.0, 1.0)
        bgl.glBegin(bgl.GL_TRIANGLE_FAN)
        for x,y in rectangle:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        bgl.glBegin(bgl.GL_LINE_STRIP) 
        for x,y in flash:
            bgl.glVertex2f(x,y)
        bgl.glEnd()
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(font_id,ipx,ipy,0)
        blf.size(font_id,ipsize,72)
        blf.draw(font_id,'CTRL+SNAP')
           
    """       
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    #print('7')
    print('10_callback_EXTRUDE_END')
    
    

class NPFPRunExtrude(bpy.types.Operator):
    bl_idname='object.np_fp_run_extrude'
    bl_label='NP FP Run Extrude'
    bl_options={'INTERNAL'}

    print('10_run_EXTRUDE_START')
    count=0
       
    def modal(self,context,event):
        context.area.tag_redraw()        
        self.count+=1
        selob = Storage.selob
        flag = Storage.flag
        polyob = Storage.polyob
        phase = Storage.phase
        
        if self.count == 1:
            
            if phase == 3:
                bpy.ops.view3d.edit_mesh_extrude_move_normal('INVOKE_DEFAULT')
            else:
                bpy.ops.transform.translate('INVOKE_DEFAULT',constraint_axis=(False, False, True), constraint_orientation='NORMAL')

            print('B')
            print('10_run_EXTRUDE_count_1_INVOKE_DEFAULT')
                     
        elif event.type in ('LEFTMOUSE','NUMPAD_ENTER') and event.value == 'RELEASE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            polyob.select = True
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)           
            bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')            
            polyob.select = False
            bpy.ops.object.mode_set(mode = 'EDIT')
            Storage.flag = 'BEVEL'
            print('10_run_EXTRUDE_left_release_FINISHED')
            return{'FINISHED'}

        elif event.type == 'SPACE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            Storage.phase = 3.5
            Storage.flag = 'NAVEX'
            print('10_run_TRANS_space_FINISHED_flag_NAVIGATE')
            return{'FINISHED'}

        elif event.type == 'RET':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            polyob.select = True
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)           
            bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')            
            bpy.ops.object.select_all(action='DESELECT')            
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('10_run_EXTRUDE_space_FINISHED_flag_TRANSLATE')
            return{'FINISHED'}       
  
        elif event.type in ('ESC', 'RIGHTMOUSE'):
        #this actually begins when user RELEASES esc or rightmouse, PRESS is taken by transform.translate operator        
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')            
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('10_run_EXTRUDE_space_CANCELLED_flag_TRANSLATE')
            return{'CANCELLED'}
  
        print('10_run_EXTRUDE_PASS_THROUGH')
        return{'PASS_THROUGH'}

    def invoke(self, context, event):
        print('10_run_EXTRUDE_INVOKE_a')

        selob = Storage.selob
        flag = Storage.flag
        print('flag = ', flag)
        polyob = Storage.polyob

        
        if flag == 'EXTRUDE':
            if context.area.type == 'VIEW_3D':
                if bpy.context.mode == 'OBJECT':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.scene.objects.active = polyob
                    polyob.select = True        
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    polyme = polyob.data
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    i = len(polyme.vertices) 
                    i = int(i / 2)
                    Storage.startloc3d = polyme.vertices[0].co
                    Storage.startloc3d = polyme.vertices[i].co
                if bpy.context.mode == 'EDIT':
                    polyme = polyob.data
                    i = len(polyme.vertices) 
                    i = int(i / 2)
                    Storage.startloc3d = polyme.vertices[0].co
                    Storage.startloc3d = polyme.vertices[i].co                
                args = (self, context)
                self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px_EXTRUDE, args, 'WINDOW', 'POST_PIXEL')      
                context.window_manager.modal_handler_add(self)
                
                print('10_run_EXTRUDE_INVOKE_a_RUNNING_MODAL')
                return {'RUNNING_MODAL'}
            else:
                self.report({'WARNING'}, "View3D not found, cannot run operator")
                print('10_run_EXTRUDE_INVOKE_a_CANCELLED')
                return {'CANCELLED'}
        else:
            print('10_run_EXTRUDE_INVOKE_a_FINISHED')
            return {'FINISHED'}

class NPFPRunBevel(bpy.types.Operator):
    bl_idname='object.np_fp_run_bevel'
    bl_label='NP FP Run Bevel'
    bl_options={'INTERNAL'}

    print('11_run_BEVEL_START')
    count=0
       
    def modal(self,context,event):
        context.area.tag_redraw()        
        self.count+=1
        selob = Storage.selob
        flag = Storage.flag
        polyob = Storage.polyob
        
        
        if self.count == 1:

            bpy.ops.mesh.bevel('INVOKE_DEFAULT')

            print('B')
            print('11_run_BEVEL_count_1_INVOKE_DEFAULT')
                     
        elif event.type in ('LEFTMOUSE','RET','NUMPAD_ENTER', 'SPACE') and event.value == 'RELEASE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            Storage.flag = 'TRANSLATE'
            bpy.ops.object.select_all(action='DESELECT')
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None   
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('10_run_EXTRUDE_left_release_FINISHED')
            return{'FINISHED'}     
  
        elif event.type in ('RIGHTMOUSE','ESC'):
        #this actually begins when user RELEASES esc or rightmouse, PRESS is taken by transform.translate operator        
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT') 
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)
            print('11_run_BEVEL_esc_CANCELLED')
            return{'CANCELLED'}
  
        print('11_run_BEVEL_PASS_THROUGH')
        return{'PASS_THROUGH'}

    def invoke(self, context, event):
        print('11_run_BEVEL_INVOKE_a')
        addon_prefs = context.user_preferences.addons[__name__].preferences
        bevel = addon_prefs.bevel
        selob = Storage.selob
        flag = Storage.flag
        print('flag = ', flag)
        polyob = Storage.polyob

        
        if flag == 'BEVEL' and bevel:
            if context.area.type == 'VIEW_3D':
                bpy.context.scene.objects.active = polyob       
                bpy.ops.mesh.select_all(action = 'SELECT')
                args = (self, context)
                Storage.main_BEVEL = 'DESIGNATE BEVEL AMOUNT'
                self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px_EXTRUDE, args, 'WINDOW', 'POST_PIXEL')      
                context.window_manager.modal_handler_add(self)                
                print('11_run_BEVEL_INVOKE_a_RUNNING_MODAL')
                return {'RUNNING_MODAL'}

            else:
                self.report({'WARNING'}, "View3D not found, cannot run operator")
                print('11_run_BEVEL_INVOKE_a_CANCELLED')
                return {'CANCELLED'}
        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            if selob is not polyob:
                for ob in selob:
                    ob.select=True
            else:
                polyob.select = True
            Storage.startloc3d=(0.0,0.0,0.0)
            Storage.endloc3d=(0.0,0.0,0.0)
            Storage.phase=0
            Storage.start = None
            Storage.end = None
            Storage.dist = None
            Storage.polyob = None            
            Storage.flag='TRANSLATE'
            bpy.context.tool_settings.use_snap=Storage.use_snap
            bpy.context.tool_settings.snap_element=Storage.snap_element
            bpy.context.tool_settings.snap_target=Storage.snap_target
            bpy.context.space_data.pivot_point=Storage.pivot_point
            bpy.context.space_data.transform_orientation=Storage.trans_orient
            if Storage.acob is not None:
                bpy.context.scene.objects.active=Storage.acob
                bpy.ops.object.mode_set(mode = Storage.edit_mode)           
            print('11_run_BEVEL_INVOKE_a_FINISHED')
            return {'FINISHED'}


class ArchiPanel(bpy.types.Panel):
    bl_label = "Architectural Infos"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"

    def draw(self, context):
     
        dist = Storage.dist
        dist = str(dist)
        info = "Last distance: "+ dist
        layout = self.layout
        row = layout.row(align = True)
        row.label(info)
        row = layout.row()
        row.operator("object.np_float_poly_001", icon='IPO_CONSTANT', text='float_poly')
      
# Defining the settings part in the addons tab:
      
class NPFPPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__
      
    scale = bpy.props.FloatProperty(
            name='Unit scale',
            description='Distance multiplier (for example, for cm use 100)',
            default=100,
            min=0,
            step=1,
            precision=3)
    
    suffix = bpy.props.EnumProperty(
        name='Unit suffix',
        items=(("'","'",''), ('"','"',''), ('thou','thou',''), ('km','km',''), ('m','m',''), ('cm','cm',''), ('mm','mm',''), ('nm','nm',''), ('None','None','')),       
        default='cm',
        description='Add a unit extension after the numerical distance ')
    
    badge = bpy.props.BoolProperty(
            name='Mouse badge',
            description='Use the graphical badge near the mouse cursor',
            default=True)
    
    badge_size = bpy.props.FloatProperty(
            name='size',
            description='Size of the mouse badge, the default is 2.0',
            default=2,
            min=0.5,
            step=10,
            precision=1)    
    
    point_markers = bpy.props.BoolProperty(
            name='Point markers',
            description='Use the markers for the start and other points of the poly',
            default=True)

    point_size = bpy.props.FloatProperty(
            name='size',
            description='Size of the start and point markers, the default is 5.0',
            default=5,
            min=0.5,
            step=50,
            precision=1)
 
    point_color_DEF = bpy.props.BoolProperty(
            name='Default point COLOR',
            description='Use the default color for the point markers',
            default=True)  
    
    col_line_main_DEF = bpy.props.BoolProperty(
            name='Default',
            description='Use the default color',
            default=True)
    
    col_line_shadow_DEF = bpy.props.BoolProperty(
            name='Default',
            description='Use the default color',
            default=True)

    col_num_main_DEF = bpy.props.BoolProperty(
            name='Default',
            description='Use the default color',
            default=True)

    col_num_shadow_DEF = bpy.props.BoolProperty(
            name='Default',
            description='Use the default color',
            default=True)  
    
    wire = bpy.props.BoolProperty(
            name='Wire contour',
            description="Use the 'show wireframe' option over the object's solid drawing",
            default=True)

    smooth = bpy.props.BoolProperty(
            name='Smooth shading',
            description='Automaticaly turn on smooth shading for the poly object',
            default=False)

    material = bpy.props.BoolProperty(
            name='Base material',
            description='Automaticaly assign a base material to the poly object',
            default=True)
    
    bevel = bpy.props.BoolProperty(
            name='Bevel',
            description='Start the bevel operation after the extrusion',
            default=False)    
    
    point_color = bpy.props.FloatVectorProperty(name='', default=(0.3, 0.3, 0.3, 1.0), size=4, subtype="COLOR", min=0, max=1, description = 'Color of the point markers')

    col_line_main = bpy.props.FloatVectorProperty(name='', default=(1.0, 1.0, 1.0, 1.0), size=4, subtype="COLOR", min=0, max=1, description = 'Color of the measurement line, to disable it set alpha to 0.0')
    
    col_line_shadow = bpy.props.FloatVectorProperty(name='', default=(0.1, 0.1, 0.1, 0.25), size=4, subtype="COLOR", min=0, max=1, description = 'Color of the line shadow, to disable it set alpha to 0.0')
    
    col_num_main = bpy.props.FloatVectorProperty(name='', default=(0.1, 0.1, 0.1, 0.75), size=4, subtype="COLOR", min=0, max=1, description = 'Color of the number, to disable it set alpha to 0.0')
    
    col_num_shadow = bpy.props.FloatVectorProperty(name='', default=(1.0, 1.0, 1.0, 1.0), size=4, subtype="COLOR", min=0, max=1, description = 'Color of the number shadow, to disable it set alpha to 0.0')
    
    def draw(self, context):
        layout = self.layout
        split = layout.split()
        col = split.column()       
        col.prop(self, "scale")        
        col = split.column()      
        col.prop(self, "suffix")
        split = layout.split()        
        col = split.column()
        col.label(text='Line Main COLOR')
        col.prop(self, "col_line_main_DEF")
        if self.col_line_main_DEF == False:
            col.prop(self, "col_line_main")
        col = split.column()
        col.label(text='Line Shadow COLOR')
        col.prop(self, "col_line_shadow_DEF")
        if self.col_line_shadow_DEF == False:        
            col.prop(self, "col_line_shadow")
        col = split.column()
        col.label(text='Numerical Main COLOR')
        col.prop(self, "col_num_main_DEF")
        if self.col_num_main_DEF == False:        
            col.prop(self, "col_num_main")
        col = split.column()
        col.label(text='Numerical Shadow COLOR')
        col.prop(self, "col_num_shadow_DEF")
        if self.col_num_shadow_DEF == False:        
            col.prop(self, "col_num_shadow")
        split = layout.split()
        col = split.column()       
        col.prop(self, "badge")
        col = split.column()       
        if self.badge == True:
            col.prop(self, "badge_size")
        col = split.column()
        col = split.column()
        split = layout.split()
        col = split.column()       
        col.prop(self, "point_markers")
        col = split.column()       
        if self.point_markers == True:
            col.prop(self, "point_size")
        col = split.column()
        col.prop(self, "point_color_DEF")
        col = split.column() 
        if self.point_color_DEF == False:        
            col.prop(self, "point_color")                          
        split = layout.split()
        col = split.column()       
        col.prop(self, "bevel")
        col = split.column()       
        col.prop(self, "material")
        col = split.column()       
        col.prop(self, "smooth")
        col = split.column()
        col.prop(self, "wire")

                    
        
    
# This is the actual addon process, the algorithm that defines the order of operator activation inside the main macro:

def register():
  
    bpy.utils.register_class(NPFPPreferences)
    bpy.utils.register_class(ArchiPanel)
    bpy.utils.register_module(__name__)
    bpy.app.handlers.scene_update_post.append(scene_update)    
    
    
    NPFloatPoly001.define('OBJECT_OT_np_fp_get_selection')
    NPFloatPoly001.define('OBJECT_OT_np_fp_read_mouse_loc')
    NPFloatPoly001.define('OBJECT_OT_np_fp_add_points')
    for i in range(1, 10):
        NPFloatPoly001.define('OBJECT_OT_np_fp_run_translate')
        NPFloatPoly001.define('OBJECT_OT_np_fp_run_navigate')       
    NPFloatPoly001.define('OBJECT_OT_np_fp_change_phase')
    for i in range(1, 50):
        for i in range(1, 10):
            NPFloatPoly001.define('OBJECT_OT_np_fp_run_translate')
            NPFloatPoly001.define('OBJECT_OT_np_fp_run_navigate')
        NPFloatPoly001.define('OBJECT_OT_np_fp_make_segment')        
    NPFloatPoly001.define('OBJECT_OT_np_fp_delete_points')  
    NPFloatPoly001.define('OBJECT_OT_np_fp_make_surface')
    for i in range(1, 10):
        NPFloatPoly001.define('OBJECT_OT_np_fp_run_extrude')
        NPFloatPoly001.define('OBJECT_OT_np_fp_run_navex')    
    NPFloatPoly001.define('OBJECT_OT_np_fp_run_bevel')
    
def unregister():

    bpy.utils.unregister_class(NPFPPreferences)
    bpy.utils.unregister_class(ArchiPanel)
    bpy.utils.unregister_module(__name__)
    #bpy.app.handlers.scene_update_post.remove(scene_update)       

    
if __name__ == "__main__":
    __name__ = "NP_float_poly_001"
    register()