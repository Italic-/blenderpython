bl_info = {
    "name": "Auto-Rig Pro",
    "author": "Artell",
    "version": (0, 1),
    "blender": (2, 7, 5),
    "location": "3D View > Properties> Auto-Rig Pro",
    "description": "Automatic rig generation based on reference bones",     
    "category": "Animation"}    


import bpy, bmesh, mathutils, math

debug_print = False

 ##########################  CLASSES  ##########################
class create_driver(bpy.types.Operator):
      
    #tooltip
    """ Create a driver for the selected shape key using the Bone name and Bone transform parameter """
    
    bl_idname = "id.create_driver"
    bl_label = "create_driver"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:           
            _create_driver()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
 
class set_picker_camera(bpy.types.Operator):
      
    #tooltip
    """ Display the bone picker in this active view"""
    
    bl_idname = "id.set_picker_camera"
    bl_label = "set_picker_camera"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:           
            _set_picker_camera()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
 
class bind_to_rig(bpy.types.Operator):
      
    #tooltip
    """ Select the character mesh only then click to bind it to the rig"""
    
    bl_idname = "id.bind_to_rig"
    bl_label = "bind_to_rig"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:
                bpy.ops.object.mode_set(mode='EDIT')
                mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
                bpy.ops.object.mode_set(mode='OBJECT')           
            except TypeError:
                self.report({'ERROR'}, "Select the body object")
                bpy.ops.object.mode_set(mode='OBJECT')       
                return{'FINISHED'}
                
            _bind_to_rig()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
        
class unbind_to_rig(bpy.types.Operator):
      
    #tooltip
    """ Select the character mesh only then click to unbind it from the rig"""
    
    bl_idname = "id.unbind_to_rig"
    bl_label = "unbind_to_rig"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:
                bpy.ops.object.mode_set(mode='EDIT')
                mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
                bpy.ops.object.mode_set(mode='OBJECT')           
            except TypeError:
                self.report({'ERROR'}, "Select the body object")
                bpy.ops.object.mode_set(mode='OBJECT')       
                return{'FINISHED'}
                
            _unbind_to_rig()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}


class edit_ref(bpy.types.Operator):
      
    #tooltip
    """ Select the rig then click it to display the reference bones layer for editing"""
    
    bl_idname = "id.edit_ref"
    bl_label = "edit_ref"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try: #check if the armature is selected               
                get_bones = bpy.context.object.data.bones                      
            except AttributeError:
                self.report({'ERROR'}, "Select the rig object")                     
                return{'FINISHED'}
                
            _edit_ref()            
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class align_arm_bones(bpy.types.Operator):
      
    #tooltip
    """ Select the rig then click it to align the arm bones, roll, fk pole... from the main bones"""
    
    bl_idname = "id.align_arm_bones"
    bl_label = "align_arm_bones"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:                
                get_bones = bpy.context.object.data.bones                      
            except AttributeError:
                self.report({'ERROR'}, "Select the rig object")                     
                return{'FINISHED'}
                
            _align_arm_bones()            
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class align_spine_bones(bpy.types.Operator):
      
    #tooltip
    """ Align the spine bones from the main bones"""
    
    bl_idname = "id.align_spine_bones"
    bl_label = "align_spine_bones"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:                
                get_bones = bpy.context.object.data.bones                      
            except AttributeError:
                self.report({'ERROR'}, "Select the rig object")                     
                return{'FINISHED'}
                
            _align_spine_bones()            
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class align_leg_bones(bpy.types.Operator):
      
    #tooltip
    """ Align the legs bones, roll, fk pole... from the main bones"""
    
    bl_idname = "id.align_leg_bones"
    bl_label = "align_leg_bones"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:                
                get_bones = bpy.context.object.data.bones                      
            except AttributeError:
                self.report({'ERROR'}, "Select the rig object")                     
                return{'FINISHED'}
                
            _align_leg_bones()            
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class align_all_bones(bpy.types.Operator):
      
    #tooltip
    """ Select the rig then click it to match the rig with the reference bones"""
    
    bl_idname = "id.align_all_bones"
    bl_label = "align_all_bones"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:                
                get_bones = bpy.context.object.data.bones                      
            except AttributeError:
                self.report({'ERROR'}, "Select the rig object")                     
                return{'FINISHED'}
        
            _align_arm_bones()        
            _align_leg_bones()
            _align_spine_bones()
            
            bpy.context.object.show_x_ray = False            
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}   

    
 ##########################  FUNCTIONS  ##########################
def _create_driver():
        
    obj = bpy.context.active_object
    shape_keys = obj.data.shape_keys.key_blocks
    shape_index = bpy.context.object.active_shape_key_index

    #create driver        
    new_driver = shape_keys[shape_index].driver_add("value")
    new_driver.driver.expression = "var"
    new_var = new_driver.driver.variables.new()
    new_var.type = 'TRANSFORMS'
    new_var.targets[0].id = bpy.data.objects["rig"]
    new_var.targets[0].bone_target = bpy.context.object.driver_bone

    new_var.targets[0].transform_type = bpy.context.object.driver_transform
    new_var.targets[0].transform_space = 'LOCAL_SPACE' 
 
 
def _set_picker_camera():
    
    # go to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #save current scene camera
    current_cam = bpy.context.scene.camera
    
    
    bpy.ops.object.select_all(action='DESELECT')

    cam_ui = bpy.data.objects["cam_ui"]
    rig = bpy.data.objects["rig"]
    cam_ui.select = True
    bpy.context.scene.objects.active = cam_ui
    bpy.ops.view3d.object_as_camera()
    bpy.context.space_data.lock_camera_and_layers = False 
    
    #restore the scene camera
    bpy.context.scene.camera = current_cam
    
    #back to pose mode
    bpy.ops.object.select_all(action='DESELECT')
    rig.select = True
    bpy.context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')

def _bind_to_rig():
    char_mesh =  bpy.context.scene.objects.active    
    rig = bpy.data.objects["rig"]
    rig_add = bpy.data.objects["rig_add"]
    
    rig_add.hide = False    
    bpy.context.scene.objects.active = rig_add       
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    bpy.context.scene.objects.active = rig
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    bpy.context.scene.objects.active = char_mesh
    bpy.context.object.modifiers["Armature"].name = "rig_add"
    bpy.context.object.modifiers["Armature.001"].name = "rig"
    #reorder at the top
    for i in range(0,20):
        bpy.ops.object.modifier_move_up(modifier="rig")
    for i in range(0,20):
        bpy.ops.object.modifier_move_up(modifier="rig_add")

    bpy.context.object.modifiers["rig"].use_deform_preserve_volume = True
    #unparent
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    
    rig_add.hide = True  

def _unbind_to_rig():
    char_mesh =  bpy.context.scene.objects.active    
    rig = bpy.data.objects["rig"]
    rig_add = bpy.data.objects["rig_add"]    
    
    bpy.context.scene.objects.active = char_mesh   
    # delete modifiers
    bpy.ops.object.modifier_remove(modifier="rig_add")
    bpy.ops.object.modifier_remove(modifier="rig")
    try:
        bpy.ops.object.vertex_group_remove(all=True)
    except:
        pass
 
 
 
def _edit_ref():
    
    
    #display layer 17 only
    _layers = bpy.context.object.data.layers
    #must enabling one before disabling others
    _layers[17] = True  
    for i in range(0,31):
        if i != 17:
            _layers[i] = False 
      
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    #enable x-axis mirror edit
    bpy.context.object.data.use_mirror_x = True



