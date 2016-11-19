import bpy
from mathutils import Matrix, Vector
from math import acos, pi


############################
## Math utility functions ##
############################
rig_id = ""

def perpendicular_vector(v):
    """ Returns a vector that is perpendicular to the one given.
        The returned vector is _not_ guaranteed to be normalized.
    """
    # Create a vector that is not aligned with v.
    # It doesn't matter what vector.  Just any vector
    # that's guaranteed to not be pointing in the same
    # direction.
    if abs(v[0]) < abs(v[1]):
        tv = Vector((1,0,0))
    else:
        tv = Vector((0,1,0))

    # Use cross prouct to generate a vector perpendicular to
    # both tv and (more importantly) v.
    return v.cross(tv)


def rotation_difference(mat1, mat2):
    """ Returns the shortest-path rotational difference between two
        matrices.
    """
    q1 = mat1.to_quaternion()
    q2 = mat2.to_quaternion()
    angle = acos(min(1,max(-1,q1.dot(q2)))) * 2
    if angle > pi:
        angle = -angle + (2*pi)
    return angle


#########################################
## "Visual Transform" helper functions ##
#########################################

def get_pose_matrix_in_other_space(mat, pose_bone):
    """ Returns the transform matrix relative to pose_bone's current
        transform space.  In other words, presuming that mat is in
        armature space, slapping the returned matrix onto pose_bone
        should give it the armature-space transforms of mat.
        TODO: try to handle cases with axis-scaled parents better.
    """
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()
    if pose_bone.parent:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    # Get matrix in bone's current transform space
    smat = rest_inv * (par_rest * (par_inv * mat))

    # Compensate for non-local location
    #if not pose_bone.bone.use_local_location:
    #    loc = smat.to_translation() * (par_rest.inverted() * rest).to_quaternion()
    #    smat.translation = loc

    return smat


def get_local_pose_matrix(pose_bone):
    """ Returns the local transform matrix of the given pose bone.
    """
    return get_pose_matrix_in_other_space(pose_bone.matrix, pose_bone)


def set_pose_translation(pose_bone, mat):
    """ Sets the pose bone's translation to the same translation as the given matrix.
        Matrix should be given in bone's local space.
    """
    if pose_bone.bone.use_local_location == True:
        pose_bone.location = mat.to_translation()
    else:
        loc = mat.to_translation()

        rest = pose_bone.bone.matrix_local.copy()
        if pose_bone.bone.parent:
            par_rest = pose_bone.bone.parent.matrix_local.copy()
        else:
            par_rest = Matrix()

        q = (par_rest.inverted() * rest).to_quaternion()
        pose_bone.location = q * loc


def set_pose_rotation(pose_bone, mat):
    """ Sets the pose bone's rotation to the same rotation as the given matrix.
        Matrix should be given in bone's local space.
    """
    q = mat.to_quaternion()

    if pose_bone.rotation_mode == 'QUATERNION':
        pose_bone.rotation_quaternion = q
    elif pose_bone.rotation_mode == 'AXIS_ANGLE':
        pose_bone.rotation_axis_angle[0] = q.angle
        pose_bone.rotation_axis_angle[1] = q.axis[0]
        pose_bone.rotation_axis_angle[2] = q.axis[1]
        pose_bone.rotation_axis_angle[3] = q.axis[2]
    else:
        pose_bone.rotation_euler = q.to_euler(pose_bone.rotation_mode)


def set_pose_scale(pose_bone, mat):
    """ Sets the pose bone's scale to the same scale as the given matrix.
        Matrix should be given in bone's local space.
    """
    pose_bone.scale = mat.to_scale()


