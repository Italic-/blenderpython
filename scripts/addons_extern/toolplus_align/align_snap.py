__author__ = "mkbreuer"
__status__ = "toolplus"
__version__ = "1.0"
__date__ = "2016"


import bpy
from bpy import*
from bpy.props import*

         
               
class VIEW3D_TP_ORIENT_AXIS(bpy.types.Operator):
    """Transform Axis Orientation"""
    bl_idname = "tp_ops.orient_axis"
    bl_label = "Transform Axis Orientation"
    bl_options = {'REGISTER', 'UNDO'}

    tp_axis = bpy.props.EnumProperty(
        items=[("tp_global"    ,"Global"   ,"Global"),
               ("tp_local"     ,"Local"    ,"Local"),
               ("tp_normal"    ,"Normal"   ,"Normal"),
               ("tp_gimbal"    ,"Gimbal"   ,"Gimbal"),
               ("tp_view"      ,"View"     ,"View")],
               name = "TP-Axis",
               default = "tp_global",    
               description = "change manipulator axis")

    def execute(self, context):
        
        if self.tp_axis == "tp_global":
            bpy.context.space_data.transform_orientation = 'GLOBAL'               
        elif self.tp_axis == "tp_local":
            bpy.context.space_data.transform_orientation = 'LOCAL' 
        elif self.tp_axis == "tp_normal":
            bpy.context.space_data.transform_orientation = 'NORMAL'            
        elif self.tp_axis == "tp_gimbal":
             bpy.context.space_data.transform_orientation = 'GIMBAL'            
        elif self.tp_axis == "tp_view":
            bpy.context.space_data.transform_orientation = 'VIEW'      
        
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout.column(1)  

        box = layout.box().column(1)  
        
        row = box.column(1)
        row.alignment = 'CENTER'        
        row.prop(self, 'tp_axis',text=" ", expand =True) 




class VIEW3D_TP_SNAP_TARGET(bpy.types.Operator):
    """Snap Target"""
    bl_idname = "tp_ops.snap_target"
    bl_label = "Snap Target"
    bl_options = {'REGISTER', 'UNDO'}


    bpy.types.Scene.tp_snapt = bpy.props.EnumProperty(
                             items=[("tp_closest"   ,"Closes"   ,"Closest"  ,"" , 1),
                                    ("tp_center"    ,"Center"   ,"Center"   ,"" , 2),
                                    ("tp_median"    ,"Median"   ,"Median"   ,"" , 3),
                                    ("tp_median"    ,"Active"   ,"Active"   ,"" , 4)],
                                    name = "TP-Snap Target", 
                                    default = "tp_closest")

    def execute(self, context):
  
        if self.tp_snapt == "tp_closest":
            bpy.context.scene.tool_settings.snap_target = 'CLOSEST'         
        elif self.tp_snapt == "tp_center":
            bpy.context.scene.tool_settings.snap_target = 'CENTER'
        elif self.tp_snapt == "tp_median":
            bpy.context.scene.tool_settings.snap_target = 'MEDIAN'        
        elif self.tp_snapt == "tp_active":
            bpy.context.scene.tool_settings.snap_target = 'ACTIVE'

        return {'FINISHED'}



class VIEW3D_TP_PIVOT_TARGET(bpy.types.Operator):
    """Set Pivot"""
    bl_idname = "tp_ops.set_pivot"
    bl_label = "Set Pivot"
    bl_options = {'REGISTER', 'UNDO'}


    bpy.types.Scene.tp_pivot = bpy.props.EnumProperty(
                             items=[("tp_bbcenter"  ," "    ,""   ,"ROTATE"            , 1),
                                    ("tp_cursor"    ," "    ,""  ,"CURSOR"             , 2),
                                    ("tp_indiorg"   ," "    ,""   ,"ROTATECOLLECTION"  , 3),
                                    ("tp_median"    ," "    ,""   ,"ROTATECENTER"      , 4),
                                    ("tp_element"   ," "    ,""   ,"ROTACTIVE"         , 5)],
                                    name = "TP-Pivot", 
                                    default = "tp_bbcenter")

    def execute(self, context):

        if self.tp_pivot == "tp_bbcenter":
            bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'             
        elif self.tp_pivot == "tp_cursor":
            bpy.context.space_data.pivot_point = 'CURSOR' 
        elif self.tp_pivot == "tp_indiorg":
            bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'           
        elif self.tp_pivot == "tp_median":
            bpy.context.space_data.pivot_point = 'MEDIAN_POINT'                        
        elif self.tp_pivot == "tp_element":
            bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'

        return {'FINISHED'}


