__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"


import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*



class View3D_TP_Origin_BBox(bpy.types.Operator):
    """TP Origin :)"""
    bl_label = "TP Origin :)"
    bl_idname = "tp_batch.origin_bbox"               
    bl_options = {'REGISTER', 'UNDO'}  
        
    def draw(self, context):
        layout = self.layout
        
        if context.mode == 'OBJECT':   
                
            box = layout.box().column(1)  

            row = box.column(1)
            row.operator("tp_ops.origin_set_cursor", text="3D Cursor", icon="LAYER_ACTIVE")
            row.operator("tp_ops.origin_set_mass", text="Center of Mass", icon="LAYER_ACTIVE")
            row.operator("tp_ops.origin_set_geom", text="Geometry to Origin", icon="LAYER_ACTIVE")
            
            box.separator()

            if bpy.context.object.type == 'MESH':

                box = layout.box().column(1)     
                box.scale_x = 0.1
                
                row = box.row(1)                                     
                sub1 = row.row(1)

                sub1.alignment ='LEFT'         
                sub1.label(" +Y Axis")

                sub2 = row.row(1)
                sub2.alignment ='CENTER'         
                sub2.label("   xY Axis")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT'         
                sub3.label("--Y Axis")

                #####  
                
                row = box.row(1)                                     
                sub1 = row.row(1)

                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubeback_cornertop_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_edgetop_minus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_cornertop_plus_xy', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 
                
                sub2.operator('tp_ops.cubefront_edgetop_minus_x', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_plus_z', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_edgetop_plus_x', text="", icon = "LAYER_ACTIVE")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_cornertop_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubeback_edgetop_plus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_cornertop_plus_xy', text="", icon = "LAYER_ACTIVE")
                
                #####

                row = box.row(1) 
                 
                sub1 = row.row(1)
                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubefront_edgemiddle_minus_x', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_side_plus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_edgemiddle_plus_x', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 

                sub2.operator('tp_ops.cubefront_side_minus_x', text="", icon = "LAYER_ACTIVE")
                if context.mode == 'OBJECT':
                    sub2.operator('object.origin_set', text="", icon = "LAYER_ACTIVE").type='ORIGIN_GEOMETRY'
                else:
                    sub2.operator('tp_ops.origin_set_editcenter', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_plus_x', text="", icon = "LAYER_ACTIVE")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_edgemiddle_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_side_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_edgemiddle_plus_y', text="", icon = "LAYER_ACTIVE")

                #####

                row = box.row(1)
                  
                sub1 = row.row(1)
                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubeback_cornerbottom_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_edgebottom_plus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_cornerbottom_plus_xy', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 

                sub2.operator('tp_ops.cubefront_edgebottom_minus_x', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_minus_z', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_edgebottom_plus_x', text="", icon = "LAYER_ACTIVE")    

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_cornerbottom_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_edgebottom_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_cornerbottom_plus_xy', text="", icon = "LAYER_ACTIVE")

                box.separator()


        else:   
            
            if context.mode == 'EDIT_MESH': 
                
                box = layout.box().column(1)     
                box.scale_x = 0.1
                
                row = box.row(1)                                     
                sub1 = row.row(1)

                sub1.alignment ='LEFT'         
                sub1.label(" +Y Axis")

                sub2 = row.row(1)
                sub2.alignment ='CENTER'         
                sub2.label("   xY Axis")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT'         
                sub3.label("--Y Axis")

                #####  
                
                row = box.row(1)                                     
                sub1 = row.row(1)

                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubeback_cornertop_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_edgetop_minus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_cornertop_plus_xy', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 
                
                sub2.operator('tp_ops.cubefront_edgetop_minus_x', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_plus_z', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_edgetop_plus_x', text="", icon = "LAYER_ACTIVE")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_cornertop_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubeback_edgetop_plus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_cornertop_plus_xy', text="", icon = "LAYER_ACTIVE")
                
                #####

                row = box.row(1) 
                 
                sub1 = row.row(1)
                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubefront_edgemiddle_minus_x', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_side_plus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_edgemiddle_plus_x', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 

                sub2.operator('tp_ops.cubefront_side_minus_x', text="", icon = "LAYER_ACTIVE")
                if context.mode == 'OBJECT':
                    sub2.operator('object.origin_set', text="", icon = "LAYER_ACTIVE").type='ORIGIN_GEOMETRY'
                else:
                    sub2.operator('tp_ops.origin_set_editcenter', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_plus_x', text="", icon = "LAYER_ACTIVE")

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_edgemiddle_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_side_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_edgemiddle_plus_y', text="", icon = "LAYER_ACTIVE")

                #####

                row = box.row(1)
                  
                sub1 = row.row(1)
                sub1.alignment ='LEFT' 
                
                sub1.operator('tp_ops.cubeback_cornerbottom_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubefront_edgebottom_plus_y', text="", icon = "LAYER_ACTIVE")
                sub1.operator('tp_ops.cubeback_cornerbottom_plus_xy', text="", icon = "LAYER_ACTIVE")

                sub2 = row.row(1)
                sub2.alignment ='CENTER' 

                sub2.operator('tp_ops.cubefront_edgebottom_minus_x', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_side_minus_z', text="", icon = "LAYER_ACTIVE")
                sub2.operator('tp_ops.cubefront_edgebottom_plus_x', text="", icon = "LAYER_ACTIVE")    

                sub3 = row.row(1)
                sub3.alignment ='RIGHT' 
                
                sub3.operator('tp_ops.cubefront_cornerbottom_minus_xy', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_edgebottom_minus_y', text="", icon = "LAYER_ACTIVE")
                sub3.operator('tp_ops.cubefront_cornerbottom_plus_xy', text="", icon = "LAYER_ACTIVE")

                box.separator()
                    
                                  
       
            box = layout.box().row()
            
            row = box.column(1) 
            row.label("Origin", icon = "EDITMODE_HLT") 
            row.label("  in  ", icon = "BLANK1") 
            row.label("  Editmode") 
            
            row = box.column(1) 
            row.operator("tp_ops.origin_cursor_edm","> Cursor")
            row.operator("tp_ops.origin_edm","> Active")   
            row.operator("tp_ops.origin_edm","> Selected")   
            
            box.separator()  
            
            box = layout.box().row()            
                                
            row = box.column(1) 
            row.label("Origin", icon = "OBJECT_DATAMODE") 
            row.label("   to  ", icon = "BLANK1") 
            row.label("Objectmode") 
                                    
            row = box.column(1) 
            row.operator("tp_ops.origin_cursor_obm","> Cursor")  
            row.operator("tp_ops.origin_obm","> Active")             
            row.operator("tp_ops.origin_obm","> Selected")             
     
            box.separator()         
                
        #####

        Display_Transform = context.user_preferences.addons[__package__].preferences.tab_transform_menu
        if Display_Transform == 'on':

            box = layout.box().column(1) 
             
            row = box.row(1)
            row.label("", icon = "MAN_TRANS")
            row.label("", icon = "MAN_ROT")
            row.label("", icon = "MAN_SCALE")
            row.label("Apply Transform")

            if context.mode == 'OBJECT':
                                
                row = box.row(1)                
                row.operator("object.transform_apply", "Location").location=True 
                row.operator("object.transform_apply", "Rotation").rotation=True 
                row.operator("object.transform_apply", "Scale").scale=True 
                                
            row = box.row(1)
            sub = row.row(1)
            sub.scale_x = 0.45                 
            sub.operator("object.location_clear", "ZeroObj").clear_delta=False
            sub.operator("tp_ops.zero_cursor", "Zero3dC")
            
            sub1 = row.row(1)
            sub1.scale_x = 0.15                
            sub1.operator("tp_ops.zero_x", "X")
            sub1.operator("tp_ops.zero_y", "Y")
            sub1.operator("tp_ops.zero_z", "Z")
            
            box.separator()
        
       
        if context.mode == 'OBJECT': 
                   
            Display_Align = context.user_preferences.addons[__package__].preferences.tab_align_menu
            if Display_Align == 'on':
                 
                box = layout.box().column(1) 
                 
                row = box.column(1)
                row.operator("object.align_tools", icon = "MANIPUL")
                row.operator("object.distribute_osc", icon = "ALIGN")
                
                box.separator()

        box = layout.box().column(1) 
         
        row = box.row(1)
        if context.mode == 'OBJECT':
            if len(bpy.context.selected_objects) == 0:
                pass 
            else:
                row.operator("tp_ops.bounding_box_simple", "BBox", icon = "MOD_LATTICE")   

        Display_BBox = context.user_preferences.addons[__package__].preferences.tab_bbox_menu
        if Display_BBox == 'on':

            row.prop(context.object, "show_bounds", text="ShowBounds", icon='STICKY_UVS_LOC') 

            sub = row.row(1)
            sub.scale_x = 0.5  
            sub.prop(context.object, "draw_bounds_type", text="") 


        Display_History = context.user_preferences.addons[__package__].preferences.tab_history_menu 
        if Display_History == 'on':
            
            box = layout.box().column(1)  
            
            row = box.row(1)
            row.operator("ed.undo", text=" ", icon="LOOP_BACK")
            row.operator("ed.redo", text=" ", icon="LOOP_FORWARDS") 
           
            box.separator()   

    def execute(self, context):
   
        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=300)




    

class View3D_TP_Origin_Cursor(bpy.types.Operator):
    '''Set Origin to Cursor'''
    bl_idname = "tp_ops.origin_set_cursor"
    bl_label = "Origin to Cursor"
    bl_options = {"REGISTER", 'UNDO'}   

    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        return{'FINISHED'}

 
class View3D_TP_Origin_Mass(bpy.types.Operator):
    '''Set Origin to Center of Mass'''
    bl_idname = "tp_ops.origin_set_mass"
    bl_label = "Origin to Center of Mass"
    bl_options = {"REGISTER", 'UNDO'}   

    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        
        return{'FINISHED'}


class View3D_TP_Origin_Geom(bpy.types.Operator):
    '''Set Geometry to Origin'''
    bl_idname = "tp_ops.origin_set_geom"
    bl_label = "Geometry to Origin"
    bl_options = {"REGISTER", 'UNDO'}   

    def execute(self, context):

        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        
        return{'FINISHED'}    
    
    

def register():

    bpy.utils.register_module(__name__)

def unregister():

    bpy.utils.unregister_module(__name__) 


if __name__ == "__main__":
    register()

   