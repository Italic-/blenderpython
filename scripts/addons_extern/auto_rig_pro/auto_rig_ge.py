import bpy, bmesh, math, re, operator, os, difflib
from math import degrees, pi, radians, ceil
from bpy.types import Panel, UIList
import mathutils
from mathutils import Vector, Euler, Matrix
import numpy



print ("\n START AUTO-RIG PRO UNITY EXPORTER... \n")

##########################  CLASSES  ##########################
class unity_export(bpy.types.Operator):
      
    #tooltip
    """Make sure the character mesh in binded to the Auto-Rig Pro armature \nThen select the mesh and click to setup the rig"""
    
    bl_idname = "id.unity_export"
    bl_label = "unity_export"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            if context.object.type != 'MESH':
                self.report({'ERROR'}, "Select the body mesh")
                return{'FINISHED'}
            
            #save current mode
            body_obj = bpy.context.object
            current_mode = context.mode                 
            #bpy.ops.object.mode_set(mode='EDIT')  
            
            _unity_export()    
            
             #restore saved mode    
              
            try:                
                bpy.ops.object.mode_set(mode=current_mode)
                set_active_object(body_obj.name)
                self.report({'INFO'}, "Done.")
            except:
                pass
     
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo    
        
        return {'FINISHED'}
        
class set_humanoid_rig(bpy.types.Operator):
      
    #tooltip
    """Append the Humanoid armature, then click it to set the Humanoid armature as the deforming armature """
    
    bl_idname = "id.set_humanoid_rig"
    bl_label = "set_humanoid_rig"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        
        try:
            """
            if (context.object.type != 'ARMATURE') or (not 'humanoid' in context.object.name):
                self.report({'ERROR'}, "1. Append the Humanoid armature. \n2. Select the Auto-Rig Pro armature then the Humanoid armature (active).\n3. Click this button to link the Humanoid armature to the character mesh.")
                return{'FINISHED'}
            """
            try:
                bpy.data.objects["rig_humanoid"]                
            except:
                self.report({'ERROR'}, "Please append the Humanoid armature in the scene.")
                return{'FINISHED'} 
            try:
                bpy.data.objects["rig"]
            except:
                self.report({'ERROR'}, "Please append the Auto-Rig Pro armature in the scene.")
                return{'FINISHED'} 
           
            #save current mode           
            current_mode = context.mode 
         
            
            _set_humanoid_rig()
            
             #restore saved mode              
            try:                
                bpy.ops.object.mode_set(mode=current_mode)
               
                self.report({'INFO'}, "Done.")
            except:
                pass
     
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo    
        
        return {'FINISHED'}
        
class unset_humanoid_rig(bpy.types.Operator):
      
    #tooltip
    """ Set the Auto-Rig Pro armature as the deforming armature """
    
    bl_idname = "id.unset_humanoid_rig"
    bl_label = "unset_humanoid_rig"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        
        try:       
            try:
                bpy.data.objects["rig_humanoid"]                
            except:
                self.report({'ERROR'}, "The Humanoid armature has not been set yet.")
                return{'FINISHED'} 
            try:
                bpy.data.objects["rig"]
            except:
                self.report({'ERROR'}, "The Humanoid armature has not been set yet.")
                return{'FINISHED'} 
           
            #save current mode           
            current_mode = context.mode         
            print("execute")
            _unset_humanoid_rig()
            
             #restore saved mode              
            try:                
                print("restore")
                bpy.ops.object.mode_set(mode=current_mode)               
                self.report({'INFO'}, "Done.")
            except:
                pass
     
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo    
        
        return {'FINISHED'}

        
class select_exportable(bpy.types.Operator):
      
    #tooltip
    """Auto select the exportable armature and meshes to export """
    
    bl_idname = "id.select_exportable"
    bl_label = "select_exportable"
    bl_options = {'UNDO'}   
    
    type = bpy.props.StringProperty(name="Type")
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        
        #save current mode           
        current_mode = context.mode 
        
 
        if self.type == 'generic':
            try:
                arp_armature = bpy.data.objects['rig']
            except:
                self.report({'ERROR'}, "Please append the Auto-Rig Pro armature in the scene.")
                return{'FINISHED'} 
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            # select meshes with ARP armature modifier
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    try:
                        for modif in obj.modifiers:
                            if modif.type == 'ARMATURE':
                                if modif.object == arp_armature:                                  
                                    obj.select = True
                        
                    except:
                        pass
            # select ARP armature
            set_active_object("rig")
            
        if self.type == 'humanoid':
            try:
                humanoid_armature = bpy.data.objects['rig_humanoid']
            except:
                self.report({'ERROR'}, "Please append the Humanoid armature in the scene.")
                return{'FINISHED'} 
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            # select meshes with Humanoid armature modifier
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    try:
                        for modif in obj.modifiers:
                            if modif.type == 'ARMATURE':
                                if modif.object == humanoid_armature:                                  
                                    obj.select = True
                        
                    except:
                        pass
            # select Humanoid armature
            set_active_object("rig_humanoid")   
        
        #restore saved mode
        try:                
            bpy.ops.object.mode_set(mode=current_mode)           
           
        except:
            pass
     
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo   
        
        return {'FINISHED'}
        
        
