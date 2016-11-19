 ##### BEGIN GPL LICENSE BLOCK #####
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
    "name": "Branch Extrusion",
    "author": "Rebellion",
    "version": (1, 4, 5),
    "blender": (2, 6, 5),
    "location": "View3D > Object_Edit > Mesh Tools ",
    "description": "Extrude and Resize the face",
    "warning": "",
    "wiki_url": "http://blenderartists.org/forum/showthread.php?248664-Branch-Extrusion",
    "tracker_url": "http://blenderartists.org/forum/showthread.php?248664-Branch-Extrusion",
    "category": "Mesh"}


#set the next face to the set distance (min distance)
#set the taper value = difference between the first and next face


import bpy, mathutils, math
import bmesh
from bpy.props import IntProperty, FloatProperty
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_location_3d,location_3d_to_region_2d



def extrusion(loc,face_center,taper_value, cons_x,cons_y,cons_z,orientation):
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    
    
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(loc), "constraint_axis":(cons_x, cons_y, cons_z), "constraint_orientation": orientation})
    bpy.ops.transform.translate(value =(-face_center ))         
    bpy.ops.transform.resize(value = (taper_value, taper_value, taper_value)) 
    
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

class BranchExtrusionOperator(bpy.types.Operator):
    
  
    bl_idname = "object.branch_extrusion"
    bl_label = "Branch Extrusion"
    bl_options = {'REGISTER', 'UNDO'}
    
    bpy.types.Scene.min_distance = FloatProperty(name='Min Distance', min=0,  soft_min=0, \
        soft_max=20, default= 5, description='Minimun distance from a face to another')
    
    bpy.types.Scene.taper_value = bpy.props.FloatProperty(name= 'Taper Value', min=0, max=999, soft_min=0.001, \
        soft_max=2, default= 0.5, description='Difference in size from a face to another')
    
    bpy.types.Scene.cons_x = bpy.props.BoolProperty(name= 'X Axis', default = False)
    bpy.types.Scene.cons_y = bpy.props.BoolProperty(name= 'Y Axis', default = False)
    bpy.types.Scene.cons_z = bpy.props.BoolProperty(name= 'Z Axis', default = False)
    bpy.types.Scene.orientation = bpy.props.EnumProperty(items = [( 'GLOBAL','Global','Global'), ('LOCAL','Local','Local'), ('NORMAL','Normal','Normal')],name = "")
    bpy.types.Scene.collapse = bpy.props.BoolProperty(name="Collapse", description="End branches with one vertex", default=True)
    bpy.types.Scene.auto_rotate = bpy.props.BoolProperty(name="Auto Rotate", description="Rotate face giving better shape", default=True)
    bpy.types.Scene.spin = bpy.types.Scene.spin = bpy.props.FloatProperty(name= 'Spin', min=0, max=360, soft_min=0, \
        soft_max=360, default= 0, description='Spin value in degree')
           
    bpy.types.Scene.stepsCounter = bpy.props.IntProperty(name = "Steps",min = 0, soft_min=0, soft_max = 10,step=1,default = 0, description = "Number of extrusion, set 0 to unlimited(until you press right mouse)")
    bpy.types.Scene.steps = bpy.props.IntProperty(min = 0, default = 0)
    
    # create scene variables
