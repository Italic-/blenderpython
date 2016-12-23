# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and / or
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####




import bpy, os
from bpy import *

import bpy.utils.previews
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)


def draw_normal_tools(context, layout):

    Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals
    if Display_Normals == 'on':
                 
        box = layout.box().column(1) 
        
        row = box.column(1) 
        row.label("Normals Transform", icon="ROTACTIVE")

        box.separator() 

        row = box.row(1)                
        row.menu("tp_ops.translate_normal_menu", text="Move")
        row.menu("tp_ops.rotate_normal_menu", text="Rotate")
        row.menu("tp_ops.resize_normal_menu", text="Scale")           

        box.separator() 


def draw_align_tools_panel_layout(self, context, layout):
        tpw = context.window_manager.tp_collapse_menu_align
        lt = context.window_manager.looptools
        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)
                  
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        ob = context.object  
        obj = context.object
        scene = context.scene
        scn = context.scene
        rs = bpy.context.scene 
                  
        obj = context.active_object     
        if obj:
           obj_type = obj.type
                          
           if obj_type in {'MESH'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("MESH") 
                                  
           if obj_type in {'LATTICE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("LATTICE") 

           if obj_type in {'CURVE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("CURVE")               
               
           if obj_type in {'SURFACE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("SURFACE")                 
               
           if obj_type in {'META'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("MBall")                 
               
           if obj_type in {'FONT'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("FONT")  
                                              
           if obj_type in {'ARMATURE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("ARMATURE") 

           if obj_type in {'EMPTY'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("EMPTY") 

           if obj_type in {'CAMERA'}:
              box = layout.box()
              row = box.row(1)                                        
              row.alignment = "CENTER"
              row.label("CAMERA") 

           if obj_type in {'LAMP'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("LAMP") 

           if obj_type in {'SPEAKER'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("SPEAKER") 


#######  Panel  #######-------------------------------------------------------     

        box = layout.box()
        
        row = box.row(1)  
        sub = row.row(1)
        sub.scale_x = 7

        sub.operator("tp_ops.pivot_bounding_box", "", icon="ROTATE")
        sub.operator("tp_ops.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("tp_ops.pivot_active", "", icon="ROTACTIVE")
        sub.operator("tp_ops.pivot_individual", "", icon="ROTATECOLLECTION")
        sub.operator("tp_ops.pivot_median", "", icon="ROTATECENTER")           
        #sub.menu("tp_ops.org_set", "", icon="PANEL_CLOSE")           


        if context.mode == 'OBJECT':

            box = layout.box().column(1)  
            
            row = box.row(1)
            row.alignment = "CENTER"            
            row.label("Align all Selected to Active")  
             
            box.separator() 
                        
            row = box.row(1)
            row.operator("object.align_location_all",text=" ", icon='MAN_TRANS')  
            row.operator("object.align_location_x",text="X")
            row.operator("object.align_location_y",text="Y")
            row.operator("object.align_location_z",text="Z")
        
            sub = row.row(1)
            sub.scale_x = 2.0    
            sub.operator("object.location_clear", text="", icon="X")
          
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= True
            props.rotation= False
            props.scale= False
                         
            row = box.row(1)
            row.operator("object.align_rotation_all",text=" ", icon='MAN_ROT') 
            row.operator("object.align_rotation_x",text="X")
            row.operator("object.align_rotation_y",text="Y")
            row.operator("object.align_rotation_z",text="Z")
            
            sub = row.row(1)
            sub.scale_x = 2.0           
            sub.operator("object.rotation_clear", text="", icon="X")
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= False
            props.rotation= True
            props.scale= False           

            row = box.row(1)
            row.operator("object.align_objects_scale_all",text=" ", icon='MAN_SCALE')  
            row.operator("object.align_objects_scale_x",text="X")
            row.operator("object.align_objects_scale_y",text="Y")
            row.operator("object.align_objects_scale_z",text="Z")
            
            sub = row.row(1)
            sub.scale_x = 2.0           
            sub.operator("object.scale_clear", text="", icon="X")
            
            props = row.operator("object.transform_apply", text="",icon="FILE_TICK")
            props.location= False
            props.rotation= False
            props.scale= True  
          
            box.separator()        
           
            row = box.row(1)         
            row.operator("object.distribute_osc", text="distribute between origins", icon="ALIGN")   

            box.separator()  

            Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals
            if Display_Normals == 'on':

                box = layout.box().column(1) 
                          
                row = box.row(1)  
                row.label("Normal [ZZ]") 
                
                row = box.row(1)              
                row.menu("tp_ops.translate_normal_menu", text="Move")
                row.menu("tp_ops.rotate_normal_menu", text="Rotate")
                row.menu("tp_ops.resize_normal_menu", text="Scale")           

                box.separator() 
            
            box = layout.box().column(1) 
                      
            row = box.row(1)  
            row.label("Mirror", icon='ARROW_LEFTRIGHT') 

            row = box.row(1)                             
            row.operator("tp_ops.mirror1",text="X-Axis")
            row.operator("tp_ops.mirror2",text="Y-Axis")
            row.operator("tp_ops.mirror3",text="Z-Axis")      

            box.separator()  
                
            box = layout.box().column(1) 
                      
            row = box.row(1)         
            row.label("Align with Local Y-Axis") 
            
            row = box.row(1) 
            row.operator("lookat.it", text="Look @ Obj ")
            row.operator("lookat.cursor", text="Look @ Cursor")   

            box.separator()  

            box = layout.box().column(1)           

            row = box.row(1)
            row.operator("object.align_by_faces", text="Active Face to Active Face", icon="SNAP_SURFACE") 
            row = box.row(1)
            row.operator("object.drop_on_active", text="Drop down to Active", icon="NLA_PUSHDOWN")        

            box.separator()      
                               
            box = layout.box().column(1)  
            
            row = box.row(1)
            row.operator("object.align_tools", "Advance Align Tools", icon="ROTATE") 

            box.separator()      
                               

        if context.mode == 'EDIT_MESH':

            box = layout.box().row()
            
            row = box.column(1) 
            row.label("Align") 
            row.label("to") 
            row.label("Axis") 

            row = box.column(1)
            row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
            row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
            row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

            row = box.column(1)
            row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
            row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
            row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

            row.separator()          
                         
            row = layout.box().column(1)                                  
            row.operator("tp_ops.align_to_normal", "Align to active Normal", icon ="SNAP_NORMAL")    

            box.separator() 
              
      
            box = layout.box().column(1)   
                         
            row = box.column(1)                                                         
            row.operator("mesh.vertex_align",text="Straighten Line", icon ="ALIGN") 
            row.operator("mesh.vertex_distribute",text="Distribute Vertices", icon ="PARTICLE_POINT")                                        
      
            box.separator() 
            
            box = layout.box().column(1)              
            
            row = box.row(1)  
            # space - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_space:
                split.prop(lt, "display_space", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_space", text="", icon='TRIA_RIGHT')
            
            split.operator("mesh.looptools_space", text="LoopTools  Space", icon='BLANK1')
            # space - settings
            if lt.display_space:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "space_interpolation")
                row.prop(lt, "space_input")

                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.space_lock_x:
                    row.prop(lt, "space_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_x", text = "X", icon='UNLOCKED')
                if lt.space_lock_y:
                    row.prop(lt, "space_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_y", text = "Y", icon='UNLOCKED')
                if lt.space_lock_z:
                    row.prop(lt, "space_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "space_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "space_influence")

                box.separator() 
                box = layout.box().column(1)   


            row = box.row(1)  
            # curve - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_curve:
                split.prop(lt, "display_curve", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_curve", text="", icon='TRIA_RIGHT')
            split.operator("mesh.looptools_curve", text="LoopTools  Curve", icon='BLANK1')
            # curve - settings
            if lt.display_curve:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "curve_interpolation")
                row.prop(lt, "curve_restriction")
                row.prop(lt, "curve_boundaries")
                row.prop(lt, "curve_regular")
                
                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.curve_lock_x:
                    row.prop(lt, "curve_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_x", text = "X", icon='UNLOCKED')
                if lt.curve_lock_y:
                    row.prop(lt, "curve_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_y", text = "Y", icon='UNLOCKED')
                if lt.curve_lock_z:
                    row.prop(lt, "curve_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "curve_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "curve_influence")

                box.separator() 
                box = layout.box().column(1)    


            row = box.row(1)  
            # circle - first line
            split = row.split(percentage=0.15, align=True)
            if lt.display_circle:
                split.prop(lt, "display_circle", text="", icon='TRIA_DOWN')
            else:
                split.prop(lt, "display_circle", text="", icon='TRIA_RIGHT')
            split.operator("mesh.looptools_circle", text="LoopTools  Circle", icon='BLANK1')
            # circle - settings
            if lt.display_circle:
                box = layout.box().column(1)              
                
                row = box.column(1) 
                row.prop(lt, "circle_fit")
                
                row.separator()

                row.prop(lt, "circle_flatten")
                
                row = box.row(align=True)
                row.prop(lt, "circle_custom_radius")
                
                row_right = row.row(align=True)
                row_right.active = lt.circle_custom_radius
                row_right.prop(lt, "circle_radius", text="")                
                box.prop(lt, "circle_regular")
                
                box.separator()

                col_move = box.column(align=True)
                row = col_move.row(align=True)
                if lt.circle_lock_x:
                    row.prop(lt, "circle_lock_x", text = "X", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_x", text = "X", icon='UNLOCKED')
                if lt.circle_lock_y:
                    row.prop(lt, "circle_lock_y", text = "Y", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_y", text = "Y", icon='UNLOCKED')
                if lt.circle_lock_z:
                    row.prop(lt, "circle_lock_z", text = "Z", icon='LOCKED')
                else:
                    row.prop(lt, "circle_lock_z", text = "Z", icon='UNLOCKED')
                col_move.prop(lt, "circle_influence")

            
            box.separator() 

            box = layout.box().column(1)              
            
            row = box.column(1) 
            row.operator("mesh.rot_con", "Rotate selected Face", icon ="LOCKVIEW_ON")   
            
            box.separator() 

            Display_Normals = context.user_preferences.addons[__package__].preferences.tab_normals
            if Display_Normals == 'on':
                         
                box = layout.box().column(1) 
                
                row = box.column(1) 
                row.label("Normal Transform", icon="ROTACTIVE")

                box.separator() 

                row = box.row(1)                
                row.menu("tp_ops.translate_normal_menu", text="Move")
                row.menu("tp_ops.rotate_normal_menu", text="Rotate")
                row.menu("tp_ops.resize_normal_menu", text="Scale")           

                box.separator() 

            box = layout.box().column(1)   
                         
            row = box.column(1)             
            row.label("Mirror", icon="ARROW_LEFTRIGHT")
                            
            row = box.row(1) 
            row.operator("tp_ops.mirror1",text="X-Axis")
            row.operator("tp_ops.mirror2",text="Y-Axis")
            row.operator("tp_ops.mirror3",text="Z-Axis")      

            box.separator() 

            row = box.column(1)          
            row.operator("tp_ops.mirror_over_edge", "Mirror over selected Edge", icon='IPO_LINEAR')    

            box.separator() 

            box = layout.box().column(1) 
                      
            row = box.row(1)         
            row.label("Align Edge to Edge") 
            
            row = box.row(1) 
            row.operator("mesh.align_operator", text = 'Store Edge').type_op = 1
            align_op = row.operator("mesh.align_operator", text = 'Align Edge').type_op = 0

            box.separator()      
 
            row = box.row(1) 
            if tpw.display_align_help:
                row.prop(tpw, "display_align_help", text="", icon='INFO')
            else:
                row.prop(tpw, "display_align_help", text="", icon='INFO')

            row.prop(bpy.context.window_manager.paul_manager, 'align_dist_z', text = 'Superpose')
            row.prop(bpy.context.window_manager.paul_manager, 'align_lock_z', text = 'lock Z')

            if tpw.display_align_help:

                box.separator() 
                              
                row = box.column(1)         
                row.label("This Tool need stored edge in the target:")         
                row.label("1. go into the editmode of the target") 
                row.label("2. select one edge as active") 
                row.label("3. and press Store Edge") 
               
                row.separator()            
                
                row.label("Now go into editmode of the object you want to align") 
                row.label("1. select all mesh that needs to be align") 
                row.label("2. select on edge as active") 
                row.label("3. and press Align Edge")
                
                row.separator()            
                
                row.label("Superpose: edge jump to edge")                  
                row.label("lock Z: preserve the z axis")                  

            ### 
            box.separator()     

  

        if context.mode == 'EDIT_LATTICE':

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             box = layout.box().column(1)   

             row = box.row(1) 
             row.operator("lattice.flip", text="FlipX").axis = "U"
             row.operator("lattice.flip", text="FlipY").axis = "V"
             row.operator("lattice.flip", text="FlipZ").axis = "W"

             box.separator()  
             
             row = box.row(1)         
             row.operator("tp_ops.mirror1",text="MX", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror2",text="MY", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror3",text="MZ", icon='ARROW_LEFTRIGHT')            

             ###         
             box.separator()

             draw_normal_tools(context, layout)               



        if context.mode == 'EDIT_CURVE' or context.mode == 'EDIT_SURFACE':

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             box.separator()  
           
             box = layout.box().column(1)               
            
             row = box.row(1)         
             row.operator("tp_ops.mirror1",text="MX", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror2",text="MY", icon='ARROW_LEFTRIGHT')
             row.operator("tp_ops.mirror3",text="MZ", icon='ARROW_LEFTRIGHT')            

             ###         
             box.separator()

             draw_normal_tools(context, layout)               



        if context.mode == 'EDIT_ARMATURE':    

             box = layout.box().row()
             row = box.column(1) 
             row.label("Align") 
             row.label("to") 
             row.label("Axis") 

             row = box.column(1)
             row.operator("tp_ops.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
             row.operator("tp_ops.face_align_yz", "Zy", icon='TRIA_UP_BAR')           
             row.operator("tp_ops.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

             row = box.column(1)
             row.operator("tp_ops.face_align_x", "X", icon='TRIA_RIGHT')
             row.operator("tp_ops.face_align_y", "Y", icon='TRIA_UP')           
             row.operator("tp_ops.face_align_z", "Z", icon='SPACE3')

             ###         
             box.separator()

             draw_normal_tools(context, layout)               


       
        Display_Orientation = context.user_preferences.addons[__package__].preferences.tab_orientation
        if Display_Orientation == 'on':
            
            box = layout.box().column(1)  

            row = box.row(1)         
            row.label(text="Transform Orientation")

            row = box.row(1)         
            row.prop(context.space_data, "transform_orientation", text="", icon='MANIPUL')
            row.operator("transform.create_orientation", text="", icon='ZOOMIN')

            if context.space_data.current_orientation:
                box.separator() 
                
                row = box.row(1)
                row.prop(context.space_data.current_orientation, "name", text="")
                row.operator("transform.delete_orientation", text="", icon='X')
           
            box.separator() 


        Display_History = context.user_preferences.addons[__package__].preferences.tab_history_align
        if Display_History == 'on':

            box = layout.box().column(1)  
           
            row = box.row(1)
            row.scale_y = 0.85        
            row.operator("view3d.ruler", text="Ruler")   
             
            row.operator("ed.undo_history", text="History")
            row.operator("ed.undo", text="", icon="LOOP_BACK")
            row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
            box.separator()   
        
        
        
#Align
def axe_select(self, context):
    axes = ['X','Y','Z']
    return [tuple(3 * [axe]) for axe in axes]

#Align
def project_select(self, context):
    projects = ['XY','XZ','YZ','XYZ']
    return [tuple(3 * [proj]) for proj in projects]



class VIEW3D_TP_Align_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Align"
    bl_idname = "VIEW3D_TP_Align_Panel_TOOLS"
    bl_label = "Align"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}
    
    bpy.types.Scene.AxesProperty = bpy.props.EnumProperty(items=axe_select)
    bpy.types.Scene.ProjectsProperty = bpy.props.EnumProperty(items=project_select)

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        ob = context.object  
        obj = context.object
        scene = context.scene
        scn = context.scene
        rs = bpy.context.scene 

        draw_align_tools_panel_layout(self, context, layout) 



class VIEW3D_TP_Align_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Align_Panel_UI"
    bl_label = "Align"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    bpy.types.Scene.AxesProperty = bpy.props.EnumProperty(items=axe_select)
    bpy.types.Scene.ProjectsProperty = bpy.props.EnumProperty(items=project_select)

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        ob = context.object  
        obj = context.object
        scene = context.scene
        scn = context.scene
        rs = bpy.context.scene 

        draw_align_tools_panel_layout(self, context, layout) 