def match_pose_translation(pose_bone, target_bone):
    """ Matches pose_bone's visual translation to target_bone's visual
        translation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_translation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_rotation(pose_bone, target_bone):
    """ Matches pose_bone's visual rotation to target_bone's visual
        rotation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_rotation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_scale(pose_bone, target_bone):
    """ Matches pose_bone's visual scale to target_bone's visual
        scale.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_scale(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


##############################
## IK/FK snapping functions ##
##############################

def match_pole_target(ik_first, ik_last, pole, match_bone, length):
    """ Places an IK chain's pole target to match ik_first's
        transforms to match_bone.  All bones should be given as pose bones.
        You need to be in pose mode on the relevant armature object.
        ik_first: first bone in the IK chain
        ik_last:  last bone in the IK chain
        pole:  pole target bone for the IK chain
        match_bone:  bone to match ik_first to (probably first bone in a matching FK chain)
        length:  distance pole target should be placed from the chain center
    """
    a = ik_first.matrix.to_translation()
    b = ik_last.matrix.to_translation() + ik_last.vector

    # Vector from the head of ik_first to the
    # tip of ik_last
    ikv = b - a

    # Get a vector perpendicular to ikv
    pv = perpendicular_vector(ikv).normalized() * length

    def set_pole(pvi):
        """ Set pole target's position based on a vector
            from the arm center line.
        """
        # Translate pvi into armature space
        ploc = a + (ikv/2) + pvi

        # Set pole target to location
        mat = get_pose_matrix_in_other_space(Matrix.Translation(ploc), pole)
        set_pose_translation(pole, mat)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    set_pole(pv)

    # Get the rotation difference between ik_first and match_bone
    angle = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Try compensating for the rotation difference in both directions
    pv1 = Matrix.Rotation(angle, 4, ikv) * pv
    set_pole(pv1)
    ang1 = rotation_difference(ik_first.matrix, match_bone.matrix)

    pv2 = Matrix.Rotation(-angle, 4, ikv) * pv
    set_pole(pv2)
    ang2 = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Do the one with the smaller angle
    if ang1 < ang2:
        set_pole(pv1)    


def fk2ik_arm(obj, fk, ik):
    """ Matches the fk bones in an arm rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]
    switch = obj.pose.bones[ik[3]]
    pole = obj.pose.bones[ik[4]]

    # Stretch
    if handi['auto_stretch'] == 0.0:
        hand['stretch_length'] = handi['stretch_length']
    else:
        diff = (uarmi.vector.length + farmi.vector.length) / (uarm.vector.length + farm.vector.length)
        hand['stretch_length'] *= diff

    # Upper arm snap
    match_pose_rotation(uarm, uarmi)
    #match_pose_scale(uarm, uarmi)

    # Forearm snap
    match_pose_rotation(farm, farmi)
    #match_pose_scale(farm, farmi)

    # Hand snap
    match_pose_rotation(hand, handi)
    
    hand.scale[0]=handi.scale[0]
    hand.scale[1]=handi.scale[1]
    hand.scale[2]=handi.scale[2]
    
    #rot debug
    farm.rotation_euler[0]=0
    farm.rotation_euler[1]=0
    
    #switch
    switch['ik_fk_switch'] = 1.0
    
    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
        #fk chain
        switch.keyframe_insert(data_path='["ik_fk_switch"]')
        hand.keyframe_insert(data_path='["stretch_length"]')
        hand.keyframe_insert(data_path="scale")
        hand.keyframe_insert(data_path="rotation_euler")
        uarm.keyframe_insert(data_path="rotation_euler")
        farm.keyframe_insert(data_path="rotation_euler")
                
        #ik chain
        handi.keyframe_insert(data_path='["stretch_length"]')
        handi.keyframe_insert(data_path='["auto_stretch"]')
        handi.keyframe_insert(data_path="location")
        handi.keyframe_insert(data_path="rotation_euler")
        handi.keyframe_insert(data_path="scale")
        pole.keyframe_insert(data_path="location")
        

    