#    bpy.context.scene.min_distance = 5
#    bpy.context.scene.taper_value = 0.5
#    bpy.context.scene.cons_x = False
#    bpy.context.scene.cons_y = False
#    bpy.context.scene.cons_z = False
#    bpy.context.scene['orientation'] = 2
#    bpy.context.scene.auto_rotate = True
#    bpy.context.scene.collapse = True
#    bpy.context.scene.spin = 0
#    bpy.context.scene.stepsCounter = 0
#    bpy.context.scene.steps = 0
    
    
    LMB_Hold = False
    
    #set the face selection
    #bpy.context.tool_settings.mesh_select_mode[0] = False
    #bpy.context.tool_settings.mesh_select_mode[1] = False
    #bpy.context.tool_settings.mesh_select_mode[2] = True
    
    def modal(self, context, event):
        
        scn = context.scene 
                  
        if event.type == 'MOUSEMOVE' and self.LMB_Hold:
        
            #bpy.ops.object.mode_set(mode='OBJECT')
            #bpy.ops.object.mode_set(mode='EDIT')
            
                      
            # create variables           
            coord = event.mouse_region_x, event.mouse_region_y
            region = context.region
            rv3d = context.space_data.region_3d
            vec = region_2d_to_vector_3d(region, rv3d, coord)
            loc = (region_2d_to_location_3d(region, rv3d, coord, vec))
                  
            # get face center
            bpy.ops.object.mode_set(mode='OBJECT')
            me = bpy.context.object.data # Get the active mesh
            bm = bmesh.new()   # create an empty BMesh
            bm.from_mesh(me)   # fill it in from a Mesh
            face = bpy.context.object.data.polygons.active
            face_center = bm.faces[face].calc_center_median()
            bpy.ops.object.mode_set(mode='EDIT')
            face_center_2d = location_3d_to_region_2d(region, rv3d, face_center)
            face_normal = bpy.context.active_object.data.polygons[face].normal
            angle = 0
            
            if mathutils.Vector((coord)).x >= face_center_2d.x  and mathutils.Vector((coord)).y >= face_center_2d.y:
                
                angle = loc.angle(face_center)#/math.pi*180
                
            elif  mathutils.Vector((coord)).x <= face_center_2d.x  and mathutils.Vector((coord)).y <= face_center_2d.x:
                
                angle = -(loc.angle(face_center))#/math.pi*180
                       
                             
            x = rv3d.perspective_matrix[3].x
            y = rv3d.perspective_matrix[3].y
            z = rv3d.perspective_matrix[3].z
            axis = mathutils.Vector((x,y,z))                                           
            
            
            nx = face_normal.x
            ny=  face_normal.y
            nz= face_normal.z
            
            spinAngle = scn.spin *math.pi/180
             
            minDisVec = mathutils.Vector((scn.min_distance,scn.min_distance,scn.min_distance))    
            
