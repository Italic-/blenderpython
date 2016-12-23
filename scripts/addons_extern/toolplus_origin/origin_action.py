__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"


import bpy, mathutils, math, re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*


class View3D_TP_Origin_EditCenter(bpy.types.Operator):
    '''Set Origin to Center / Editmode'''
    bl_idname = "tp_ops.origin_set_editcenter"
    bl_label = "Set Origin to Center / Editmode"
    bl_options = {"REGISTER", 'UNDO'}   

    def execute(self, context):

        bpy.ops.mesh.select_all(action='SELECT') 
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle() 
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')               
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT') 
        
        return{'FINISHED'}  


class View3D_TP_OriginObm(bpy.types.Operator):
    """set origin to selected / stay in objectmode"""                 
    bl_idname = "tp_ops.origin_obm"          
    bl_label = "origin to selected / in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
    

class View3D_TP_OriginEdm(bpy.types.Operator):
    """set origin to selected / stay in editmode"""                 
    bl_idname = "tp_ops.origin_edm"          
    bl_label = "origin to selected in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class View3D_TP_Origin_Edm_Cursor(bpy.types.Operator):
    """set origin to cursor / stay in editmode"""                 
    bl_idname = "tp_ops.origin_cursor_edm"          
    bl_label = "origin to cursor in editmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class View3D_TP_Origin_Obm_Cursor(bpy.types.Operator):
    """set origin to cursor / stay in objectmode"""                 
    bl_idname = "tp_ops.origin_cursor_obm"          
    bl_label = "origin to cursor in objectmode"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}   

 

class View3D_TP_Zero_X(bpy.types.Operator):
    """Zero X Axis"""                 
    bl_idname = "tp_ops.zero_x"          
    bl_label = "ZeroX"                 
    bl_options = {'REGISTER', 'UNDO'}   

    tp_switch = bpy.props.EnumProperty(
        items=[("tp_obj"    ,"Object"       ,"05"),
               ("tp_crs"    ,"3D Cursor"    ,"08")],
               name = "ZeroX",
               default = "tp_obj",    
               description = "zero object or cursor to x axis")

    def draw(self, context):
        layout = self.layout
        
        box = layout.box().column(1)

        row = box.row()
        row.prop(self, 'tp_switch', expand=True)

        box.separator()
        
    def execute(self, context):

        if self.tp_switch == "tp_obj":        
            bpy.context.object.location[0] = 0  

        if self.tp_switch == "tp_crs":        
            bpy.context.space_data.cursor_location[0] = 0 

        return {'FINISHED'} 

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*2, height=300)


    
class View3D_TP_Zero_Y(bpy.types.Operator):
    """Zero Y Axis"""                 
    bl_idname = "tp_ops.zero_y"          
    bl_label = "ZeroY"                 
    bl_options = {'REGISTER', 'UNDO'}   

    tp_switch = bpy.props.EnumProperty(
        items=[("tp_obj"    ,"Object"       ,"05"),
               ("tp_crs"    ,"3D Cursor"    ,"08")],
               name = "ZeroY",
               default = "tp_obj",    
               description = "zero object or cursor to y axis")

    def draw(self, context):
        layout = self.layout
        
        box = layout.box().column(1)

        row = box.row()
        row.prop(self, 'tp_switch', expand=True)

        box.separator()
        
    def execute(self, context):

        if self.tp_switch == "tp_obj":        
            bpy.context.object.location[1] = 0  

        if self.tp_switch == "tp_crs":        
            bpy.context.space_data.cursor_location[1] = 0 

        return {'FINISHED'} 

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*2, height=300)



class View3D_TP_Zero_Z(bpy.types.Operator):
    """Zero Z Axis"""                 
    bl_idname = "tp_ops.zero_z"          
    bl_label = "ZeroZ"                 
    bl_options = {'REGISTER', 'UNDO'}   

    tp_switch = bpy.props.EnumProperty(
        items=[("tp_obj"    ,"Object"       ,"05"),
               ("tp_crs"    ,"3D Cursor"    ,"08")],
               name = "ZeroZ",
               default = "tp_obj",    
               description = "zero object or cursor to z axis")

    def draw(self, context):
        layout = self.layout
        
        box = layout.box().column(1)

        row = box.row()
        row.prop(self, 'tp_switch', expand=True)

        box.separator()
        
    def execute(self, context):

        if self.tp_switch == "tp_obj":        
            bpy.context.object.location[2] = 0  

        if self.tp_switch == "tp_crs":        
            bpy.context.space_data.cursor_location[2] = 0 

        return {'FINISHED'} 

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*2, height=300)


class View3D_TP_Zero_Cursor(bpy.types.Operator):
    """Zero Cursor"""                 
    bl_idname = "tp_ops.zero_cursor"          
    bl_label = "Zero3DC"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):

        bpy.context.space_data.cursor_location[0] = 0 
        bpy.context.space_data.cursor_location[1] = 0 
        bpy.context.space_data.cursor_location[2] = 0 

        return {'FINISHED'} 



def register():

    bpy.utils.register_module(__name__)
 
    
def unregister():

    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()




