def ik2fk_arm(obj, fk, ik):
    """ Matches the ik bones in an arm rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    polefk = obj.pose.bones[fk[3]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]
    pole  = obj.pose.bones[ik[3]]
    switch = obj.pose.bones[ik[4]]
 

    # Stretch
    handi['stretch_length'] = hand['stretch_length']
    
    # Hand position
    match_pose_translation(handi, hand)
    match_pose_rotation(handi, hand)
    
    # Hand scale
    handi.scale[0]=hand.scale[0]
    handi.scale[1]=hand.scale[1]
    handi.scale[2]=hand.scale[2]

    # Pole target position
    match_pose_translation(pole, polefk)    
    
    #switch
    switch['ik_fk_switch'] = 0.0
    
     #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
        #ik chain
        switch.keyframe_insert(data_path='["ik_fk_switch"]')
        handi.keyframe_insert(data_path='["stretch_length"]')
        handi.keyframe_insert(data_path='["auto_stretch"]')
        handi.keyframe_insert(data_path="location")
        handi.keyframe_insert(data_path="rotation_euler")
        handi.keyframe_insert(data_path="scale")
        pole.keyframe_insert(data_path="location")
        
        #fk chain
        hand.keyframe_insert(data_path='["stretch_length"]')
        hand.keyframe_insert(data_path="location")        
        hand.keyframe_insert(data_path="rotation_euler")
        hand.keyframe_insert(data_path="scale")
        uarm.keyframe_insert(data_path="rotation_euler")
        farm.keyframe_insert(data_path="rotation_euler")
        
        
          


def fk2ik_leg(obj, fk, ik):
    """ Matches the fk bones in an arm rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh  = obj.pose.bones[fk[0]]
    leg  = obj.pose.bones[fk[1]]
    foot  = obj.pose.bones[fk[2]]
    toes = obj.pose.bones[fk[3]]
    thighi = obj.pose.bones[ik[0]]
    legi = obj.pose.bones[ik[1]]
    footi = obj.pose.bones[ik[2]]    
    toesi = obj.pose.bones[ik[3]]
    footi_rot = obj.pose.bones[ik[4]]
    switch = obj.pose.bones[ik[5]]
    foot_01 = obj.pose.bones[ik[6]]
    foot_roll = obj.pose.bones[ik[7]]
    pole = obj.pose.bones[ik[8]]


    # Stretch
    if footi['auto_stretch'] == 0.0:
        foot['stretch_length'] = footi['stretch_length']
    else:
        diff = (thighi.vector.length + legi.vector.length) / (thigh.vector.length + leg.vector.length)
        foot['stretch_length'] *= diff

    # Thigh snap
    match_pose_rotation(thigh, thighi)

    # Leg snap
    match_pose_rotation(leg, legi)    

    # Foot snap
    match_pose_rotation(foot, footi_rot)
        #scale    
    foot.scale[0]=footi.scale[0]
    foot.scale[1]=footi.scale[1]
    foot.scale[2]=footi.scale[2]
    
    
    #Toes snap
    match_pose_rotation(toes, toesi)
        #scale
    toes.scale[0]=toesi.scale[0]
    toes.scale[1]=toesi.scale[1]
    toes.scale[2]=toesi.scale[2]    

    #rotation debug
    leg.rotation_euler[0]=0
    leg.rotation_euler[1]=0
    
     #switch
    switch['ik_fk_switch'] = 1.0
    
    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
        #fk chain
        switch.keyframe_insert(data_path='["ik_fk_switch"]')
        foot.keyframe_insert(data_path='["stretch_length"]')
        foot.keyframe_insert(data_path="scale")
        foot.keyframe_insert(data_path="rotation_euler")
        thigh.keyframe_insert(data_path="rotation_euler")
        leg.keyframe_insert(data_path="rotation_euler")
        toes.keyframe_insert(data_path="rotation_euler")
        toes.keyframe_insert(data_path="scale")
        
        #ik chain        
        footi.keyframe_insert(data_path='["stretch_length"]')
        footi.keyframe_insert(data_path='["auto_stretch"]')
        footi.keyframe_insert(data_path="location")
        footi.keyframe_insert(data_path="rotation_euler")
        footi.keyframe_insert(data_path="scale")
        foot_01.keyframe_insert(data_path="rotation_euler")
        foot_roll.keyframe_insert(data_path="location")       
        toesi.keyframe_insert(data_path="rotation_euler")
        toesi.keyframe_insert(data_path="scale")        
        pole.keyframe_insert(data_path="location")
  