def _align_arm_bones():
    
    if debug_print == True:
        print("\n START ALIGNING ARM BONES ... \n")
    
    #disable the proxy picker to avoid bugs
    proxy_picker_state = bpy.context.scene.Proxy_Picker.active    
    try:
        bpy.context.scene.Proxy_Picker.active = False
    except:
        pass    
    
    #define the side
    side = ".l"    
     
    #get bones
    prepole_name = "arm_fk_pre_pole"
    arm_name = "arm_ref"
    forearm_name = "forearm_ref"
    hand_name = "hand_ref"
    fk_pole_name = "arm_fk_pole"
    ik_pole_name = "c_arms_pole"
    shoulder_name = "shoulder_ref"
    shoulder_track_pole_name = "shoulder_track_pole"
    shoulder_pole_name = "shoulder_pole"
    arm_twist_offset_name = "c_arm_twist_offset"
    hand_rot_twist_name = "hand_rot_twist"
    stretch_arm_name = "c_stretch_arm"
    
    forearms = ["c_forearm_fk"+side, "forearm_fk"+side, "forearm_ik_nostr"+side, "forearm_ik"+side, "forearm_twist"+side, "forearm_stretch"+side, "forearm"+side]
    
    arms = ["c_arm_fk"+side, "arm_fk"+side, "arm_ik_nostr"+side, "arm_ik_nostr_scale_fix"+side, "arm_ik"+side, "arm_twist"+side, "arm_stretch"+side, "arm"+side, "c_arm_twist_offset"+side]
    
    hands = ["hand"+side, "c_hand_ik"+side, "c_hand_fk"+side, "c_hand_fk_scale_fix"+side]
    shoulders = ["shoulder"+side, "c_shoulder"+side]
    arm_bends = ["c_shoulder_bend"+side, "c_arm_bend"+side, "c_elbow_bend"+side, "c_forearm_bend"+side, "c_wrist_bend"+side]
    
    bpy.ops.object.mode_set(mode='EDIT')
        #enable x-axis mirror edit
    bpy.context.object.data.use_mirror_x = True
    
    #select all layers
        #save current displayed layers
    _layers = bpy.context.object.data.layers
    layers_select = []
    for i in range(0,31):
        if bpy.context.object.data.layers[i] == True:    
            layers_select.append(True)
        else:
            layers_select.append(False)
        
    #display all layers for constraint parameters to work
    for i in range(0,31):
        bpy.context.object.data.layers[i] = True
        
    #declare bones (maybe useless here)
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]   
    arm =  bpy.context.object.data.edit_bones[arm_name + side]
    forearm =  bpy.context.object.data.edit_bones[forearm_name + side]
    fk_pole =  bpy.context.object.data.edit_bones[fk_pole_name + side]
    ik_pole = bpy.context.object.data.edit_bones[ik_pole_name + side]
    
    #align arms and forearms bones from references bones
    for bone in arms:
        init_selection(bone)
        current_arm = bpy.context.object.data.edit_bones[bone]
        ref_arm = bpy.context.object.data.edit_bones[arm_name+side]
        arm_vec = ref_arm.tail - ref_arm.head
        
        if bone == arm_twist_offset_name+side:
            current_arm.head = ref_arm.head
            current_arm.tail = ref_arm.head + arm_vec * 0.4
           
        else:
            current_arm.head = ref_arm.head
            current_arm.tail = ref_arm.tail
        mirror_hack()
    
    # stretch controller
    init_selection(stretch_arm_name+side)
    stretch_arm = get_bone(stretch_arm_name+side)
    arm = get_bone(arm_name+side)
    dir = stretch_arm.tail - stretch_arm.head
    stretch_arm.head = arm.tail
    stretch_arm.tail = stretch_arm.head + dir
    mirror_hack()  
        
    # pin controller
    init_selection("c_stretch_arm_pin"+side)
    stretch_arm_pin = get_bone("c_stretch_arm_pin"+side)
    arm = get_bone(arm_name+side)
    dir = stretch_arm.tail - stretch_arm.head
    stretch_arm_pin.head = arm.tail
    stretch_arm_pin.tail = stretch_arm_pin.head + dir
    mirror_hack()       
        
    for bone in forearms:
        init_selection(bone)
        current_arm = bpy.context.object.data.edit_bones[bone]
        ref_arm = bpy.context.object.data.edit_bones[forearm_name+side]
        
        current_arm.head = ref_arm.head
        current_arm.tail = ref_arm.tail
        mirror_hack()
        
    for bone in shoulders:
        init_selection(bone)
        current_bone = bpy.context.object.data.edit_bones[bone]
        ref_bone = bpy.context.object.data.edit_bones[shoulder_name+side]
        
        current_bone.head = ref_bone.head
        current_bone.tail = ref_bone.tail
        current_bone.roll = ref_bone.roll
        mirror_hack()
        
        # align secondary bones
    for bone in arm_bends:
        init_selection(bone)
        current_bone = bpy.context.object.data.edit_bones[bone]
        arm = bpy.context.object.data.edit_bones[arm_name+side]
        forearm = bpy.context.object.data.edit_bones[forearm_name+side]
        length = 0.07
        
        if "shoulder" in bone: 
            current_bone.head = arm.head + (arm.tail-arm.head) * 0.3
            current_bone.tail = current_bone.head - arm.z_axis * length
        if "c_arm_bend" in bone: 
            arm_vec = arm.tail - arm.head
            current_bone.head = arm.head + arm_vec*0.6
            current_bone.tail = current_bone.head - arm.z_axis * length
        if "elbow" in bone:            
            current_bone.head = arm.tail
            current_bone.tail = current_bone.head - arm.z_axis * length
        if "forearm" in bone:            
            arm_vec = forearm.tail - forearm.head
            current_bone.head = forearm.head + arm_vec*0.5
            current_bone.tail = current_bone.head - forearm.z_axis * length
        if "wrist" in bone: 
            current_bone.head = forearm.tail - forearm.y_axis * 0.025
            current_bone.tail = current_bone.head - forearm.z_axis * length
        
        #set roll
        bpy.ops.armature.calculate_roll(type='POS_Z')    
        mirror_hack()
        
    #align FK pre-pole
    init_selection(prepole_name+side)       
    
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]
    arm =  bpy.context.object.data.edit_bones[arm_name + side]
    forearm =  bpy.context.object.data.edit_bones[forearm_name + side]
    
        # center the prepole in the middle of the chain    
    prepole.head[0] = (arm.head[0] + forearm.tail[0])/2
    prepole.head[1] = (arm.head[1] + forearm.tail[1])/2
    prepole.head[2] = (arm.head[2] + forearm.tail[2])/2
        # point toward the elbow
    prepole.tail[0] = arm.tail[0]
    prepole.tail[1] = arm.tail[1]
    prepole.tail[2] = arm.tail[2]    
    
        #mirror other side bone    
    mirror_hack()
    
    
    #align FK pole
    init_selection(fk_pole_name+side)  
    
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]
    fk_pole = bpy.context.object.data.edit_bones[fk_pole_name + side]
    
    prepole_dir = prepole.tail - prepole.head
    fk_pole.head = prepole.head + prepole_dir * 11.5
    fk_pole.tail = prepole.tail + prepole_dir * 11.5 
   
    mirror_hack()  
    
    #align IK pole
    init_selection(ik_pole_name+side)    
    
    fk_pole =  bpy.context.object.data.edit_bones[fk_pole_name + side]
    ik_pole = bpy.context.object.data.edit_bones[ik_pole_name + side]
    
    ik_pole.head = fk_pole.head
    ik_pole.tail = [ik_pole.head[0], ik_pole.head[1], ik_pole.head[2]+0.1]   
   
    mirror_hack()
   
    # bone roll adjust
    init_selection(forearm_name+side)   
    
    bpy.ops.armature.calculate_roll(type='POS_Z')    
   
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT')
    arm =  bpy.context.object.data.edit_bones[arm_name + side]
    arm.select = True   
    bpy.context.object.data.bones.active = bpy.context.object.pose.bones[forearm_name+side].bone    
    bpy.ops.armature.calculate_roll(type='ACTIVE') 
   
    mirror_hack()    
    
    #copy the roll to other bones
    init_selection("null") 
    
    forearm =  bpy.context.object.data.edit_bones[forearm_name + side]
    arm =  bpy.context.object.data.edit_bones[arm_name + side]
    
    for bone in forearms:        
        current_bone = bpy.context.object.data.edit_bones[bone].select = True
        bpy.context.object.data.edit_bones[bone].roll = forearm.roll             
    
    for bone in arms:
        bpy.context.object.data.edit_bones[bone].roll = arm.roll   
    
    # shoulder poles
    init_selection(shoulder_track_pole_name+side)    
    
        #track pole        
    shoulder_track_pole = bpy.context.object.data.edit_bones[shoulder_track_pole_name + side]
    forearm =  bpy.context.object.data.edit_bones[forearm_name + side]
    arm =  bpy.context.object.data.edit_bones[arm_name + side]    
    
    shoulder_track_pole.select = True    
    
    shoulder_track_pole.head = (arm.head + get_bone(shoulder_name+side).head)/2
    shoulder_track_pole.head[2] += 0.04
    dir = forearm.head - shoulder_track_pole.head
    shoulder_track_pole.tail = shoulder_track_pole.head + dir / 4
    
    shoulder_track_pole.roll = arm.roll
        
    mirror_hack()
    
        #shoulder visual position
    init_selection("c_p_shoulder"+side)
    p_shoulder = get_bone("c_p_shoulder"+side)
    #test if has breast to set the shoulder visual position
    has_breast = False
    try:
        breast_02 = get_bone("c_breast_02"+side)
        has_breast = True
    except:
        has_breast = False
        
    shoulder = get_bone("c_shoulder"+side)
    
    p_shoulder.head = (shoulder.head + shoulder.tail)/2
    p_shoulder.head[2] += 0.05
    if has_breast == True:
        p_shoulder.head[1] = breast_02.head[1]
    else:
        p_shoulder.head[1] += -0.08
    p_shoulder.tail = p_shoulder.head + (shoulder.tail-shoulder.head)/2
    p_shoulder.tail[2] = p_shoulder.head[2]
    p_shoulder.roll = math.radians(180)
    
    mirror_hack()
    
        # pole
    init_selection(shoulder_pole_name+side)    
    
    arm =  bpy.context.object.data.edit_bones[arm_name + side]
    shoulder_track_pole = bpy.context.object.data.edit_bones[shoulder_track_pole_name + side]
    shoulder_pole = bpy.context.object.data.edit_bones[shoulder_pole_name + side]
    
    shoulder_pole.head = arm.head + arm.z_axis * -0.1
    shoulder_pole.tail = arm.head + arm.z_axis * -0.1 + arm.y_axis * 0.1       
 
    mirror_hack()    
    
    # reset stretchy bone length
    bpy.ops.object.mode_set(mode='OBJECT')   
    bpy.ops.object.mode_set(mode='POSE')     
    
    #reset the stretch
    bpy.context.object.data.pose_position = 'REST'
    all_arms = arms + forearms
    
    for bone in all_arms:
        if "twist" in bone or bone == "forearm"+side or "stretch" in bone:
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
            #mirror
            bpy.ops.pose.select_mirror()
            try:
                c = bpy.context.copy()
                c["constraint"] = bpy.context.active_pose_bone.constraints['Stretch To']
                bpy.ops.constraint.stretchto_reset(c, constraint="Stretch To", owner='BONE')
                
            except KeyError:
                if debug_print == True:
                    print("can't reset the stretch for: " + bone)              
    
    
    # align hand_rot_twist
    init_selection(hand_rot_twist_name+side)
    
    hand =  bpy.context.object.data.edit_bones[hand_name + side]
    hand_rot_twist = bpy.context.object.data.edit_bones[hand_rot_twist_name + side]
    forearm = bpy.context.object.data.edit_bones[forearm_name + side]    
    
    hand_rot_twist.head = hand.head + hand.y_axis * 0.02 + hand.z_axis * 0.04
    hand_rot_twist.tail = hand_rot_twist.head + forearm.y_axis * 0.02
    hand_rot_twist.roll = forearm.roll
    
    mirror_hack()
    
    # align hands
    hands = ["hand"+side, "c_hand_ik"+side, "c_hand_fk"+side, "c_hand_fk_scale_fix"+side]

    for bone in hands:
        init_selection(bone)
        current_hand = bpy.context.object.data.edit_bones[bone]
        ref_hand = bpy.context.object.data.edit_bones[hand_name + side]
        current_hand.head = ref_hand.head
        current_hand.tail = ref_hand.tail
        current_hand.roll = ref_hand.roll
        mirror_hack()
        
    # align fingers
    hand_def = bpy.context.object.data.edit_bones["hand" + side]    
    
        #make list of fingers
    fingers = []
    
    init_selection(hand_def.name)
    bpy.ops.armature.select_similar(type='CHILDREN')
    for bone in bpy.context.selected_editable_bones[:]:
        if not "hand" in bone.name and not ".r" in bone.name:#fingers only and left side only
            fingers.append(bone.name)

    for finger in fingers:        
        init_selection(finger)
        bone_name = finger[2:-2]+"_ref"+ side
        
        if "bend_all" in finger: #exception for the "bend_all" fingers to find the ref name
            bone_name = finger[:-11]+"1_ref"+ side         
        if "thumb1_base" in finger: #thumb1 base case
            bone_name = "thumb1_ref"+ side
            
        bone_ref = bpy.context.object.data.edit_bones[bone_name]    
        current_bone = bpy.context.object.data.edit_bones[finger]
        current_bone.head = bone_ref.head
        current_bone.tail = bone_ref.tail
        current_bone.roll = bone_ref.roll  
        mirror_hack()    
   
   
    #display layers 16, 0, 1 only   
    _layers = bpy.context.object.data.layers
        #must enabling one before disabling others
    _layers[16] = True  
    for i in range(0,31):
        if i != 16:
            _layers[i] = False 
    _layers[0] = True
    _layers[1] = True   
            
    bpy.ops.object.mode_set(mode='POSE')             
    bpy.context.object.data.pose_position = 'POSE'   
    
    #reset the proxy picker state
    bpy.context.scene.Proxy_Picker.active = proxy_picker_state
    
    if debug_print == True:    
        print("\n FINISH ALIGNING ARM BONES...\n")
    