#            if scn['stepsCounter']==0:
#                
#               
#                if scn['min_distance'] >= 1:  
#                       
#                    increment = round((loc - face_center).length,0) 
#        
#                    if increment == scn['min_distance'] :
#                                           
#                       if scn.auto_rotate:
#                           bpy.ops.transform.rotate(value=(angle), axis=(axis))
#                       extrusion(coord,region,rv3d,vec,loc,face,face_center,scn['taper_value'],scn.cons_x ,scn.cons_y,scn.cons_z,scn.orientation)
#                       bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz))
#                       
#                       
#                else:
#                    increment = round((loc - face_center).length,2)
#        
#                    if increment >= scn['min_distance']:
#                                           
#                       if scn.auto_rotate:
#                           bpy.ops.transform.rotate(value=(angle), axis=(axis))
#                       extrusion(coord,region,rv3d,vec,loc,face,face_center,scn['taper_value'],scn.cons_x ,scn.cons_y,scn.cons_z,scn.orientation)
#                       bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz))
#              
#        
#            else:
#                
#                
#                if scn['min_distance'] >= 1 and scn.steps > scn.stepsCounter:  
#                       
#                    increment = round((loc - face_center).length,0) 
#        
#                    if increment == scn['min_distance'] :
#                                           
#                       if scn.auto_rotate:
#                           bpy.ops.transform.rotate(value=(angle), axis=(axis))
#                       extrusion(coord,region,rv3d,vec,loc,face,face_center,scn['taper_value'],scn.cons_x ,scn.cons_y,scn.cons_z,scn.orientation)
#                       bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz))
#                       scn['steps']+=1
#                       print(scn.steps, scn.stepsCounter)
#                       
#                       
#                       
#                else:
#                    increment = round((loc - face_center).length,2)
#        
#                    if increment >= scn['min_distance']:
#                                           
#                       if scn.auto_rotate:
#                           bpy.ops.transform.rotate(value=(angle), axis=(axis))
#                       extrusion(coord,region,rv3d,vec,loc,face,face_center,scn['taper_value'],scn.cons_x ,scn.cons_y,scn.cons_z,scn.orientation)
#                       bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz))                                                                                   
#                       scn.steps+=1
            increment = round((loc - face_center).length,5)
             
              
            if scn.stepsCounter >0:
                
                if increment >= scn['min_distance'] and scn.steps < scn.stepsCounter:                                                                     
                    scn.steps += 1
                    if scn.auto_rotate:
                        bpy.ops.transform.rotate(value=(angle), axis=(axis))
                    extrusion(loc , face_center,scn['taper_value'], scn.cons_x, scn.cons_y, scn.cons_z,scn.orientation) 
                    bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz)) 
                                                            
            else:
                if increment >= scn['min_distance']:
                
                    if scn.auto_rotate:
                       bpy.ops.transform.rotate(value=(angle), axis=(axis))
                    extrusion(loc,face_center,scn['taper_value'],scn.cons_x ,scn.cons_y,scn.cons_z,scn.orientation)
                    bpy.ops.transform.rotate(value=(spinAngle), axis=(nx,ny,nz)) 
                    
                                   
        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.LMB_Hold = True
            elif event.value == 'RELEASE':
                self.LMB_Hold = False
     
        
        
        elif event.type in {'RIGHTMOUSE', 'NUMPAD_ENTER'} or (scn.steps >= scn.stepsCounter and scn.stepsCounter !=0):
            
            scn.steps = 0 
            if bpy.context.scene.collapse == True :
        
                bpy.ops.mesh.merge(type='COLLAPSE', uvs=True)
                           
            context.area.header_text_set()
                
            return {'FINISHED'}
        
        elif event.type == 'ESC':  
            
            bpy.ops.ed.undo()    
            context.area.header_text_set()
            
            return {'CANCELLED'}
        
        context.area.header_text_set('Hold LMB and move to extrude, RMB to confirm, ESC to abort ')
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if bpy.data.meshes[context.active_object.name].total_face_sel > 0:
            context.window_manager.modal_handler_add(self)
            if context.area.type == 'VIEW_3D':
                context.area.header_text_set('Hold LMB and move to extrude, RMB to confirm, ESC to abort')
                
            #self.initial_mouse = mathutils.Vector((event.mouse_region_x, event.mouse_region_y))
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active faces, could not finish")
            return {'CANCELLED'}
    
        
    
        
class UI (bpy.types.Panel):
    bl_label = 'Branch Extrusion'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
   
   

    def draw(self, context):
        
        scn = context.scene 
             
        layout = self.layout
        column = layout.column(align=True)
        column.operator('object.branch_extrusion')  
        
        column.label(text='Extrusion set:')
        
        column.prop(scn,'stepsCounter' , slider = True)
        
        column.prop(scn,'min_distance' , slider=True)
        column.prop(scn, 'taper_value', slider=True)
        column.prop(scn, 'spin', slider=True)
               
        column.label(text='Constraint axis')
        
        column.prop(scn,'cons_x')   
        column.prop(scn,'cons_y') 
        column.prop(scn,'cons_z') 
        
        column.label(text='ORIENTATION')
        
        column.prop(scn,'orientation') 
          
        column.label(text='Options:') 
        
        column.prop(scn,'collapse')       
        column.prop(scn,'auto_rotate')
        
def Menu_append(self, context):
    self.layout.separator()
    self.layout.operator(BranchExtrusionOperator.bl_idname, text="Branch Extrusion")
 

def register():
    bpy.utils.register_class(BranchExtrusionOperator)
    bpy.utils.register_class(UI)
    
def unregister():
    bpy.utils.unregister_class(BranchExtrusionOperator)
    bpy.utils.unregister_class(UI)
    
if __name__ == "__main__":
    register()