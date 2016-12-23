__status__ = "toolplus custom version"
__author__ = "mkbreuer"
__version__ = "1.0"
__date__ = "2016"



import bpy
from bpy import*
from bpy.props import *


class View3D_TP_FAKE_OPS(bpy.types.Operator):
    """do nothing"""
    bl_idname = "tp_ops.fake_ops"
    bl_label = "Do Nothing"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print
        return {'FINISHED'}


class View3D_TP_X_Mod_Mirror(bpy.types.Operator):
    """Add a x mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_x"
    bl_label = "Mirror X"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                         
                    bpy.context.object.modifiers["Mirror"].use_x = True
                    bpy.context.object.modifiers["Mirror"].use_y = False
                    bpy.context.object.modifiers["Mirror"].use_z = False          
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}
    

class View3D_TP_Y_Mod_Mirror(bpy.types.Operator):
    """Add a y mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_y"
    bl_label = "Mirror Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = False
                    bpy.context.object.modifiers["Mirror"].use_y = True
                    bpy.context.object.modifiers["Mirror"].use_z = False  
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}
    

class View3D_TP_Z_Mod_Mirror(bpy.types.Operator):
    """Add a z mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_z"
    bl_label = "Mirror Z"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = False
                    bpy.context.object.modifiers["Mirror"].use_y = False
                    bpy.context.object.modifiers["Mirror"].use_z = True         
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}   


class View3D_TP_XY_Mod_Mirror(bpy.types.Operator):
    """Add a xy mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_xy"
    bl_label = "Mirror XY"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = True
                    bpy.context.object.modifiers["Mirror"].use_y = True
                    bpy.context.object.modifiers["Mirror"].use_z = False           
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}


class View3D_TP_Yz_Mod_Mirror(bpy.types.Operator):
    """Add a yz mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_yz"
    bl_label = "Mirror Yz"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
    
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = False
                    bpy.context.object.modifiers["Mirror"].use_y = True
                    bpy.context.object.modifiers["Mirror"].use_z = True     
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}
    

class View3D_TP_Xz_Mod_Mirror(bpy.types.Operator):
    """Add a xz mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_xz"
    bl_label = "Mirror Xz"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = True
                    bpy.context.object.modifiers["Mirror"].use_y = False
                    bpy.context.object.modifiers["Mirror"].use_z = True         
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}   
    

class View3D_TP_XYZ_Mod_Mirror(bpy.types.Operator):
    """Add a xyz mirror modifier with cage and clipping"""
    bl_idname = "tp_ops.mod_mirror_xyz"
    bl_label = "Mirror XYZ"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "MIRROR")
            
            for mod in obj.modifiers: 
               
                if mod.type == "MIRROR":
                    
                    bpy.context.object.modifiers["Mirror"].use_x = True
                    bpy.context.object.modifiers["Mirror"].use_y = True
                    bpy.context.object.modifiers["Mirror"].use_z = True         
                    bpy.context.object.modifiers["Mirror"].show_on_cage = True
                    bpy.context.object.modifiers["Mirror"].use_clip = True

        return {'FINISHED'}   