def _align_leg_bones():
    
    if debug_print == True:
        print("\n START ALIGNING LEG BONES ... \n")
    
    #disable the proxy picker to avoid bugs
    proxy_picker_state = bpy.context.scene.Proxy_Picker.active    
    try:
        bpy.context.scene.Proxy_Picker.active = False
    except:
        pass    
    
    #define the side
    side = ".l"    
     
    #get bones
    prepole_name = "leg_fk_pre_pole"
    thigh_name = "thigh_ref"
    leg_name = "leg_ref"
    foot_name = "foot_ref"
    toes_name = "toes_ref"
    fk_pole_name = "leg_fk_pole"
    ik_pole_name = "c_leg_pole"
    foot_pole_name = "foot_pole" 
    stretch_leg_name = "c_stretch_leg"
    bot_bend_name = "bot_bend_ref"
    
    legs = ["c_leg_fk"+side, "leg_fk"+side, "leg_ik_nostr"+side, "leg_ik"+side, "leg_twist"+side, "leg_stretch"+side, "leg"+side]
    
    thighs = ["c_thigh_fk"+side, "thigh_fk"+side, "thigh_ik_nostr"+side, "thigh_ik"+side, "thigh_twist"+side, "thigh_stretch"+side, "thigh"+side]
    
    feet = ["foot"+side, "foot_fk"+side, "c_foot_fk"+side, "foot_ik"+side, "c_foot_ik"+side, "foot_snap_fk"+side, "foot_ik_target"+side, "c_foot_bank_01"+side, "c_foot_bank_02"+side, "c_foot_heel"+side, "c_foot_01"+side]
        
    leg_bends = ["c_thigh_bend_contact"+side, "c_thigh_bend_01"+side, "c_thigh_bend_02"+side, "c_knee_bend"+side, "c_leg_bend_01"+side, "c_leg_bend_02"+side, "c_ankle_bend"+side]
    
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    #enable x-axis mirror edit
    bpy.context.object.data.use_mirror_x = True
    
    #select all layers
        #save current displayed layers
    _layers = bpy.context.object.data.layers
    layers_select = []
    for i in range(0,31):
        if bpy.context.object.data.layers[i] == True:    
            layers_select.append(True)
        else:
            layers_select.append(False)
        
    #display all layers for mirror to work
    for i in range(0,31):
        bpy.context.object.data.layers[i] = True
        
    #declare bones (maybe useless here)
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]   
    thigh =  bpy.context.object.data.edit_bones[thigh_name + side]
    leg =  bpy.context.object.data.edit_bones[leg_name + side]
    fk_pole =  bpy.context.object.data.edit_bones[fk_pole_name + side]
    ik_pole = bpy.context.object.data.edit_bones[ik_pole_name + side]
    
    #align every legs and thighs bones types with references locations
    for bone in thighs:
        init_selection(bone)
        current_bone = bpy.context.object.data.edit_bones[bone]
        ref_bone = bpy.context.object.data.edit_bones[thigh_name+side] 
        
        current_bone.head = ref_bone.head
        current_bone.tail = ref_bone.tail
        mirror_hack()
    
        #stretch bone    
    init_selection(stretch_leg_name+side)
    stretch_leg = get_bone(stretch_leg_name+side)
    thigh = get_bone(thigh_name+side)
    dir = stretch_leg.tail - stretch_leg.head
    stretch_leg.head = thigh.tail
    stretch_leg.tail = stretch_leg.head + dir
    mirror_hack()

    # pin controller
    init_selection("c_stretch_leg_pin"+side)
    stretch_leg_pin = get_bone("c_stretch_leg_pin"+side)
    thigh = get_bone(thigh_name+side)
    dir = stretch_leg_pin.tail - stretch_leg_pin.head
    stretch_leg_pin.head = thigh.tail
    stretch_leg_pin.tail = stretch_leg_pin.head + dir
    mirror_hack()        
        
    for bone in legs:
        init_selection(bone)
        current_bone = bpy.context.object.data.edit_bones[bone]
        ref_bone = bpy.context.object.data.edit_bones[leg_name+side]
        
        current_bone.head = ref_bone.head
        current_bone.tail = ref_bone.tail
        mirror_hack()
    
        # align secondary bones
    for bone in leg_bends:
        init_selection(bone)
        current_bone = bpy.context.object.data.edit_bones[bone]
        thigh = bpy.context.object.data.edit_bones[thigh_name+side]
        leg = bpy.context.object.data.edit_bones[leg_name+side]
        thigh_vec = thigh.tail - thigh.head
        leg_vec = leg.tail - leg.head
        length = 0.04
        if "contact" in bone: 
            current_bone.head = thigh.head + thigh_vec*0.15
            current_bone.tail = current_bone.head + thigh.y_axis * length
        if "thigh_bend_01" in bone:            
            current_bone.head = thigh.head + thigh_vec*0.4
            current_bone.head[0] += -0.03
            current_bone.tail = current_bone.head + thigh.y_axis * length
        if "thigh_bend_02" in bone:            
            current_bone.head = thigh.head + thigh_vec*0.75
            current_bone.tail = current_bone.head + thigh.y_axis * length            
        if "knee" in bone:            
            current_bone.head = thigh.tail
            current_bone.tail = current_bone.head + thigh.y_axis * length
            set_draw_scale(bone[:-2], 0.6)
        if "leg_bend_01" in bone:           
            current_bone.head = leg.head + leg_vec*0.25
            current_bone.tail = current_bone.head + leg.y_axis * length
            set_draw_scale(bone[:-2], 0.8)
        if "leg_bend_02" in bone:           
            current_bone.head = leg.head + leg_vec*0.5
            current_bone.tail = current_bone.head + leg.y_axis * length
            set_draw_scale(bone[:-2], 0.7)
        if "ankle" in bone: 
            current_bone.head = leg.head + leg_vec*0.85
            current_bone.tail = current_bone.head + leg.y_axis * length
            set_draw_scale(bone[:-2], 0.7)
        
        #set roll
        bpy.ops.armature.calculate_roll(type='POS_X')    
        mirror_hack()
    
    
    #align FK pre-pole
    init_selection(prepole_name+side)       
    
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]
    thigh =  bpy.context.object.data.edit_bones[thigh_name + side]
    leg =  bpy.context.object.data.edit_bones[leg_name + side]
    
        # center the prepole in the middle of the chain    
    prepole.head[0] = (thigh.head[0] + leg.tail[0])/2
    prepole.head[1] = (thigh.head[1] + leg.tail[1])/2
    prepole.head[2] = (thigh.head[2] + leg.tail[2])/2
        # point toward the elbow
    prepole.tail[0] = thigh.tail[0]
    prepole.tail[1] = thigh.tail[1]
    prepole.tail[2] = thigh.tail[2]    
    
    mirror_hack()   
       
    #align FK pole
    init_selection(fk_pole_name+side)  
    
    prepole = bpy.context.object.data.edit_bones[prepole_name + side]
    fk_pole = bpy.context.object.data.edit_bones[fk_pole_name + side]
    
    prepole_dir = prepole.tail - prepole.head
    fk_pole.head = prepole.head + prepole_dir * 14
    fk_pole.tail = prepole.tail + prepole_dir * 14       
    
    mirror_hack()   
    
    #align IK pole
    init_selection(ik_pole_name+side)   
    
    fk_pole =  bpy.context.object.data.edit_bones[fk_pole_name + side]
    ik_pole = bpy.context.object.data.edit_bones[ik_pole_name + side]
    
    ik_pole.head = fk_pole.head
    ik_pole.tail = [ik_pole.head[0], ik_pole.head[1], ik_pole.head[2]+0.1]    
      
    mirror_hack()    
   
    # bone roll adjust
    init_selection(leg_name+side)  
    
    bpy.ops.armature.calculate_roll(type='POS_Z')   

    init_selection("null")  
    thigh =  bpy.context.object.data.edit_bones[thigh_name + side]
    thigh.select = True   
    bpy.context.object.data.bones.active = bpy.context.object.pose.bones[leg_name+side].bone    
    bpy.ops.armature.calculate_roll(type='ACTIVE')    
    
    mirror_hack()    
        
    #copy the roll to other bones
    init_selection("null")
    
    leg =  bpy.context.object.data.edit_bones[leg_name + side]
    thigh =  bpy.context.object.data.edit_bones[thigh_name + side]
    
    for bone in legs:        
        current_bone = bpy.context.object.data.edit_bones[bone].select = True
        bpy.context.object.data.edit_bones[bone].roll = leg.roll             
    
    for bone in thighs:
        bpy.context.object.data.edit_bones[bone].roll = thigh.roll 
    
    
    # foot poles
    init_selection(foot_pole_name+side)   
            
    foot_pole = bpy.context.object.data.edit_bones[foot_pole_name + side]
    leg =  bpy.context.object.data.edit_bones[leg_name + side]   
    
    foot_pole.head = leg.tail + leg.x_axis * 0.24 * leg.length + leg.y_axis * 0.03 * leg.length
    foot_pole.tail = foot_pole.head + leg.y_axis * 0.05
    
    foot_pole.roll = leg.roll
    
    mirror_hack() 
    
    # align feet
    feet = ["foot"+side, "foot_fk"+side, "c_foot_fk"+side, "foot_ik"+side, "c_foot_ik"+side, "foot_snap_fk"+side, "foot_ik_target"+side, "c_foot_bank_01"+side, "c_foot_bank_02"+side, "c_foot_heel"+side, "c_foot_01"+side, "c_foot_fk_scale_fix"+side]
    foot_name = "foot_ref"
    
    for foot in feet:
        if foot == "foot_fk"+side or foot == "foot_ik"+side or foot == "foot"+side:
            init_selection(foot)
            current_foot = bpy.context.object.data.edit_bones[foot]
            foot_ref = bpy.context.object.data.edit_bones[foot_name + side]
            current_foot.head = foot_ref.head
            current_foot.tail = foot_ref.tail
            current_foot.roll = foot_ref.roll
            mirror_hack()
        if foot == "c_foot_fk"+side or foot == "c_foot_ik"+side or foot == "foot_snap_fk"+side or foot == "c_foot_fk_scale_fix"+side:
            init_selection(foot)
            current_foot = bpy.context.object.data.edit_bones[foot]
            foot_ref = bpy.context.object.data.edit_bones[foot_name + side]
            current_foot.head = foot_ref.head
            current_foot.tail = foot_ref.head
            current_foot.tail[1] += -0.04
            current_foot.roll = math.radians(180)
            mirror_hack()
        if foot == "foot_ik_target"+side:
            init_selection(foot)
            current_foot = bpy.context.object.data.edit_bones[foot]
            foot_ref = bpy.context.object.data.edit_bones[foot_name + side]            
            current_foot.head = foot_ref.head
            current_foot.tail = current_foot.head - foot_ref.y_axis*0.05
            current_foot.roll = 0
            mirror_hack()
        if "bank" in foot or "foot_heel" in foot:
            init_selection(foot)
            current_foot = bpy.context.object.data.edit_bones[foot]
            foot_ref = bpy.context.object.data.edit_bones[foot[2:-2]+"_ref"+side]
            current_foot.head = foot_ref.head
            current_foot.tail = foot_ref.tail
            current_foot.roll = foot_ref.roll
            mirror_hack()
        if foot == "c_foot_01"+side:
            init_selection(foot)
            current_foot = bpy.context.object.data.edit_bones[foot]
            foot_ref = bpy.context.object.data.edit_bones[foot_name + side]    
            current_foot.head = foot_ref.tail
            current_foot.tail = current_foot.head + foot_ref.z_axis*0.05
            current_foot.roll = math.radians(180)                        
            mirror_hack()           
         
            
            
        #align foot_01_pole            
        init_selection("foot_01_pole"+side)
        current_foot = get_bone("foot_01_pole"+side)
        c_foot_01 = get_bone("c_foot_01"+side)
        current_foot.head = c_foot_01.tail + c_foot_01.y_axis * 0.05
        current_foot.tail = current_foot.head + c_foot_01.y_axis * 0.05
        current_foot.roll = math.radians(180)           
        mirror_hack()
        #align foot visual position
        init_selection("c_p_foot"+side)
        foot_ref = get_bone(foot_name + side)
        heel_ref = get_bone("foot_heel_ref" + side)   
        p_foot = get_bone("c_p_foot"+side)
        
        p_foot.head = foot_ref.head
        p_foot.head[2] = heel_ref.head[2]
        p_foot.tail = p_foot.head
        p_foot.tail[1] += -0.06
        mirror_hack()
    
    # align toes
    toes = ["c_toes_fk"+side, "c_toes_ik"+side, "toes_01_ik"+side, "c_toes_track"+side, "toes_02"+side, "c_toes_end"+side, "c_toes_end_01"+side, "toes_01"+side, ]
    
    
    for bone in toes:
        if bone == "c_toes_end"+side:
            init_selection(bone)
            current_bone = bpy.context.object.data.edit_bones[bone]
            bone_ref = bpy.context.object.data.edit_bones[bone[2:-2]+"_ref" + side]
            toes_ref = bpy.context.object.data.edit_bones[toes_name + side]
            current_bone.head = bone_ref.head
            current_bone.tail = bone_ref.tail
            current_bone.tail[2] = toes_ref.tail[2]
            current_bone.roll = bone_ref.roll
            mirror_hack()
            
        if bone == "c_toes_end_01"+side:
            init_selection(bone)
            current_bone = bpy.context.object.data.edit_bones[bone]
            c_toes_end = get_bone("toes_end_ref"+side)
            current_bone.head = c_toes_end.tail
            current_bone.tail = current_bone.head + c_toes_end.y_axis * 0.035
            current_bone.roll = math.radians(180)
            mirror_hack()
        
        if bone == "c_toes_fk"+side or bone == "c_toes_track"+side or bone == "c_toes_ik"+side:
            init_selection(bone)
            current_bone = get_bone(bone)
            bone_ref = get_bone("toes_ref" + side)
            c_toes_end = get_bone("toes_end_ref"+side)
            current_bone.head = bone_ref.head
            current_bone.tail = c_toes_end.tail
            current_bone.roll = bone_ref.roll
            mirror_hack()
            
        if bone == "toes_01_ik"+side or bone == "toes_01"+side:
            init_selection(bone)
            toes_ref = bpy.context.object.data.edit_bones[toes_name + side]
            current_bone = bpy.context.object.data.edit_bones[bone]
            c_toes_fk = bpy.context.object.data.edit_bones["c_toes_fk"+side]
            current_bone.head = toes_ref.head
            dir = c_toes_fk.tail - c_toes_fk.head
            current_bone.tail = current_bone.head + dir/3
            bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Z')
            mirror_hack()
        
        if bone == "toes_02"+side:
            init_selection(bone)
            toes_01_ik = get_bone("toes_01_ik" + side)
            current_bone = get_bone(bone)
            c_toes_fk = get_bone("c_toes_fk"+side)
            current_bone.head = toes_01_ik.tail            
            current_bone.tail = c_toes_fk.tail
            bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Z')
            mirror_hack()
            
            
    #foot roll
    init_selection("c_foot_roll"+side)
    foot_ref = bpy.context.object.data.edit_bones[foot_name+side]
    c_foot_roll = bpy.context.object.data.edit_bones["c_foot_roll"+side]
    c_foot_roll.head = foot_ref.head
    c_foot_roll.head[2] = foot_ref.tail[2]
    c_foot_roll.head[1] += 0.23
    c_foot_roll.tail = c_foot_roll.head
    c_foot_roll.tail[1] += -0.06
    mirror_hack()
    
        #cursor
    init_selection("c_foot_roll_cursor"+side)
    c_foot_roll = bpy.context.object.data.edit_bones["c_foot_roll"+side]
    c_foot_roll_cursor = bpy.context.object.data.edit_bones["c_foot_roll_cursor"+side]
    c_foot_roll_cursor.head = c_foot_roll.head
    c_foot_roll_cursor.head[2] += 0.08
    c_foot_roll_cursor.tail = c_foot_roll.tail
    c_foot_roll_cursor.tail[2] += 0.08
    mirror_hack()
    
    # align c_thigh_b
    init_selection("c_thigh_b"+side)
    c_thigh_b = bpy.context.object.data.edit_bones["c_thigh_b"+side]
    thigh_fk = bpy.context.object.data.edit_bones["thigh_fk"+side]
    dir = thigh_fk.tail - thigh_fk.head
    c_thigh_b.head = thigh_fk.head - dir/7
    c_thigh_b.tail = thigh_fk.head
    c_thigh_b.roll = thigh_fk.roll
    mirror_hack()
    
    #align bot_bend
    init_selection("c_bot_bend"+side)
    bot_ref = bpy.context.object.data.edit_bones[bot_bend_name+side]
    c_bot_bend = bpy.context.object.data.edit_bones["c_bot_bend"+side]
    dir = bot_ref.tail - bot_ref.head
    c_bot_bend.head = bot_ref.head   
    c_bot_bend.tail = bot_ref.tail - dir/2    
    mirror_hack()
    
    # reset stretchy bone length
    bpy.ops.object.mode_set(mode='OBJECT')   
    bpy.ops.object.mode_set(mode='POSE')     

    #reset the stretch
    bpy.context.object.data.pose_position = 'REST'
    full_legs = thighs + legs
    
    for bone in full_legs:
        if "twist" in bone or bone == "leg"+side or "stretch" in bone:
            bpy.ops.pose.select_all(action='DESELECT')           
            bpy.context.object.pose.bones[bone].bone.select = True
            bpy.context.object.data.bones.active = bpy.context.object.pose.bones[bone].bone
            try:
                c = bpy.context.copy()
                c["constraint"] = bpy.context.active_pose_bone.constraints['Stretch To']
                bpy.ops.constraint.stretchto_reset(c, constraint="Stretch To", owner='BONE')
            except KeyError:
                if debug_print == True:
                    print("can't reset the stretch for : "+ bone)
            #mirror
            bpy.ops.pose.select_mirror()
            try:
                c = bpy.context.copy()
                c["constraint"] = bpy.context.active_pose_bone.constraints['Stretch To']
                bpy.ops.constraint.stretchto_reset(c, constraint="Stretch To", owner='BONE')
            except KeyError:
                if debug_print == True:
                    print("can't reset the stretch for : " + bone)
    """            
    #restore the save displayed layers          
    for i in range(0,31):
        bpy.context.object.data.layers[i] = layers_select[i]
    """
    
    #display layers 16, 0, 1 only   
    _layers = bpy.context.object.data.layers
        #must enabling one before disabling others
    _layers[16] = True  
    for i in range(0,31):
        if i != 16:
            _layers[i] = False 
    _layers[0] = True
    _layers[1] = True   
                 
    bpy.context.object.data.pose_position = 'POSE'

    #reset the proxy picker state
    bpy.context.scene.Proxy_Picker.active = proxy_picker_state
    
    if debug_print == True:    
        print("\n FINISH ALIGNING LEG BONES...\n")
    
    #--END ALIGN LEGS BONES

