__author__ = "mkbreuer"
__status__ = "toolplus"
__version__ = "1.0"
__date__ = "2016"


import bpy
from bpy import*
from bpy.props import  *


class View3D_TP_Axis_Planes_Menu(bpy.types.Menu):
    bl_label = "Axis Planes"
    bl_idname = "tp_menu.intersetion_planes"

    def draw(self, context):
        layout = self.layout

        layout.operator("tp_ops.plane_x")
        layout.operator("tp_ops.plane_y")
        layout.operator("tp_ops.plane_z")



class View3D_TP_Boolean_Union(bpy.types.Operator):
    """Boolean Union"""
    bl_idname = "tp_ops.bool_union"
    bl_label = "Union"

    def execute(self, context):
        
        bpy.ops.mesh.intersect_boolean(operation='UNION')     
       
        return {'FINISHED'}  


class View3D_TP_Boolean_Different(bpy.types.Operator):
    """Boolean Different"""
    bl_idname = "tp_ops.bool_different"
    bl_label = "Different"

    def execute(self, context):
        
        bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')      
        
        return {'FINISHED'}  


class View3D_TP_Boolean_Intersect(bpy.types.Operator):
    """Boolean Intersect"""
    bl_idname = "tp_ops.bool_intersect"
    bl_label = "Intersect"

    def execute(self, context):
       
        bpy.ops.mesh.intersect_boolean(operation='INTERSECT')      
        
        return {'FINISHED'} 


class View3D_TP_Plane_X(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "tp_ops.plane_x"
    bl_label = "X Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')    

    def execute(self, context):
       
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.view3d.snap_cursor_to_selected()        
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')

        return {'FINISHED'}   


class View3D_TP_Plane_Y(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "tp_ops.plane_y"
    bl_label = "Y Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')    

    def execute(self, context):
       
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.view3d.snap_cursor_to_selected()    
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL')

        return {'FINISHED'}  
    

class View3D_TP_Plane_Z(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "tp_ops.plane_z"
    bl_label = "Z Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')    

    def execute(self, context):
      
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.view3d.snap_cursor_to_selected()    
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')

        return {'FINISHED'}  
    
   

class View3D_TP_Origin_Edm(bpy.types.Operator):
    """set origin to selected / editmode"""                 
    bl_idname = "tp_ops.origin_edm"          
    bl_label = "origin to selected"                 
    bl_options = {'REGISTER', 'UNDO'}   

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}




def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()