class View3D_TP_X_Array(bpy.types.Operator):
    bl_label = 'X Array'
    bl_idname = 'tp_ops.x_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            bpy.context.object.modifiers["Array"].name = "Array_X"  
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY":
                          
                    bpy.context.object.modifiers["Array_X"].count = 5
                    bpy.context.object.modifiers["Array_X"].relative_offset_displace[0] = 1
                    bpy.context.object.modifiers["Array_X"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array_X"].relative_offset_displace[2] = 0                 
                    bpy.context.object.modifiers["Array_X"].use_merge_vertices = True
                    bpy.context.object.modifiers["Array_X"].use_merge_vertices_cap = True

        return {'FINISHED'}


class View3D_TP_Y_Array(bpy.types.Operator):
    bl_label = 'Y Array'
    bl_idname = 'tp_ops.y_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            bpy.context.object.modifiers["Array"].name = "Array_Y"  
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY":  
                    bpy.context.object.modifiers["Array_Y"].count = 5
                    bpy.context.object.modifiers["Array_Y"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array_Y"].relative_offset_displace[1] = 1
                    bpy.context.object.modifiers["Array_Y"].relative_offset_displace[2] = 0  
                    bpy.context.object.modifiers["Array_Y"].use_merge_vertices = True
                    bpy.context.object.modifiers["Array_Y"].use_merge_vertices_cap = True
                           
        return {'FINISHED'}


class View3D_TP_Z_Array(bpy.types.Operator):
    bl_label = 'Z Array'
    bl_idname = 'tp_ops.z_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            bpy.context.object.modifiers["Array"].name = "Array_Z" 
                        
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY":                      
                    bpy.context.object.modifiers["Array_Z"].count = 5
                    bpy.context.object.modifiers["Array_Z"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array_Z"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array_Z"].relative_offset_displace[2] = 1   
                    bpy.context.object.modifiers["Array_Z"].use_merge_vertices = True
                    bpy.context.object.modifiers["Array_Z"].use_merge_vertices_cap = True                    
        
        return {'FINISHED'}



class View3D_TP_XY_Array(bpy.types.Operator):
    bl_label = 'XY Array'
    bl_idname = 'tp_ops.xy_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY":          

                    bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1
                    bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0        
                    bpy.context.object.modifiers["Array"].count = 5

            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 

                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 0
        
        return {'FINISHED'}


class View3D_TP_XZ_Array(bpy.types.Operator):
    bl_label = 'XZ Array'
    bl_idname = 'tp_ops.xz_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1
                    bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0        
                    bpy.context.object.modifiers["Array"].count = 5
            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        
        return {'FINISHED'}


class View3D_TP_YZ_Array(bpy.types.Operator):
    bl_label = 'YZ Array'
    bl_idname = 'tp_ops.yz_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 1
                    bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0

            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        
        return {'FINISHED'}


class View3D_TP_XYZ_Array(bpy.types.Operator):
    bl_label = 'XYZ Array'
    bl_idname = 'tp_ops.xyz_array'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1
                    bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0
                    bpy.context.object.modifiers["Array"].count = 5

            
            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1
                    bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 0

            object.modifier_add(type = "ARRAY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "ARRAY": 
                    bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
                    bpy.context.object.modifiers["Array.002"].relative_offset_displace[1] = 0
                    bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = 1
                  
        return {'FINISHED'}





class View3D_TP_Bevel(bpy.types.Operator):
    bl_label = 'Bevel '
    bl_idname = 'tp_ops.mods_bevel'
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "BEVEL")
            
            for mod in obj.modifiers: 
               
                if mod.type == "BEVEL":
                    
                    bpy.context.object.modifiers["Bevel"].width = 0.2
                    bpy.context.object.modifiers["Bevel"].segments = 2
                    bpy.context.object.modifiers["Bevel"].profile = 1
                    bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
                    bpy.context.object.modifiers["Bevel"].angle_limit = 0.7   
     
        return {'FINISHED'}


        
class View3D_TP_Solidify(bpy.types.Operator):
    bl_label = 'Solidify'
    bl_idname = 'tp_ops.mods_solidify'
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        scene = bpy.context.scene 
        selected = bpy.context.selected_objects 
        object = bpy.ops.object 

        for obj in selected: 
            scene.objects.active = obj 
            
            object.modifier_add(type = "SOLIDIFY")
            
            for mod in obj.modifiers: 
               
                if mod.type == "SOLIDIFY":
                    bpy.context.object.modifiers["Solidify"].thickness = 0.25
                    bpy.context.object.modifiers["Solidify"].use_even_offset = True
     
        return {'FINISHED'}


class View3D_TP_Display_DrawWire(bpy.types.Operator):
    """Draw Type Wire"""
    bl_idname = "tp_ops.draw_wire"
    bl_label = "Draw Type Wire"

    def execute(self, context):
        bpy.context.object.draw_type = 'WIRE'       
        return {'FINISHED'}


class View3D_TP_Display_DrawSolid(bpy.types.Operator):
    """Draw Type Solid"""
    bl_idname = "tp_ops.draw_solid"
    bl_label = "Draw Type Solid"

    def execute(self, context):
        bpy.context.object.draw_type = 'SOLID'       
        return {'FINISHED'}


class View3D_TP_Wire_All(bpy.types.Operator):
    """Wire on all objects in the scene"""
    bl_idname = "tp_ops.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False            
            else:
                obj.show_all_edges = True
                obj.show_wire = True
                             
        return {'FINISHED'} 
    


class View3D_TP_Negativ_X_Cut(bpy.types.Operator):
    """cut object and delete negative X"""
    bl_idname = "tp_ops.mods_negativ_x_cut"
    bl_label = "Cut -X"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
          
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_Positiv_X_Cut(bpy.types.Operator):
    """cut object and delete positiv X"""
    bl_idname = "tp_ops.mods_positiv_x_cut"
    bl_label = "Cut +X"
    bl_options = {'REGISTER', 'UNDO'}


    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
          
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_Negativ_Y_Cut(bpy.types.Operator):
    """cut object and delete negative Y"""
    bl_idname = "tp_ops.mods_negativ_y_cut"
    bl_label = "Cut -Y"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
          
        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_Positiv_Y_Cut(bpy.types.Operator):
    """cut object and delete positiv Y"""
    bl_idname = "tp_ops.mods_positiv_y_cut"
    bl_label = "Cut +Y"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
          
        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_Negativ_Z_Cut(bpy.types.Operator):
    """cut object and delete negative Z"""
    bl_idname = "tp_ops.mods_negativ_z_cut"
    bl_label = "Cut -Z"
    bl_options = {'REGISTER', 'UNDO'}

    remove = bpy.props.BoolProperty(name="Remove Modifier",  description="Remove Modifier", default=False) 
    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
          
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_Positiv_Z_Cut(bpy.types.Operator):
    """cut object and delete positiv Z"""
    bl_idname = "tp_ops.mods_positiv_z_cut"
    bl_label = "Cut +Z"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':            
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}



class View3D_TP_Negativ_X_Cut_obm(bpy.types.Operator):
    """cut object and delete negative X"""
    bl_idname = "tp_ops.mods_negativ_x_cut_obm"
    bl_label = "Cut -X"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
          
        return {'FINISHED'}


class View3D_TP_Positiv_X_Cut_obm(bpy.types.Operator):
    """cut object on the positiv X-Ais"""
    bl_idname = "tp_ops.mods_positiv_x_cut_obm"
    bl_label = "Cut +X"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
        
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()                
                 
        return {'FINISHED'}


class View3D_TP_Negativ_Y_Cut_obm(bpy.types.Operator):
    """cut object and delete negative Y"""
    bl_idname = "tp_ops.mods_negativ_y_cut_obm"
    bl_label = "Cut -Y"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
                  
        return {'FINISHED'}


class View3D_TP_Positiv_Y_Cut_obm(bpy.types.Operator):
    """cut object and delete positiv Y"""
    bl_idname = "tp_ops.mods_positiv_y_cut_obm"
    bl_label = "Cut +Y"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 
    
    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
         
        return {'FINISHED'}


class View3D_TP_Negativ_Z_Cut_obm(bpy.types.Operator):
    """cut object and delete positive Z"""
    bl_idname = "tp_ops.mods_negativ_z_cut_obm"
    bl_label = "Cut -Z"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()
        bpy.ops.object.modifier_remove(modifier="Mirror")

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


class View3D_TP_PositivZ_Cut_obm(bpy.types.Operator):
    """cut object and delete positive Z  """
    bl_idname = "tp_ops.mods_positiv_z_cut_obm"
    bl_label = "Cut +Z"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 


    def execute(self, context):
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()
        bpy.ops.object.modifier_remove(modifier="Mirror")  

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}