def _align_spine_bones():
    
    if debug_print == True:
        print("\n START ALIGNING SPINE BONES ... \n")
    
    #disable the proxy picker to avoid bugs
    proxy_picker_state = bpy.context.scene.Proxy_Picker.active    
    try:
        bpy.context.scene.Proxy_Picker.active = False
    except:
        pass    
    
    #define the side
    side = ".l"    
     
    #get reference bones
    root_name = "root_ref.x"
    spine_01_name = "spine_01_ref.x"
    spine_02_name = "spine_02_ref.x"  
    neck_name = "neck_ref.x"  
    head_name = "head_ref.x"
    jaw_name = "jaw_ref.x"
    eye_name = "eye_ref"+side
    
    bpy.ops.object.mode_set(mode='EDIT')
    #enable x-axis mirror edit
    bpy.context.object.data.use_mirror_x = True
    
    #select all layers
        #save current displayed layers
    _layers = bpy.context.object.data.layers
    layers_select = []
    for i in range(0,31):
        if bpy.context.object.data.layers[i] == True:    
            layers_select.append(True)
        else:
            layers_select.append(False)
        
    #display all layers for mirror to work
    for i in range(0,31):
        bpy.context.object.data.layers[i] = True
        
        
    #align root master
    init_selection("c_root_master.x")
    c_root_master = bpy.context.object.data.edit_bones["c_root_master.x"]
    c_root_ref = bpy.context.object.data.edit_bones[root_name]
    p_root_master = bpy.context.object.data.edit_bones["c_p_root_master.x"]
    
    copy_bone_transforms(c_root_ref, c_root_master)
    get_pose_bone("c_root_master.x").custom_shape_scale = 0.1 / (c_root_master.tail[2] - c_root_master.head[2]) 
    
        # set the visual shape position
    dir = p_root_master.tail - p_root_master.head
    p_root_master.head = c_root_master.head + (c_root_master.tail-c_root_master.head)/2
    p_root_master.head[1] += -0.04
    p_root_master.tail = p_root_master.head + dir
    p_root_master.tail[1] = p_root_master.head[1]
    
    #align root
    init_selection("c_root.x")
    c_root = bpy.context.object.data.edit_bones["c_root.x"]
    root = bpy.context.object.data.edit_bones["root.x"]
    c_root_ref = bpy.context.object.data.edit_bones[root_name]
    p_root = bpy.context.object.data.edit_bones["c_p_root.x"]
    
    c_root.head = c_root_ref.tail
    c_root.tail = c_root_ref.head
    c_root.roll = c_root_ref.roll
    get_pose_bone("c_root.x").custom_shape_scale = 0.1 / abs(c_root.tail[2] - c_root.head[2]) 
    copy_bone_transforms(c_root, root)
    
        # set the visual shape position
    dir = p_root.tail - p_root.head 
    p_root.head = c_root_ref.head + (c_root_ref.tail-c_root_ref.head)/2
    p_root.head[1] += -0.04
    p_root.tail = p_root.head + dir
    p_root.tail[1] = p_root.head[1]
    p_root.roll = 0
    
        #root bend
    root_bend = get_bone("c_root_bend.x")
    dir = root_bend.tail - root_bend.head    
    root_bend.head = c_root.head +(c_root.tail - c_root.head)/2
    root_bend.tail = root_bend.head + dir
    root_bend.roll = 0
    
    #align spine 01
    init_selection("c_spine_01.x")
    c_spine_01 = bpy.context.object.data.edit_bones["c_spine_01.x"]
    spine_01 = bpy.context.object.data.edit_bones["spine_01.x"]
    spine_01_ref = bpy.context.object.data.edit_bones[spine_01_name]
    p_spine_01 = bpy.context.object.data.edit_bones["c_p_spine_01.x"]
    
    copy_bone_transforms(spine_01_ref, c_spine_01)
    copy_bone_transforms(c_spine_01, spine_01) 
    
        # set the visual shape position
    p_spine_01.head = c_spine_01.head
    p_spine_01.head[1] += -0.03
    p_spine_01.tail = p_spine_01.head + (c_spine_01.tail-c_spine_01.head)
    p_spine_01.tail[1] = p_spine_01.head[1]
    get_pose_bone("c_spine_01.x").custom_shape_scale = 0.2 / abs(p_spine_01.tail[2] - p_spine_01.head[2]) 
    
        #waist bend
    waist_bend = get_bone("c_waist_bend.x")
    waist_bend.head = p_spine_01.head
    waist_bend.tail = p_spine_01.tail - (p_spine_01.tail - p_spine_01.head)/2
    waist_bend.roll = 0
    get_pose_bone("c_waist_bend.x").custom_shape_scale = 0.15 / abs(p_spine_01.tail[2] - p_spine_01.head[2]) 
        #spine_01_bend
    spine_01_bend = get_bone("c_spine_01_bend.x")
    spine_01_bend.head = p_spine_01.tail
    spine_01_bend.tail = p_spine_01.tail - (p_spine_01.tail - p_spine_01.head)/2
    spine_01_bend.roll = 0
    get_pose_bone("c_spine_01_bend.x").custom_shape_scale = 0.075 / abs(spine_01_bend.tail[2] - spine_01_bend.head[2]) 
    
     #align spine 02
    init_selection("c_spine_02.x")
    c_spine_02 = bpy.context.object.data.edit_bones["c_spine_02.x"]
    spine_02 = bpy.context.object.data.edit_bones["spine_02.x"]
    spine_02_ref = bpy.context.object.data.edit_bones[spine_02_name]
    p_spine_02 = bpy.context.object.data.edit_bones["c_p_spine_02.x"]
    
    copy_bone_transforms(spine_02_ref, c_spine_02) 
    copy_bone_transforms(c_spine_02, spine_02) 
    get_pose_bone("c_spine_02.x").custom_shape_scale = 0.3 / abs(c_spine_02.tail[2] - c_spine_02.head[2]) 
    
        # set the visual shape position
    p_spine_02.head = c_spine_02.head + (c_spine_02.tail - c_spine_02.head)/2
    p_spine_02.head[1] += -0.04
    p_spine_02.tail = p_spine_02.head + (c_spine_02.tail-c_spine_02.head)/1.5
    p_spine_02.tail[1] = p_spine_02.head[1]    
        #spine_02_bend
    spine_02_bend = get_bone("c_spine_02_bend.x")
    spine_02_bend.head = p_spine_02.head
    spine_02_bend.tail = p_spine_02.head - (p_spine_02.tail - p_spine_02.head)/3
    spine_02_bend.roll = 0
    get_pose_bone("c_spine_02_bend.x").custom_shape_scale = 0.08/ abs(spine_02_bend.tail[2] - spine_02_bend.head[2]) 
    
    #align neck    
    init_selection("c_neck.x")
    c_neck = bpy.context.object.data.edit_bones["c_neck.x"]
    neck = bpy.context.object.data.edit_bones["neck.x"]
    c_neck_01 = bpy.context.object.data.edit_bones["c_neck_01.x"]
    p_neck = bpy.context.object.data.edit_bones["c_p_neck.x"]
    p_neck_01 = bpy.context.object.data.edit_bones["c_p_neck_01.x"]
    neck_ref = bpy.context.object.data.edit_bones[neck_name]   
    
    copy_bone_transforms(neck_ref, c_neck) 
    copy_bone_transforms(neck_ref, neck) 
    c_neck_01.head = neck_ref.head
    c_neck_01.tail = c_neck_01.head    
    
    c_neck_01.tail[1] += -neck_ref.length/3
    c_neck_01.roll = 0
    
        # set the visual shape position
    copy_bone_transforms(neck_ref, p_neck) 
    p_neck.head += (neck_ref.tail - neck_ref.head)/2
    p_neck.tail = p_neck.head + (neck_ref.tail - neck_ref.head)
    
    p_neck_01.head = neck_ref.head
    p_neck_01.head[1] += -0.07
    p_neck_01.tail = p_neck_01.head
    p_neck_01.tail[1] += -0.03
    
    #align head
    init_selection("c_head.x")
    c_head = bpy.context.object.data.edit_bones["c_head.x"]
    head_ref = bpy.context.object.data.edit_bones["head_ref.x"]
    head = bpy.context.object.data.edit_bones["head.x"]
    c_head_scale_fix = bpy.context.object.data.edit_bones["c_head_scale_fix.x"]
    c_p_head = get_bone("c_p_head.x") 
    
    copy_bone_transforms(head_ref, c_head)
    copy_bone_transforms(head_ref, head)
    copy_bone_transforms(head_ref, c_head_scale_fix)
        # set the visual shape position
    c_p_head.head = head.tail
    c_p_head.tail = c_p_head.head + (head.tail-head.head)/2
    c_p_head.roll = head.roll
    
    #align facial
        #jaw
    c_jaw = bpy.context.object.data.edit_bones["c_jawbone.x"]
    jaw_ref = bpy.context.object.data.edit_bones["jaw_ref.x"]    
    copy_bone_transforms(jaw_ref, c_jaw)
    
        #skulls
    skulls = ["c_skull_01.x", "c_skull_02.x", "c_skull_03.x"]
    
    i=0
    
    for skull in skulls:
        skull_bone = bpy.context.object.data.edit_bones[skull]
       
        head_b = bpy.context.object.data.edit_bones["head.x"]
        head_b_vec = head_b.tail - head_b.head
        
        if i == 0:           
            skull_bone.head = head_b.head
            skull_bone.tail = skull_bone.head - (head_b_vec)/3         
            skull_bone.roll = math.radians(90)
        if i == 1:                             
            skull_bone.head = head_b.head
            skull_bone.tail = skull_bone.head + (head_b_vec)/2  
            skull_bone.roll = 0
        if i == 2:                             
            skull_bone.head = head_b.head + (head_b_vec)/2  
            skull_bone.tail = head_b.tail
            skull_bone.roll = 0
 
        i += 1
        
       
        
        #cheeks
    cheeks = ["c_cheek_smile"+side, "c_cheek_inflate"+side]
    for cheek in cheeks:
        init_selection(cheek)
        cheek_ref = get_bone(cheek[2:-2]+"_ref"+side)
        cheek_bone = get_bone(cheek)
        copy_bone_transforms(cheek_ref, cheek_bone)
        mirror_hack()
    
        #nose
    noses = ["c_nose_01.x", "c_nose_02.x", "c_nose_03.x"]
    for nose in noses:
        nose_bone = bpy.context.object.data.edit_bones[nose]
        nose_ref = bpy.context.object.data.edit_bones[nose[2:-2]+"_ref.x"]
        copy_bone_transforms(nose_ref, nose_bone)
        
    chins = ["c_chin_01.x", "c_chin_02.x"]
    for chin in chins:
        bone = bpy.context.object.data.edit_bones[chin]
        ref_bone = get_bone(chin[2:-2]+"_ref.x")
        copy_bone_transforms(ref_bone, bone)
        
        #mouth
    tongs = ["c_tong_01.x", "c_tong_02.x", "c_tong_03.x"]
    for tong in tongs:        
        current_bone = get_bone(tong)
        copy_bone_transforms(get_bone(tong[2:-2]+"_ref.x"), current_bone)
        copy_bone_transforms(get_bone(tong[2:-2]+"_ref.x"), get_bone(tong[2:]))
        
    teeth = ["c_teeth_top.x", "c_teeth_bot.x"]
    for tooth in teeth:        
        current_bone = get_bone(tooth)
        copy_bone_transforms(get_bone(tooth[2:-2]+"_ref.x"), current_bone)
        
    lips = ["c_lips_top.x", "c_lips_bot.x", "c_lips_top"+side, "c_lips_top_01"+side, "c_lips_bot"+side, "c_lips_bot_01"+side, "c_lips_smile"+side, "c_lips_corner_mini"+side, "c_lips_roll_top.x", "c_lips_roll_bot.x"]
    for bone in lips:
        _side = side
        if bone[-2:] == ".x":
            _side = ".x"
        init_selection(bone)
        current_bone = get_bone(bone)
        copy_bone_transforms(get_bone(bone[2:-2]+"_ref" + _side), current_bone)
        mirror_hack()
            
        
        #eyes
            #make list of all eyes bones
    eyes = []
    init_selection("c_eye_offset.l")
    bpy.ops.armature.select_similar(type='CHILDREN')
    for bone in bpy.context.selected_editable_bones[:]:
        if not ".r" in bone.name:#left side only
            eyes.append(bone.name)    
    
    eye_additions = ["c_eye"+side, "c_eye_ref_track"+side, "c_eyelid_base"+side, "eye_ref"+side]
    
        #direct copy from ref 
    for bone in eyes:        
        init_selection(bone)
        try:
            bone_ref = bpy.context.object.data.edit_bones[bone[2:-2]+"_ref"+ side]
            current_bone = bpy.context.object.data.edit_bones[bone]
            copy_bone_transforms(bone_ref, current_bone)
        except:
            pass
        
        if "eyelid_top"+side in bone:
            copy_bone_transforms(get_bone("eyelid_top_ref"+side), get_bone("eyelid_top"+side))
        if "eyelid_bot"+side in bone:
            copy_bone_transforms(get_bone("eyelid_bot_ref"+side), get_bone("eyelid_bot"+side))       
        mirror_hack()
    
        #  additional bones   
    for bone in eye_additions:        
        init_selection(bone)
        current_bone = get_bone(bone)      
        eye_ref_ref = get_bone("eye_offset_ref"+side)
        copy_bone_transforms(eye_ref_ref, current_bone)
        
        if "eye_ref"+side in bone:
            current_bone.head = eye_ref_ref.tail + (eye_ref_ref.tail-eye_ref_ref.head)
            current_bone.tail = current_bone.head
            current_bone.tail[2] += -0.006
        mirror_hack()   
     
        # eye shape scale    
    get_pose_bone("c_eye.l").custom_shape_scale = 0.8
    get_pose_bone("c_eye.r").custom_shape_scale = 0.8
    
        # eye targets
    eye_target_x = get_bone("c_eye_target.x")
    eye_ref = get_bone("eye_offset_ref"+side)
            # .x
    eye_target_x.head = eye_ref.head
    eye_target_x.head[0] = 0.0
    eye_target_x.head[1] += -1
    eye_target_x.tail = eye_target_x.head
    eye_target_x.tail[2] += 0.028
    
            # .l and .r
    init_selection("c_eye_target"+side)
    eye_target_side = get_bone("c_eye_target"+side)
    eye_target_x = get_bone("c_eye_target.x")
    eye_ref = get_bone("eye_offset_ref"+side)
    
    eye_target_side.head = eye_target_x.head
    eye_target_side.head[0] = eye_ref.head[0]
    eye_target_side.tail = eye_target_side.head
    eye_target_side.tail[2] = eye_target_x.tail[2]
    mirror_hack()
        
   # breast
    breasts = ["c_breast_01"+side, "c_breast_02"+side]
    # test if has breast 
    has_breast = False
    try:
        breast_02 = get_bone("c_breast_02"+side)
        has_breast = True
    except:
        has_breast = False
        
    if has_breast == True: 
        breast_dyn = get_bone("breast_dyn.x") 
        dist = breast_dyn.head[1] - get_bone("c_breast_01"+side).head[1]
        dir = breast_dyn.tail - breast_dyn.head
            
        for bone in breasts:
            init_selection(bone)
            current_bone = get_bone(bone)
            mirror_bone = get_bone(bone[:-2]+".r")
            
            if bpy.context.object.rig_gender == 'male':
                current_bone.layers[22] = True              
                mirror_bone.layers[22] = True
                current_bone.layers[0] = False              
                mirror_bone.layers[0] = False
                current_bone.use_deform = False
                mirror_bone.use_deform = False
            if bpy.context.object.rig_gender == 'female':
                current_bone.layers[0] = True
                mirror_bone.layers[0] = True
                current_bone.layers[22] = False              
                mirror_bone.layers[22] = False
                current_bone.use_deform = True
                mirror_bone.use_deform = True  
                
            try:
                ref_bone = get_bone(bone[2:-2] + "_ref" + side)
                copy_bone_transforms(ref_bone, current_bone)
                mirror_hack()
            except:
                if debug_print == True:
                    print("no breast ref, skip it")
           
        #dynamic        
        breast_dyn = get_bone("breast_dyn.x") 
        breast_dyn.head = get_bone("c_breast_01"+side).head
        breast_dyn.head[0] = 0
        breast_dyn.head[1] += dist
        breast_dyn.tail = breast_dyn.head + dir
        
        if bpy.context.object.rig_gender == 'female':           
            breast_dyn.layers[0] = True  
            breast_dyn.layers[22] = False
            
        if bpy.context.object.rig_gender == 'male':
            breast_dyn.layers[22] = True          
            breast_dyn.layers[0] = False
                
        #proxy bones
        breast_proxy = ["c_breast_01_proxy", "c_breast_02_proxy"]
        
        for b_proxy in breast_proxy:    
            if bpy.context.object.rig_gender == 'female':
                #get_bone(b_proxy+".l").hide = False
                #get_bone(b_proxy+".r").hide = False
                if "01" in b_proxy:
                    switch_bone_layer(b_proxy, 22, 0, True)                    
                if "02" in b_proxy:
                    switch_bone_layer(b_proxy, 22, 1, True)
                    
            if bpy.context.object.rig_gender == 'male':
                #get_bone(b_proxy+".l").hide = True
                #get_bone(b_proxy+".r").hide = True      
                if "01" in b_proxy:
                    switch_bone_layer(b_proxy, 0, 22, True)                                                 
                if "02" in b_proxy:
                    switch_bone_layer(b_proxy, 1, 22, True)
    
    # eyebrows
    eyebrows = []
        # make list of eyebrows
    init_selection("eyebrow_full_ref"+side)
    bpy.ops.armature.select_similar(type='CHILDREN')
    for bone in bpy.context.selected_editable_bones[:]:
        if not ".r" in bone.name:#fingers only and left side only
            eyebrows.append(bone.name)
            
    for eyebrow in eyebrows:        
        init_selection("c_" + eyebrow[:-6]+ side)
        current_bone = get_bone("c_" + eyebrow[:-6]+ side)
        bone_ref = get_bone(eyebrow)
        current_bone.head = bone_ref.head
        current_bone.tail = bone_ref.tail
        current_bone.roll = bone_ref.roll  
        mirror_hack()
            
   
    #display layers 16, 0, 1 only   
    _layers = bpy.context.object.data.layers
        #must enabling one before disabling others
    _layers[16] = True  
    for i in range(0,31):
        if i != 16:
            _layers[i] = False 
    _layers[0] = True
    _layers[1] = True   
     
    
    #switch pose state and mode
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.object.data.pose_position = 'POSE'   
    
    if debug_print == True:    
        print("\n FINISH ALIGNING SPINE BONES...\n")
    
    if debug_print == True:
        print("\n COPY BONES TO RIG ADD ")
    
    copy_bones_to_rig_add()
    
    if debug_print == True:
        print("\n FINISHED COPYING TO RIG ADD ")
    
    #reset the proxy picker state
    bpy.context.scene.Proxy_Picker.active = proxy_picker_state    
    
    #--END ALIGN SPINE BONES
    