class constraint_rig(bpy.types.Operator):
      
    #tooltip
    """ Bind or unbind the Humanoid armature to the Auto-Rig Pro armature. \nUnbind when exporting multiple baked actions. Bind before baking an action. """
    
    bl_idname = "id.constraint_rig"
    bl_label = "constraint_rig"
    bl_options = {'UNDO'}   
    
    state = bpy.props.BoolProperty(name="State")
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        
        #save current mode           
        current_mode = context.mode        
        
        _constraint_rig(self.state)
        
        #restore saved mode
        try:                
            bpy.ops.object.mode_set(mode=current_mode)           
           
        except:
            pass
            
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo    
        
        return {'FINISHED'}        
        
 
      
        
############ FUNCTIONS ##############################################################
def get_edit_bone(name):
    return bpy.context.object.data.edit_bones[name]
    
def set_active_object(object_name):
     bpy.context.scene.objects.active = bpy.data.objects[object_name]
     bpy.data.objects[object_name].select = True

def _unity_export():
    scene = bpy.context.scene
    body_obj = bpy.context.object
    
    # move cs_grp layer
    bpy.data.objects["cs_grp"].layers[19] = True
    bpy.data.objects["cs_grp"].layers[0] = False
    
    #delete rig_add modifier
    try:
        bpy.ops.object.modifier_remove(modifier="rig_add")
    except:
        pass
    # delete rig_add
    try:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["rig_add"].hide = False    
        bpy.data.objects["rig_add"].hide_select = False
        bpy.data.objects["rig_add"].select = True    
        bpy.ops.object.delete()
    except:
        pass
    
    # delete unused vgroups   
    try:
        vgroups = bpy.context.object.vertex_groups

        for x in vgroups:
            if 'c_eyelid_top_' in x.name or 'c_eyelid_bot_' in x.name or 'c_eyelid_corner_' in x.name:            
                bpy.ops.object.vertex_group_set_active(group=x.name)
                bpy.ops.object.vertex_group_remove()
    except:
        pass
            
    #optional optim
    if scene.bones_optim:
        bpy.ops.object.select_all(action='DESELECT')        
        set_active_object('rig')
        current_mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='EDIT')   
        edit_bones = bpy.context.object.data.edit_bones
        
        #delete bones in layer 17
        bpy.ops.armature.select_all(action='DESELECT')
        layer_17_current_state = bpy.context.object.data.layers[17]
        bpy.context.object.data.layers[17] = True #enable display for deletion

        for bone in edit_bones:   
            if bone.layers[17]:
                bone.select = True
                bpy.ops.armature.delete()
    
        bpy.context.object.data.layers[17] = layer_17_current_state
        bpy.ops.object.mode_set(mode=current_mode)   
        
    