class View3D_TP_Positiv_XY_Cut_obm(bpy.types.Operator):
    """cut object and delete positive XY  """
    bl_idname = "tp_ops.mods_positiv_xy_cut_obm"
    bl_label = "Cut +XY"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()            

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}



class View3D_TP_Positiv_XZ_Cut_obm(bpy.types.Operator):
    """cut object and delete positive XZ  """
    bl_idname = "tp_ops.mods_positiv_xz_cut_obm"
    bl_label = "Cut +XZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()     
        
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


    


class View3D_TP_Positiv_YZ_Cut_obm(bpy.types.Operator):
    """cut object and delete positive YZ  """
    bl_idname = "tp_ops.mods_positiv_yz_cut_obm"
    bl_label = "Cut +YZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()            
        
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()         

        return {'FINISHED'}



class View3D_TP_Positiv_XYZ_Cut_obm(bpy.types.Operator):
    """cut object and delete positive XYZ  """
    bl_idname = "tp_ops.mods_positiv_xyz_cut_obm"
    bl_label = "Cut +XYZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):
        
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()            
        
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'negative'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}



class View3D_TP_Negativ_XY_Cut_obm(bpy.types.Operator):
    """cut object and delete negativ XY"""
    bl_idname = "tp_ops.mods_negativ_xy_cut_obm"
    bl_label = "Cut -XY"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()            

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
                  
        return {'FINISHED'}




class View3D_TP_Negativ_XZ_Cut_obm(bpy.types.Operator):
    """cut object and delete negativ XZ"""
    bl_idname = "tp_ops.mods_negativ_xz_cut_obm"
    bl_label = "Cut -XZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()


        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
                  
        return {'FINISHED'}




class View3D_TP_Negativ_YZ_Cut_obm(bpy.types.Operator):
    """cut object and delete negativ YZ"""
    bl_idname = "tp_ops.mods_negativ_yz_cut_obm"
    bl_label = "Cut -YZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()            
        
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
                  
        return {'FINISHED'}