def switch_bone_layer(bone, base_layer, dest_layer, mirror):
    
    if mirror == False:
        get_bone(bone).layers[dest_layer] = True
        get_bone(bone).layers[base_layer] = False
    
    if mirror == True:
        get_bone(bone+".l").layers[dest_layer] = True
        get_bone(bone+".l").layers[base_layer] = False
        get_bone(bone+".r").layers[dest_layer] = True
        get_bone(bone+".r").layers[base_layer] = False                          
    
def mirror_hack():
    bpy.ops.transform.translate(value=(0, 0, 0), constraint_orientation='NORMAL', proportional='DISABLED')

def init_selection(active_bone):
    try:
        bpy.ops.armature.select_all(action='DESELECT')
    except:
        pass
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    if (active_bone != "null"):
        bpy.context.object.data.bones.active = bpy.context.object.pose.bones[active_bone].bone #set the active bone for mirror
    bpy.ops.object.mode_set(mode='EDIT')
    
 
def get_pose_bone(name):  
    return bpy.context.object.pose.bones[name]

def set_draw_scale(name, size):
    bone = bpy.context.object.pose.bones[name+".l"]
    bone.custom_shape_scale = size
    bone_mirror = bpy.context.object.pose.bones[name+".r"]
    bone_mirror.custom_shape_scale = size
    
