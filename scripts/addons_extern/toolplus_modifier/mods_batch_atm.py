import bpy
from bpy import*
from bpy.props import *



class VIEW3D_TP_Batch_Automirror(bpy.types.Operator):
    """T+ AutoMirror :)"""
    bl_idname = "tp_batch.automirror"
    bl_label = "AutoMirror :)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):      
        return {'FINISHED'}
           
    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=300)

    def draw(self, context):
        
        layout = self.layout
        wm = bpy.context.window_manager
        layout.operator_context = 'INVOKE_DEFAULT'     
        layout.operator_context = 'INVOKE_REGION_WIN'

        if bpy.context.object.type == 'MESH':
            
             box = layout.box().column(1)  

             row = box.row(1).column_flow(2) 
             row.prop(context.scene, "AutoMirror_axis", text="")
             row.prop(context.scene, "AutoMirror_orientation", text="")                      
             row.prop(context.scene, "AutoMirror_threshold", text="Threshold")             
             
             row.operator("object.automirror", text="Execute")
             row.operator("tp_ops.remove_mod", text="Delete") 
             row.operator("tp_ops.apply_mod", text="Apply") 

             box = layout.box().column(1) 
            
             row = box.row(1).column_flow(2) 
             row.prop(context.scene, "AutoMirror_toggle_edit", text="Editmode")
             row.prop(context.scene, "AutoMirror_cut", text="Cut+Mirror")
             row.prop(context.scene, "AutoMirror_use_clip", text="Use Clip")
             row.prop(context.scene, "AutoMirror_show_on_cage", text="Editable")            

             box.separator()

             box = layout.box().column(1)    
                          
             row = box.row(1)                                 

             row.operator("ed.undo", text = " ", icon="LOOP_BACK")
             row.operator("ed.redo", text = " ", icon="LOOP_FORWARDS") 

             box.separator()
 
        else:
            
            box = layout.box().column(1)  
            
            row = box.row(1)              
            row.label(icon="ERROR", text="Only for Mesh!")
           

    def check(self, context):
        return True