class View3D_TP_Negativ_XYZ_Cut_obm(bpy.types.Operator):
    """cut object and delete negativ XYZ"""
    bl_idname = "tp_ops.mods_negativ_xyz_cut_obm"
    bl_label = "Cut -XYZ"
    bl_options = {'REGISTER', 'UNDO'}

    edit = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=True) 

    def execute(self, context):

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle() 
            
        bpy.context.scene.AutoCut_axis = 'x'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()

        bpy.context.scene.AutoCut_axis = 'y'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()            
        
        bpy.context.scene.AutoCut_axis = 'z'
        bpy.context.scene.AutoCut_orientation = 'positive'
        bpy.ops.tp_ops.autocut()
        
        obj = bpy.context.active_object
        obj.modifiers.clear()

        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()        
                  
        return {'FINISHED'}


    
class View3D_TP_Boolean_Normal_Cut(bpy.types.Operator):
    """cut object at seleted normal"""
    bl_idname = "tp_ops.normal_cut"
    bl_label = "Normal Cut"
    bl_options = {'REGISTER', 'UNDO'}

    flip = bpy.props.BoolProperty(name="Switch Mode",  description="Switch Mode", default=False) 

    def execute(self, context):
        
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1})
        for i in range(self.flip):
            bpy.ops.mesh.flip_normals()
        bpy.ops.transform.resize(value=(1000, 1000, 0), constraint_axis=(True, True, False))
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 1000), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        
        bpy.ops.mesh.select_linked(delimit={'SEAM'})
        bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')
                         
        return {'FINISHED'}




class View3D_TP_AutoCut(bpy.types.Operator):
    """cut and delete choosen sides"""
    bl_idname = "tp_ops.mods_autocut"
    bl_label = "AutoCuts"
    bl_options = {'REGISTER', 'UNDO'}

    bpy.types.Scene.tp_axis = bpy.props.EnumProperty(
                          items = [("positiv",  "Positiv", "", 1),
                                   ("negativ",  "Negativ", "", 2)], 
                                   name = "Side for Remove",
                                   description="side for remove")
                                   

    bpy.types.Scene.tp_axis_cut = bpy.props.EnumProperty(
                          items = [("x",   "X",   "", 1),
                                   ("y",   "Y",   "", 2),
                                   ("z",   "Z",   "", 3), 
                                   ("xy",  "XY",  "", 4), 
                                   ("xz",  "XZ",  "", 5), 
                                   ("yz",  "YZ",  "", 6), 
                                   ("xyz", "XYZ", "", 7), 
                                   ("normal", "Normal", "", 8)],
                                   name = "Axis for Remove", 
                                   description="axis for remove")

  
    def execute(self, context):
        scene = context.scene
        
        if scene.tp_axis == "positiv":
             
            if scene.tp_axis_cut == "x":
                bpy.ops.tp_ops.mods_positiv_x_cut_obm()

            if scene.tp_axis_cut == "y":            
                bpy.ops.tp_ops.mods_positiv_y_cut_obm()

            if scene.tp_axis_cut == "z":  
                bpy.ops.tp_ops.mods_positiv_z_cut_obm()       

            if scene.tp_axis_cut == "xy":  
                bpy.ops.tp_ops.mods_positiv_xy_cut_obm()

            if scene.tp_axis_cut == "xy":  
                bpy.ops.tp_ops.mods_positiv_xz_cut_obm()

            if scene.tp_axis_cut == "yz":  
                bpy.ops.tp_ops.mods_positiv_yz_cut_obm()

            if scene.tp_axis_cut == "xyz":            
                bpy.ops.tp_ops.mods_positiv_xyz_cut_obm()
            
            if context.mode == 'EDIT_MESH':
                if scene.tp_axis_cut == "normal":            
                    bpy.ops.tp_ops.normal_cut()


        if scene.tp_axis == "negativ":

            if scene.tp_axis_cut == "x":  
                bpy.ops.tp_ops.mods_negativ_x_cut_obm()

            if scene.tp_axis_cut == "y":            
                bpy.ops.tp_ops.mods_negativ_y_cut_obm()   

            if scene.tp_axis_cut == "z":             
                bpy.ops.tp_ops.mods_negativ_z_cut_obm()

            if scene.tp_axis_cut == "xy":  
                bpy.ops.tp_ops.mods_negativ_xy_cut_obm()

            if scene.tp_axis_cut == "xz":            
                bpy.ops.tp_ops.mods_negativ_xz_cut_obm()

            if scene.tp_axis_cut == "yz":             
                bpy.ops.tp_ops.mods_negativ_yz_cut_obm()

            if scene.tp_axis_cut == "xyz":             
                bpy.ops.tp_ops.mods_negativ_xyz_cut_obm()
 
            if context.mode == 'EDIT_MESH':
                if scene.tp_axis_cut == "normal":            
                    bpy.ops.tp_ops.normal_cut(flip=True)

                      
        return {'FINISHED'}


    
def register():
    
    bpy.utils.register_module(__name__)

def unregister():
   
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()