def get_bone(name):
    return bpy.context.object.data.edit_bones[name]
    
def copy_bone_transforms(bone1, bone2):
    bone2.head = bone1.head
    bone2.tail = bone1.tail
    bone2.roll = bone1.roll
    
def copy_bones_to_rig_add():
    bpy.data.objects["rig_add"].hide = False
    armature1 = bpy.data.objects["rig"]
    armature2 = bpy.data.objects["rig_add"]
    
    bone_data = {}
    
    edit_rig(armature1)
    #make dictionnary of bones transforms in armature 1
    for bone in armature1.data.edit_bones:
        bone_data[bone.name] = (bone.head.copy(), bone.tail.copy(), bone.roll)
        
    edit_rig(armature2)
    #apply the bones transforms to the armature
    for bone in armature2.data.edit_bones:
        try:
            bone.head, bone.tail, bone.roll = bone_data[bone.name]
        except:
            pass
        
    bpy.ops.object.mode_set(mode='OBJECT')
    armature2.hide = True
    bpy.context.scene.objects.active = armature1
    #armature1.select = True
    bpy.ops.object.mode_set(mode='POSE')

def edit_rig(rig):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    rig.select = True
    bpy.context.scene.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')


# END FUNCTIONS


###########  UI PANEL  ###################

class proxy_utils_ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Auto-Rig Pro"
    bl_idname = "id_auto_rig"
    
    @classmethod
    # buttons visibility conditions
    
    def poll(cls, context):
        if bpy.context.active_object is not None:
            if context.mode == 'POSE' or context.mode == 'OBJECT' or context.mode == 'EDIT':
                return True
            else:
                return False
        else:
            return False
        
    def draw(self, context):
        layout = self.layout
        object = context.object
        scene = context.scene
        col = layout.column(align=False)
        #BUTTONS
        layout.label("Rig Type:")
        layout.prop(object, "rig_gender", expand=True)
        
        layout.separator()  
        layout.operator("id.edit_ref", text="Edit Reference Bones", icon = 'EDIT')
        layout.separator()  
        
        
        layout.operator("id.align_all_bones", text="Match to Rig", icon = 'POSE_HLT')
        #layout.operator("id.align_arm_bones", text="Match Arms")
        #layout.operator("id.align_leg_bones", text="Match Legs")
        #layout.operator("id.align_spine_bones", text="Match Spine")
             
        layout.separator()
        layout.label("Mesh Binding:")
        row = layout.column(align=True).row(align=True)        
        row.operator("id.bind_to_rig", text="Bind")
        row.operator("id.unbind_to_rig", text="Unbind")     
        layout.separator()
        layout.operator("id.set_picker_camera", text="Set Rig UI Cam", icon = 'CAMERA_DATA')
        layout.separator()
        
        layout.label("Driver Creation Tools:")
        layout.prop(object, "driver_bone")
        layout.prop(object, "driver_transform")
        layout.operator("id.create_driver", text="Create Driver")     
    
    
###########  REGISTER  ##################

def register():  
    bpy.types.Object.rig_gender = bpy.props.EnumProperty(items=(('male', 'Male', 'Male rig type'),('female', 'Female', 'Female rig type')), name = "rig gender")
    bpy.types.Object.driver_bone = bpy.props.StringProperty(name="Bone Name", description="Bone driving the shape key")
    bpy.types.Object.driver_transform = bpy.props.EnumProperty(items=(('LOC_X', 'Loc X', 'X Location'),('LOC_Y', 'Loc Y', 'Y Location'), ('LOC_Z', 'Loc Z', 'Z Location'), ('ROT_X', 'Rot X', 'X Rotation'), ('ROT_Y', 'Rot Y', 'Y Rotation'), ('ROT_Z', 'Rot Z', 'Z Rotation'), ('SCALE_X', 'Scale X', 'X Scale'), ('SCALE_Y', 'Scale Y', 'Y Scale'), ('SCALE_Z', 'Scale Z', 'Z Scale')), name = "Bone Transform")
    
def unregister():  
    del bpy.types.Object.rig_gender
    del bpy.types.Object.driver_bone
    del bpy.types.Object.driver_transform