def _set_humanoid_rig():
    #get the armatures   
    bpy.ops.object.mode_set(mode='OBJECT')    
        
    humanoid_armature = bpy.data.objects['rig_humanoid']
    arp_armature = bpy.data.objects['rig']
    """
    selected_objects = bpy.context.selected_objects
    if len(selected_objects) != 2:
        self.report({'ERROR'}, 'Select first the Auto-Rig Pro then the Humanoid armature(active)')
        return{'FINISHED'}
        
    if humanoid_armature == selected_objects[0]:
        arp_armature = selected_objects[1]
    if humanoid_armature == selected_objects[1]:
        arp_armature = selected_objects[0]
    """
    #set the scale    
    humanoid_armature.scale = arp_armature.scale
    set_active_object(humanoid_armature.name)
    bpy.ops.object.mode_set(mode='POSE')  
    bpy.ops.pose.select_all(action='SELECT')
    selected_bones = bpy.context.selected_pose_bones
    
    #list all target bones for rest pose
    bones_dict = {}
    
    #set the constraints target
    for bone in selected_bones:
        #make the bone active
        bpy.context.object.data.bones.active=bpy.context.object.pose.bones[bone.name].bone  
        
        for cns in bpy.context.object.pose.bones[bone.name].constraints:     
            #set the ARP armature as the constraint target
            cns.target = bpy.data.objects[arp_armature.name]
            
            if cns.name == 'Copy Transforms':
                bones_dict[bone.name]= (cns.subtarget, [0.0,0.0,0.0], [0.0,0.0,0.0], 0.0)
               
    
    #Define Humanoid rest pose from ARP armature
        # find the bones listed in the ARP armature and get the edit transform
    bpy.ops.object.mode_set(mode='OBJECT')
    set_active_object(arp_armature.name)
    bpy.ops.object.mode_set(mode='EDIT')    
        #make dictionnary of bones transforms    
  
    for key, value in bones_dict.items():    
        edit_bone = arp_armature.data.edit_bones[value[0]]
        
        #if key == 'root.x':
        #    edit_bone = arp_armature.data.edit_bones['c_root_master.x']
        
        bones_dict[key] = (value[0], edit_bone.head.copy(), edit_bone.tail.copy(), edit_bone.roll)
        
        # set these transforms to the humanoid armature
    bpy.ops.object.mode_set(mode='POSE') 
    bpy.ops.object.mode_set(mode='OBJECT')
    set_active_object(humanoid_armature.name)
    bpy.ops.object.mode_set(mode='EDIT') 
    
    for b in humanoid_armature.data.edit_bones:       
        b.head = bones_dict[b.name][1]
        b.tail= bones_dict[b.name][2]
        b.roll = bones_dict[b.name][3]
        if b.name == "root.x":
            #remove parent before switch direction
            get_edit_bone("spine_01.x").parent = None
            get_edit_bone("thigh_stretch.l").parent = None
            get_edit_bone("thigh_stretch.r").parent = None
            bpy.ops.armature.select_all(action='DESELECT')
            b.select = True
            bpy.ops.armature.switch_direction()
            #re assign parent
            get_edit_bone("spine_01.x").parent = get_edit_bone("root.x")
            get_edit_bone("thigh_stretch.l").parent = get_edit_bone("root.x")
            get_edit_bone("thigh_stretch.r").parent = get_edit_bone("root.x")
            get_edit_bone("spine_01.x").use_connect = True

    
    bpy.ops.object.mode_set(mode='POSE') 
    
    # create and key first and last action framerate
    bpy.ops.pose.select_all(action='SELECT')
    try:
        action = bpy.data.objects[arp_armature.name].animation_data.action

        current_frame = bpy.context.scene.frame_current#save current frame    

        for f in action.frame_range:    
            bpy.context.scene.frame_current = f
            bpy.context.scene.frame_set(bpy.context.scene.frame_current)#debug       
            bpy.ops.transform.translate(value=(0, 0, 0))#update    
            for bone in bpy.context.selected_pose_bones:
                bone.keyframe_insert(data_path="rotation_euler")
                bone.keyframe_insert(data_path="location")

        #restore current frame
        bpy.context.scene.frame_current = current_frame
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)#debug  

        bpy.data.objects[humanoid_armature.name].animation_data.action.name = action.name + "_humanoid"
        
    except:
        print("Error when creating the Humanoid action.")
    """
    # reset stretchy bone length      
    bpy.context.object.data.pose_position = 'REST'  
    stretchy_bones = ["root.x", "spine_01.x"]
    
    for bone in stretchy_bones:
        bpy.ops.pose.select_all(action='DESELECT')           
        bpy.context.object.pose.bones[bone].bone.select = True
        bpy.context.object.data.bones.active = bpy.context.object.pose.bones[bone].bone
        try:
            c = bpy.context.copy()
            c["constraint"] = bpy.context.active_pose_bone.constraints['Stretch To']
            bpy.ops.constraint.stretchto_reset(c, constraint="Stretch To", owner='BONE')
            
        except KeyError:
            if debug_print == True:
                print("can't reset the stretch for: " +bone)
                
    bpy.context.object.data.pose_position = 'POSE'   
    """
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Set the armature modifier
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            try:
                for modif in obj.modifiers:
                    if modif.type == 'ARMATURE':
                        if modif.object == arp_armature:
                            modif.object = humanoid_armature
                            modif.use_deform_preserve_volume = False
                        if modif.object == bpy.data.objects['rig_add']:
                            bpy.ops.object.select_all(action='DESELECT')
                            set_active_object(obj.name)
                            bpy.ops.object.modifier_remove(modifier=modif.name)
                        
            except:
                pass
                
    bpy.data.armatures[humanoid_armature.data.name].pose_position = 'POSE'
        
    