class VIEW3D_TP_SNAP_ELEMENT(bpy.types.Operator):
    """Snap Element"""
    bl_idname = "tp_ops.snap_element"
    bl_label = "Snap Element"
    bl_options = {'REGISTER', 'UNDO'}


    bpy.types.Scene.tp_snape = bpy.props.EnumProperty(
                             items=[("tp_increment" ,"Increment"        ,""   ,"SNAP_INCREMENT" , 1),
                                    ("tp_vertex"    ,"Vertex"        ,""   ,"SNAP_VERTEX"    , 2),
                                    ("tp_edge"      ,"Edge"        ,""   ,"SNAP_EDGE"      , 3),
                                    ("tp_face"      ,"Face"        ,""   ,"SNAP_FACE"      , 4),
                                    ("tp_volume"    ,"Volume"        ,""   ,"SNAP_VOLUME"    , 5)],
                                    name = "TP-Snap Element", 
                                    default = "tp_increment")

    def execute(self, context):

        if self.tp_snape == "tp_increment":
            bpy.ops.snape.increment()          
        elif self.tp_snape == "tp_vertex":
            bpy.ops.snape.vertex()     
        elif self.tp_snape == "tp_edge":
            bpy.ops.snape.edge()           
        elif self.tp_snape == "tp_face":
            bpy.ops.snape.face()                          
        elif self.tp_snape == "tp_volume":
            bpy.ops.snape.volume()     

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout.column(1)  

        box = layout.box().column(1)  
        
        row = box.column(1)
        row.alignment = 'CENTER'        
        row.prop(self, 'tp_snape',text=" ", expand =True)                                            
                                         

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*1.75, height=300)



######  Snap Target  ##################################################################

class VIEW3D_TP_Snap_ACTIVE(bpy.types.Operator):
    """Snap Target ACTIVE"""
    bl_idname = "tp_ops.snap_active"
    bl_label = "Snap Target ACTIVE"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        return {'FINISHED'}



class VIEW3D_TP_Snap_MEDIAN(bpy.types.Operator):
    """Snap Target MEDIAN"""
    bl_idname = "tp_ops.snap_median"
    bl_label = "Snap Target MEDIAN"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'MEDIAN'
        return {'FINISHED'}


class VIEW3D_TP_Snap_CENTER(bpy.types.Operator):
    """Snap Target CENTER"""
    bl_idname = "tp_ops.snap_center"
    bl_label = "Snap Target CENTER"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CENTER'
        return {'FINISHED'}


class VIEW3D_TP_Snap_CLOSEST(bpy.types.Operator):
    """Snap Target CLOSEST"""
    bl_idname = "tp_ops.snap_closest"
    bl_label = "Snap Target CLOSEST"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}


######  Snap Element  ##################################################################

class VIEW3D_TP_Snaep_VOLUME(bpy.types.Operator):
    """Snap Element VOLUME"""
    bl_idname = "tp_ops.snape_volume"
    bl_label = "Snap Element VOLUME"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VOLUME'
        return {'FINISHED'}


class VIEW3D_TP_Snaep_FACE(bpy.types.Operator):
    """Snap Element FACE"""
    bl_idname = "tp_ops.snape_face"
    bl_label = "Snap Element FACE"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        return {'FINISHED'}


class VIEW3D_TP_Snaep_EDGE(bpy.types.Operator):
    """Snap Element EDGE"""
    bl_idname = "tp_ops.snape_edge"
    bl_label = "Snap Element EDGE"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'EDGE'
        return {'FINISHED'}


class VIEW3D_TP_Snaep_VERTEX(bpy.types.Operator):
    """Snap Element VERTEX"""
    bl_idname = "tp_ops.snape_vertex"
    bl_label = "Snap Element VERTEX"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        return {'FINISHED'} 
    
    
class VIEW3D_TP_Snaep_INCREMENT(bpy.types.Operator):
    """Snap Element INCREMENT"""
    bl_idname = "tp_ops.snape_increment"
    bl_label = "Snap Element INCREMENT"
    bl_options = {'REGISTER'}

    
    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        return {'FINISHED'}



####Snap Set
class VIEW3D_TP_Snapset_Grid(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.grid"
    bl_label = "Absolute Grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        bpy.context.scene.tool_settings.use_snap_grid_absolute = True
        bpy.context.scene.tool_settings.use_snap_align_rotation = False            

        return {'FINISHED'}


class VIEW3D_TP_Snapset_Place(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.place"
    bl_label = "Place Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = True
        bpy.context.scene.tool_settings.use_snap_project = True
                        
        return {'FINISHED'}


class VIEW3D_TP_Snapset_Retopo(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.retopo"
    bl_label = "Mesh Retopo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
                    
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'FACE'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False
            
            
        return {'FINISHED'}


class VIEW3D_TP_Snapset_Active_Vert(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.active_vert"
    bl_label = "Active Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'            
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False       
 
        return {'FINISHED'}



class VIEW3D_TP_Snapset_Closest_Vert(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.closest_vert"
    bl_label = "Closest Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'          
        
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False       
 
        return {'FINISHED'}



class VIEW3D_TP_Snapset_Active_3d(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.active_3d"
    bl_label = "3d Cursor > Active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            

        bpy.context.space_data.pivot_point = 'CURSOR'            

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False   
        bpy.ops.view3d.snap_cursor_to_active()                    

        return {'FINISHED'}
            


class VIEW3D_TP_Snapset_Selected_3d(bpy.types.Operator):
    """Pivot and Snap changes at the same time"""
    bl_idname = "tp_ops.selected_3d"
    bl_label = "3d Cursor > Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):            
    
        bpy.context.space_data.pivot_point = 'CURSOR'  

        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
        bpy.context.scene.tool_settings.use_snap_align_rotation = False   

        bpy.ops.view3d.snap_cursor_to_selected()

        return {'FINISHED'}



def register():
    bpy.utils.register_module(__name__)
   
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()


















