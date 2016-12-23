


import bpy
from bpy import *
from bpy.props import *


def draw_align_relax_tools_panel_layout(self, context, layout):
        lt = context.window_manager.looptools

        #icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)

        box = layout.box().column(1)    
         
        row = box.row(1)              
        row.alignment = 'CENTER'
        row.label("", icon ="SPHERECURVE")

        box.separator()  

        row = box.column(1)    
        row.operator("mesh.vertices_smooth","Smooth Vertices", icon ="BLANK1") 
        row.operator("mesh.vertices_smooth_laplacian","Smooth Laplacian", icon ="BLANK1")  
        row.operator("mesh.shrinkwrap_smooth","Smooth Shrinkwrap", icon ="BLANK1")                 

        box.separator()  

        row = box.row(1)                      
        # relax - first line
        split = row.split(percentage=0.15, align=True)
        if lt.display_relax:
            split.prop(lt, "display_relax", text="", icon='TRIA_DOWN')
        else:
            split.prop(lt, "display_relax", text="", icon='TRIA_RIGHT')
        split.operator("mesh.looptools_relax", text="LoopTools  Relax", icon ="BLANK1")
        # relax - settings
        if lt.display_relax:
            box = layout.box().column(1)    
             
            row = box.column(1)  
            row.prop(lt, "relax_interpolation")
            row.prop(lt, "relax_input")
            row.prop(lt, "relax_iterations")
            row.prop(lt, "relax_regular")

            box.separator() 
            box = layout.box().column(1)   


        row = box.row(1) 
        # flatten - first line
        split = row.split(percentage=0.15, align=True)
        if lt.display_flatten:
            split.prop(lt, "display_flatten", text="", icon='TRIA_DOWN')
        else:
            split.prop(lt, "display_flatten", text="", icon='TRIA_RIGHT')
        split.operator("mesh.looptools_flatten", text="LoopTools  Flatten", icon ="BLANK1")
        # flatten - settings
        if lt.display_flatten:
            box = layout.box().column(1)    
             
            row = box.column(1)  
            row.prop(lt, "flatten_plane")

            box.separator()

            col_move = box.column(align=True)
            row = col_move.row(align=True)
            if lt.flatten_lock_x:
                row.prop(lt, "flatten_lock_x", text = "X", icon='LOCKED')
            else:
                row.prop(lt, "flatten_lock_x", text = "X", icon='UNLOCKED')
            if lt.flatten_lock_y:
                row.prop(lt, "flatten_lock_y", text = "Y", icon='LOCKED')
            else:
                row.prop(lt, "flatten_lock_y", text = "Y", icon='UNLOCKED')
            if lt.flatten_lock_z:
                row.prop(lt, "flatten_lock_z", text = "Z", icon='LOCKED')
            else:
                row.prop(lt, "flatten_lock_z", text = "Z", icon='UNLOCKED')
            col_move.prop(lt, "flatten_influence")

            box.separator() 
            box = layout.box().column(1)   


        box.separator()  

        row = box.row(1)              
        row.operator("mesh.face_make_planar", "Make Faces Planar", icon ="IMGDISPLAY")  

        ###
        box.separator()                         


        Display_History = context.user_preferences.addons[__package__].preferences.tab_history_relax 
        if Display_History == 'on':
            
            box = layout.box().column(1)  

            row = box.row(1)        
            row.operator("view3d.ruler", text="Ruler")   
             
            row.operator("ed.undo_history", text="History")
            row.operator("ed.undo", text="", icon="LOOP_BACK")
            row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
            box.separator()  




class VIEW3D_TP_Align_Relax_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Align"
    bl_idname = "VIEW3D_TP_Align_Relax_Panel_TOOLS"
    bl_label = "Relax"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        draw_align_relax_tools_panel_layout(self, context, layout) 



class VIEW3D_TP_Align_Relax_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Align_Relax_Panel_UI"
    bl_label = "Relax"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        draw_align_relax_tools_panel_layout(self, context, layout) 