def _unset_humanoid_rig():
    #get the armatures   
    bpy.ops.object.mode_set(mode='OBJECT')   
        
    humanoid_armature = bpy.data.objects['rig_humanoid']
    arp_armature = bpy.data.objects['rig']     
    
    # set the ARP armature as the deforming one
    for obj in bpy.data.objects:
        if obj.type == 'MESH':   
        
            found_rig_add = False
            found_rig = False
            
            for modif in obj.modifiers:
                if modif.type == 'ARMATURE':
                    if modif.object == humanoid_armature: 
                        found_rig = True
                        modif.object = arp_armature
                        modif.use_deform_preserve_volume = True
                    if modif.object == bpy.data.objects["rig_add"]:
                        found_rig_add = True
                        
            if not found_rig_add and found_rig:
                #add the rig_add modifier                    
                new_mod = obj.modifiers.new("rig_add", 'ARMATURE')
                new_mod.object = bpy.data.objects["rig_add"]                
                #re order
                bpy.ops.object.select_all(action='DESELECT')
                set_active_object(obj.name)
                for i in range(0,20):
                    bpy.ops.object.modifier_move_up(modifier="rig")
                for i in range(0,20):
                    bpy.ops.object.modifier_move_up(modifier="rig_add")
                #put mirror at first
                for m in bpy.context.object.modifiers:
                    if m.type == 'MIRROR':
                        for i in range(0,20):
                            bpy.ops.object.modifier_move_up(modifier=m.name)
                  
    bpy.data.armatures[humanoid_armature.data.name].pose_position = 'REST'
    
def _constraint_rig(state):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    set_active_object("rig_humanoid")
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    
    for bone in bpy.context.selected_pose_bones:
        for cns in bone.constraints:
            if cns.name != "Track To" and cns.name != "Stretch To":
                cns.mute = state
           
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.transform.translate(value=(0, 0, 0))#update   



           
    
###########  UI PANEL  ###################

class auto_rig_GE_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Auto-Rig Pro: Game Engine Export"
    bl_idname = "id_auto_rig_ge"
    

    def draw(self, context):
        layout = self.layout
        object = context.object
        scene = context.scene
        
        
        #BUTTONS
        
        #layout.label("Unity Export:")
        box = layout.box()
        #row = layout.row(align=True)
        
        box.prop(scene, "unity_rig_type", expand=True)
        #col = layout.column(align=True)
        #box = col.box()    
        if scene.unity_rig_type == 'generic': 
            box.label("For Unity")
            box.prop(scene, "bones_optim")
            box.operator("id.unity_export", "Setup Generic Rig")
            export=box.operator("id.select_exportable", "Select Exportable", icon='RESTRICT_SELECT_OFF')
            export.type = 'generic'
            
        if scene.unity_rig_type == 'humanoid': 
            box.label("For Unity and Unreal Engine")
            row = box.row(align=True)
            row.operator("id.set_humanoid_rig", "Set")
            row.operator("id.unset_humanoid_rig", "Unset")
            row = box.row(align=True)
            button = row.operator("id.constraint_rig", "Bind")
            button.state = False
            button = row.operator("id.constraint_rig", "Unbind")
            button.state = True
            row = box.row(align=True)
            export=row.operator("id.select_exportable", "Select Exportable", icon='RESTRICT_SELECT_OFF')
            export.type = 'humanoid'
            
        
 
###########  REGISTER  ##################

def register():   
    bpy.types.Scene.bones_optim = bpy.props.BoolProperty(name="Bone Optimisation", default=False, description="Remove the reference bones for higher framerate in Unity. Enable only if you are certain not to edit the reference bones later.")
    bpy.types.Scene.unity_rig_type = bpy.props.EnumProperty(items=(
        ("generic", "Generic", "Generic rig type"),
        ("humanoid", "Humanoid", "Humanoid rig type")
        ), name = "Unity Rig Type Export", description="Rig type to export")
   
    
    
  
    
    
def unregister():   
    del bpy.types.Scene.bones_optim
    del bpy.types.Scene.unity_rig_type


    