def ik2fk_leg(obj, fk, ik):
    """ Matches the ik bones in an arm rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh  = obj.pose.bones[fk[0]]
    leg  = obj.pose.bones[fk[1]]
    foot  = obj.pose.bones[fk[2]]
    toes = obj.pose.bones[fk[3]]
    polefk = obj.pose.bones[fk[4]]
    thighi = obj.pose.bones[ik[0]]
    legi = obj.pose.bones[ik[1]]
    footi = obj.pose.bones[ik[2]]
    pole  = obj.pose.bones[ik[3]]
    toesi = obj.pose.bones[ik[4]]
    foot_01 = obj.pose.bones[ik[5]]
    foot_roll = obj.pose.bones[ik[6]]
    switch = obj.pose.bones[ik[7]]

    # Stretch
    footi['stretch_length'] = foot['stretch_length']
   
    #reset IK foot_01 and foot_roll
    foot_01.rotation_euler[0]=0
    foot_roll.location[0]=0
    foot_roll.location[2]=0
    
    # foot snap
    match_pose_translation(footi, foot)
    match_pose_rotation(footi, foot)
    
        #scale
    footi.scale[0]=foot.scale[0]
    footi.scale[1]=foot.scale[1]
    footi.scale[2]=foot.scale[2]
    
    #toes snap    
    match_pose_rotation(toesi, toes)
        #scale
    toesi.scale[0]=toes.scale[0]
    toesi.scale[1]=toes.scale[1]
    toesi.scale[2]=toes.scale[2] 

    # Pole target position
    match_pose_translation(pole, polefk)
    
     #switch
    switch['ik_fk_switch'] = 0.0
    
    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
        #ik chain
        switch.keyframe_insert(data_path='["ik_fk_switch"]')
        footi.keyframe_insert(data_path='["stretch_length"]')
        foot_01.keyframe_insert(data_path="rotation_euler")
        foot_roll.keyframe_insert(data_path="location")
        footi.keyframe_insert(data_path='["auto_stretch"]')
        footi.keyframe_insert(data_path="location")
        footi.keyframe_insert(data_path="rotation_euler")
        footi.keyframe_insert(data_path="scale")
        toesi.keyframe_insert(data_path="rotation_euler")
        toesi.keyframe_insert(data_path="scale")        
        pole.keyframe_insert(data_path="location")
        
        #fk chain
        foot.keyframe_insert(data_path='["stretch_length"]')
        foot.keyframe_insert(data_path="rotation_euler")
        foot.keyframe_insert(data_path="scale")
        thigh.keyframe_insert(data_path="rotation_euler")
        leg.keyframe_insert(data_path="rotation_euler")
        toes.keyframe_insert(data_path="rotation_euler")
        toes.keyframe_insert(data_path="scale")



##############################
## IK/FK snapping operators ##
##############################

class Rigify_Arm_FK2IK(bpy.types.Operator):
    """ Snaps an FK arm to an IK arm.
    """
    bl_idname = "pose.rigify_arm_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK arm to IK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")
    pole    = bpy.props.StringProperty(name="Pole IK Name")
    switch = bpy.props.StringProperty(name="Switch Name")
    

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik, self.switch, self.pole])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Arm_IK2FK(bpy.types.Operator):
    """ Snaps an IK arm to an FK arm.
    """
    bl_idname = "pose.rigify_arm_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK arm to FK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")
    pole_fk = bpy.props.StringProperty(name="Pole FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")
    pole    = bpy.props.StringProperty(name="Pole IK Name")
    switch = bpy.props.StringProperty(name="Switch Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk, self.pole_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik, self.pole, self.switch])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_FK2IK(bpy.types.Operator):
    """ Snaps an FK leg to an IK leg.
    """
    bl_idname = "pose.rigify_leg_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK leg to IK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    leg_fk  = bpy.props.StringProperty(name="Shin FK Name")
    foot_fk  = bpy.props.StringProperty(name="Foot FK Name")
    toes_fk = bpy.props.StringProperty(name="Toes FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    leg_ik  = bpy.props.StringProperty(name="Shin IK Name")    
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    foot_01 = bpy.props.StringProperty(name="Foot_01 IK Name")
    foot_roll = bpy.props.StringProperty(name="Foot_roll IK Name")
    toes_ik = bpy.props.StringProperty(name="Toes IK Name")
    foot_ik_rot = bpy.props.StringProperty(name="Foot IK Name")    
    pole = bpy.props.StringProperty(name="Pole IK  Name")
    switch = bpy.props.StringProperty(name="Switch Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_leg(context.active_object, fk=[self.thigh_fk, self.leg_fk, self.foot_fk, self.toes_fk], ik=[self.thigh_ik, self.leg_ik, self.foot_ik, self.toes_ik, self.foot_ik_rot, self.switch, self.foot_01, self.foot_roll, self.pole])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_IK2FK(bpy.types.Operator):
    """ Snaps an IK leg to an FK leg.
    """
    bl_idname = "pose.rigify_leg_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK leg to FK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    leg_fk = bpy.props.StringProperty(name="Shin FK Name")
    foot_fk = bpy.props.StringProperty(name="Foot FK Name")
    toes_fk = bpy.props.StringProperty(name="Toes FK Name")
    pole_fk = bpy.props.StringProperty(name="Pole FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    leg_ik = bpy.props.StringProperty(name="Shin IK Name")    
    foot_ik = bpy.props.StringProperty(name="Foot IK Name")
    pole = bpy.props.StringProperty(name="Pole IK Name")
    toes_ik = bpy.props.StringProperty(name="Toes IK Name")
    foot_01= bpy.props.StringProperty(name="Foot01 IK Name")
    foot_roll= bpy.props.StringProperty(name="Foot_roll IK Name")
    switch = bpy.props.StringProperty(name="Switch Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_leg(context.active_object, fk=[self.thigh_fk, self.leg_fk, self.foot_fk, self.toes_fk, self.pole_fk], ik=[self.thigh_ik, self.leg_ik, self.foot_ik, self.pole, self.toes_ik, self.foot_01, self.foot_roll, self.switch])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}



###################
## Rig UI Panels ##
###################

class RigUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig Main Properties"
    bl_idname = rig_id + "_PT_rig_ui"

    @classmethod
    def poll(self, context):
        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            return

        def is_selected(names):
            # Returns whether any of the named bones are selected.
            if type(names) == list:
                for name in names:
                    if name in selected_bones:
                        return True
            elif names in selected_bones:
                return True
            return False   
      
       #LEFT LEG
        fk_leg = ["c_thigh_fk.l", "c_leg_fk.l", "c_foot_fk.l", "c_toes_fk.l", "leg_fk_pole.l"]
        ik_leg = ["thigh_ik.l", "leg_ik.l","c_foot_ik.l", "c_leg_pole.l", "c_toes_ik.l", "c_foot_01.l", "c_foot_roll_cursor.l", "foot_snap_fk.l", "c_ikfk_leg.l"]
        
                        
        if is_selected(fk_leg) or is_selected(ik_leg):
            layout.label("Left Leg:")
           #stretch length property
            if is_selected(fk_leg):
                layout.prop(pose_bones["c_foot_fk.l"], '["stretch_length"]', text="Stretch Length (FK)", slider=True)            
            if is_selected(ik_leg):
                layout.prop(pose_bones["c_foot_ik.l"], '["stretch_length"]', text="Stretch Length (IK)", slider=True)
            #auto_stretch ik property
                layout.prop(pose_bones["c_foot_ik.l"], '["auto_stretch"]', text="Auto Stretch", slider=True) 
        
            layout.separator()
            layout.prop(pose_bones["c_ikfk_leg.l"], '["ik_fk_switch"]', text="IK-FK Switch", slider=True)
            p = layout.operator("pose.rigify_leg_fk2ik_" + rig_id, text="Snap FK > IK")
            p.thigh_fk = fk_leg[0]
            p.leg_fk = fk_leg[1]
            p.foot_fk = fk_leg[2]
            p.toes_fk = fk_leg[3]            
            p.thigh_ik = ik_leg[0]
            p.leg_ik  = ik_leg[1]
            p.foot_ik = ik_leg[2]
            p.pole = ik_leg[3]
            p.toes_ik = ik_leg[4]
            p.foot_01 = ik_leg[5]
            p.foot_roll = ik_leg[6]
            p.foot_ik_rot = ik_leg[7]
            p.switch = ik_leg[8]            
            p = layout.operator("pose.rigify_leg_ik2fk_" + rig_id, text="Snap IK > FK")
            p.thigh_fk = fk_leg[0]
            p.leg_fk = fk_leg[1]  
            p.foot_fk = fk_leg[2]
            p.toes_fk = fk_leg[3]
            p.pole_fk = fk_leg[4]         
            p.thigh_ik = ik_leg[0]
            p.leg_ik = ik_leg[1]
            p.foot_ik = ik_leg[2] 
            p.pole = ik_leg[3]
            p.toes_ik = ik_leg[4]
            p.foot_01 = ik_leg[5]
            p.foot_roll = ik_leg[6]
            p.switch = ik_leg[8] 

        if is_selected(fk_leg+ik_leg):
            layout.separator()
        
        #RIGHT LEG        
        fk_leg = ["c_thigh_fk.r", "c_leg_fk.r", "c_foot_fk.r", "c_toes_fk.r", "leg_fk_pole.r"]
        ik_leg = ["thigh_ik.r", "leg_ik.r", "c_foot_ik.r", "c_leg_pole.r", "c_toes_ik.r", "c_foot_01.r", "c_foot_roll_cursor.r", "foot_snap_fk.r", "c_ikfk_leg.r"]
        
                    
        if is_selected(fk_leg) or is_selected(ik_leg): 
            layout.label("Right Leg:")
           #stretch length property
            if is_selected(fk_leg):
                layout.prop(pose_bones["c_foot_fk.r"], '["stretch_length"]', text="Stretch Length (FK)", slider=True)            
            if is_selected(ik_leg):
                layout.prop(pose_bones["c_foot_ik.r"], '["stretch_length"]', text="Stretch Length (IK)", slider=True)
            #auto_stretch ik property
                layout.prop(pose_bones["c_foot_ik.r"], '["auto_stretch"]', text="Auto Stretch", slider=True) 
            
            layout.separator()            
            #Snap buttons     
            layout.prop(pose_bones["c_ikfk_leg.r"], '["ik_fk_switch"]', text="IK-FK Switch", slider=True)
            p = layout.operator("pose.rigify_leg_fk2ik_" + rig_id, text="Snap FK > IK")
            p.thigh_fk = fk_leg[0]
            p.leg_fk = fk_leg[1]
            p.foot_fk = fk_leg[2]
            p.toes_fk = fk_leg[3]             
            p.thigh_ik = ik_leg[0]
            p.leg_ik = ik_leg[1]
            p.foot_ik = ik_leg[2]
            p.pole = ik_leg[3]
            p.toes_ik = ik_leg[4]
            p.foot_01 = ik_leg[5]
            p.foot_roll = ik_leg[6]
            p.foot_ik_rot = ik_leg[7]
            p.switch = ik_leg[8]               
            p = layout.operator("pose.rigify_leg_ik2fk_" + rig_id, text="Snap IK > FK")
            p.thigh_fk = fk_leg[0]
            p.leg_fk = fk_leg[1]
            p.foot_fk = fk_leg[2]
            p.toes_fk = fk_leg[3]
            p.pole_fk = fk_leg[4]                  
            p.thigh_ik = ik_leg[0]
            p.leg_ik = ik_leg[1]
            p.foot_ik = ik_leg[2] 
            p.pole = ik_leg[3]
            p.toes_ik = ik_leg[4]
            p.foot_01 = ik_leg[5]
            p.foot_roll = ik_leg[6]
            p.switch = ik_leg[8]
           
        if is_selected(fk_leg+ik_leg):
            layout.separator()
        
        #LEFT ARM        
        fk_arm = ["c_arm_fk.l", "c_forearm_fk.l", "c_hand_fk.l", "arm_fk_pole.l"]
        ik_arm = ["arm_ik.l", "forearm_ik.l", "c_hand_ik.l", "c_arms_pole.l", "c_ikfk_arm.l"]           

            #Snap buttons
        if is_selected(fk_arm) or is_selected(ik_arm):
            layout.label("Left Arm:")
           #stretch length property
            if is_selected(fk_arm):
                layout.prop(pose_bones["c_hand_fk.l"], '["stretch_length"]', text="Stretch Length (FK)", slider=True)            
            if is_selected(ik_arm):
                layout.prop(pose_bones["c_hand_ik.l"], '["stretch_length"]', text="Stretch Length (IK)", slider=True)
            #auto_stretch ik property
                layout.prop(pose_bones["c_hand_ik.l"], '["auto_stretch"]', text="Auto Stretch", slider=True)  
        
            layout.separator() 
            layout.prop(pose_bones["c_ikfk_arm.l"], '["ik_fk_switch"]', text="IK-FK Switch", slider=True)
            props = layout.operator("pose.rigify_arm_fk2ik_" + rig_id, text="Snap FK > IK")
            props.uarm_fk = fk_arm[0]
            props.farm_fk = fk_arm[1]
            props.hand_fk = fk_arm[2]
            props.uarm_ik = ik_arm[0]
            props.farm_ik = ik_arm[1]
            props.hand_ik = ik_arm[2]
            props.pole = ik_arm[3]
            props.switch = ik_arm[4]
            props = layout.operator("pose.rigify_arm_ik2fk_" + rig_id, text="Snap IK > FK")
            props.uarm_fk = fk_arm[0]
            props.farm_fk = fk_arm[1]
            props.hand_fk = fk_arm[2]
            props.pole_fk = fk_arm[3]
            props.uarm_ik = ik_arm[0]
            props.farm_ik = ik_arm[1]
            props.hand_ik = ik_arm[2]
            props.pole = ik_arm[3]
            props.switch = ik_arm[4]      

        if is_selected(fk_arm+ik_arm):
            layout.separator()
            
         #RIGHT ARM            
        fk_arm = ["c_arm_fk.r", "c_forearm_fk.r", "c_hand_fk.r", "arm_fk_pole.r"]
        ik_arm = ["arm_ik.r", "forearm_ik.r", "c_hand_ik.r", "c_arms_pole.r", "c_ikfk_arm.r"]          
       
        if is_selected(fk_arm) or is_selected(ik_arm):
            layout.label("Right Arm:")
           #stretch length property
            if is_selected(fk_arm):
                layout.prop(pose_bones["c_hand_fk.r"], '["stretch_length"]', text="Stretch Length (FK)", slider=True)            
            if is_selected(ik_arm):
                layout.prop(pose_bones["c_hand_ik.r"], '["stretch_length"]', text="Stretch Length (IK)", slider=True)
            #auto_stretch ik property
                layout.prop(pose_bones["c_hand_ik.r"], '["auto_stretch"]', text="Auto Stretch", slider=True)     
            
            layout.separator()
            #Snap buttons          
            layout.prop(pose_bones["c_ikfk_arm.r"], '["ik_fk_switch"]', text="IK-FK Switch", slider=True)
            props = layout.operator("pose.rigify_arm_fk2ik_" + rig_id, text="Snap FK > IK")            
            props.uarm_fk = fk_arm[0]
            props.farm_fk = fk_arm[1]
            props.hand_fk = fk_arm[2]
            props.uarm_ik = ik_arm[0]
            props.farm_ik = ik_arm[1]
            props.hand_ik = ik_arm[2]
            props.pole = ik_arm[3]
            props.switch = ik_arm[4]
            props = layout.operator("pose.rigify_arm_ik2fk_" + rig_id, text="Snap IK > FK")
            props.uarm_fk = fk_arm[0]
            props.farm_fk = fk_arm[1]
            props.hand_fk = fk_arm[2]
            props.pole_fk = fk_arm[3]
            props.uarm_ik = ik_arm[0]
            props.farm_ik = ik_arm[1]
            props.hand_ik = ik_arm[2]
            props.pole = ik_arm[3]
            props.switch = ik_arm[4]
       
        if is_selected(fk_arm+ik_arm):
            layout.separator()
            
        # EYE AIM        
        eye_aim_bones = ["c_eye_target.x", "c_eye_target.l", "c_eye_target.r", "c_eye.l", "c_eye.r"]
        if is_selected(eye_aim_bones):
            layout.prop(pose_bones["c_eye_target.x"], '["eye_target"]', text="Eye target follow", slider=True)
            
        # FINGERS BEND
        
        thumb_l = "c_"+"thumb"+"1_base.l"
        thumb_r = "c_"+"thumb"+"1_base.r"
        index_l = "c_"+"index"+"1_base.l"
        index_r = "c_"+"index"+"1_base.r"
        middle_l = "c_"+"middle"+"1_base.l"
        middle_r = "c_"+"middle"+"1_base.r"
        ring_l = "c_"+"ring"+"1_base.l"
        ring_r = "c_"+"ring"+"1_base.r"
        pinky_l = "c_"+"pinky"+"1_base.l"
        pinky_r = "c_"+"pinky"+"1_base.r"   
        
        fingers = [thumb_l, thumb_r, index_l, index_r, middle_l, middle_r, ring_l, ring_r, pinky_l, pinky_r]
        finger_side = ""
        for fing in fingers:
            if is_selected(fing):
                if (fing[-2:] == ".l"):
                    finger_side = "Left "
                if (fing[-2:] == ".r"):
                    finger_side = "Right "                
                text_upper = (fing[:3]).upper()
                layout.label(finger_side + text_upper[2:] + fing[3:-8] + ":")
                layout.prop(pose_bones[fing], '["bend_all"]', text="Bend All Phalanges", slider=True)
                
        # PINNING 
        pin_arms = ["c_stretch_arm_pin.l", "c_stretch_arm_pin.r", "c_stretch_arm.l", "c_stretch_arm.r"]      
        
        for pin_arm in pin_arms:
            if is_selected(pin_arm):
                if (pin_arm[-2:] == ".l"):
                    layout.label("Left Elbow Pinning")
                    layout.prop(pose_bones["c_stretch_arm.l"], '["elbow_pin"]', text="Elbow pinning", slider=True)
                if (pin_arm[-2:] == ".r"):
                    layout.label("Right Elbow Pinning")
                    layout.prop(pose_bones["c_stretch_arm.r"], '["elbow_pin"]', text="Elbow pinning", slider=True)
                    
        pin_legs = ["c_stretch_leg_pin.l", "c_stretch_leg_pin.r", "c_stretch_leg.l", "c_stretch_leg.r"]  
        
        for pin_leg in pin_legs:
            if is_selected(pin_leg):
                if (pin_leg[-2:] == ".l"):
                    layout.label("Left Knee Pinning")
                    layout.prop(pose_bones["c_stretch_leg.l"], '["leg_pin"]', text="Knee pinning", slider=True)
                if (pin_leg[-2:] == ".r"):
                    layout.label("Right Knee Pinning")
                    layout.prop(pose_bones["c_stretch_leg.r"], '["leg_pin"]', text="Knee pinning", slider=True)
                
            
        