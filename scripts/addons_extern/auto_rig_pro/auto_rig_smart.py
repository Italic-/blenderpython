import bpy, bmesh, math, bpy_extras
from math import degrees, pi
import mathutils
from mathutils import Vector, Matrix
import numpy



print ("\n START AUTO-RIG PRO SMART... \n")

##########################  CLASSES  ##########################



class set_front_view(bpy.types.Operator):
      
    #tooltip
    """ Select the character mesh object then click it to quicky place the reference bones on the character """
    
    bl_idname = "id.set_front_view"
    bl_label = "set_front_view"
    bl_options = {'UNDO'}   
    
  
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False     

        if context.object.type != 'MESH':
            self.report({'ERROR'}, "Please select the body mesh object.")
            return{'FINISHED'} 
  
        try:          
            _set_front_view()           
          
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}

class match_ref_only(bpy.types.Operator):
      
    #tooltip
    """ Click it to aumatically find the reference bones position """
    
    bl_idname = "id.match_ref_only"
    bl_label = "match_ref_only"
    bl_options = {'UNDO'}   
    
  
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False       

        try:
          
            _match_ref()           
          
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}

class match_ref(bpy.types.Operator):
      
    #tooltip
    """ Click it to automatically match the reference bones and the markers """
    
    bl_idname = "id.match_ref"
    bl_label = "match_ref"
    bl_options = {'UNDO'}   
    
  
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False       
        # check if the rig is appended in the scene
        try:
            bpy.data.objects["rig"]
            bpy.data.objects["rig_add"]
        except:
            self.report({'ERROR'}, "Please append auto-rig pro in the scene first.")
            return{'FINISHED'}
            
                 
        try:
            #uncheck simplify
            simplify_value = bpy.context.scene.render.use_simplify
            bpy.context.scene.render.use_simplify = False
        
            #clear selection
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            # go                 
            _auto_detect()           
           
            set_active_object("rig")
            
            _match_ref()
            
            bpy.ops.object.mode_set(mode='OBJECT')
                 
            _delete_detected()  
            
            # Display the ref bones layer only
            set_active_object("rig")    

            bpy.ops.object.mode_set(mode='EDIT')            
            bpy.context.object.data.use_mirror_x = True
        
                #display layer 17 only
            _layers = bpy.context.object.data.layers
                #must enabling one before disabling others
            _layers[17] = True  
            for i in range(0,31):
                if i != 17:
                    _layers[i] = False 
                    
            # turn on XRays
            bpy.context.object.show_x_ray = True

            # check back simplify           
            bpy.context.scene.render.use_simplify =  simplify_value

                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class add_marker(bpy.types.Operator):
      
    #tooltip
    """ Add the a marker to help auto-detection """
    
    bl_idname = "id.add_marker"
    bl_label = "add_marker"
    bl_options = {'UNDO'}   
    
    first_mouse_x = bpy.props.IntProperty()
    first_value = bpy.props.FloatProperty()

    body_part = bpy.props.StringProperty(name="Body Part")
    body_width = bpy.props.FloatProperty()
    body_height = bpy.props.FloatProperty()
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            
                    
            _add_marker(self.body_part)        
                           
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
        
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            #context.object.location.x = self.first_value - delta * 0.01
            #print(bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, (event.mouse_region_x, event.mouse_region_y), bpy.context.object.location))
            
            context.object.location = bpy_extras.view3d_utils.region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, (event.mouse_region_x, event.mouse_region_y), bpy.context.object.location)
            
            #limits
            if context.object.location[0] < 0 or self.body_part=="neck" or self.body_part == "root":
                context.object.location[0] = 0
                
            if context.object.location[0] > self.body_width/2:
                context.object.location[0] = self.body_width/2
                
            if context.object.location[2] > self.body_height:
                context.object.location[2] = self.body_height
                
            if context.object.location[2] < 0:
                context.object.location[2] = 0
                
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_value
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
        
    def invoke(self, context, event):
        self.execute(context)
        self.body_width = bpy.data.objects[bpy.context.scene.body_name].dimensions[0]
        self.body_height = bpy.data.objects[bpy.context.scene.body_name].dimensions[2]
        
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.first_value = context.object.location.x
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}

class auto_detect(bpy.types.Operator):
      
    #tooltip
    """ Select the body mesh then click it to try to automatically find the reference bones location. It will add an empty marker at each bone location """
    
    bl_idname = "id.auto_detect"
    bl_label = "auto_detect"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:
                #check if an editable mesh is selected
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='OBJECT')           
            except TypeError:
                self.report({'ERROR'}, "Please select the body object")
                return{'FINISHED'}
                          
            _auto_detect()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}

class delete_detected(bpy.types.Operator):
      
    #tooltip
    """ Delete the detected markers """
    
    bl_idname = "id.delete_detected"
    bl_label = "delete_detected"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:
                bpy.data.objects["auto_detect_loc"]                      
            except KeyError:
                self.report({'ERROR'}, "No markers found")
                return{'FINISHED'}
                       
            _delete_detected()        
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
class delete_big_markers(bpy.types.Operator):
      
    #tooltip
    """ Delete the markers """
    
    bl_idname = "id.delete_big_markers"
    bl_label = "delete_big_markers"
    bl_options = {'UNDO'}   
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            try:
                bpy.data.objects["markers"]                      
            except KeyError:
                self.report({'ERROR'}, "No markers found")
                return{'FINISHED'}
            #save current mode
            current_mode = context.mode
            active_obj = context.active_object
            print(current_mode)
            bpy.ops.object.mode_set(mode='OBJECT')                        
            _delete_big_markers()
            
            #restore current mode
            try:
                set_active_object(active_obj.name)
            except:
                pass
                #restore saved mode    
            if current_mode == 'EDIT_ARMATURE':
                current_mode = 'EDIT'
        
            try:
                bpy.ops.object.mode_set(mode=current_mode)
            except:
                pass
    
                       
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo        
        return {'FINISHED'}
    
    
 ##########################  FUNCTIONS  ##########################

    # extra functions -------------------------------------------------------------    
def tolerance_check(source, target, axis, tolerance, x_check):
    if source[axis] <= target + tolerance and source[axis] >= target - tolerance:
        #left side only  
        if x_check:      
            if source[0] > 0:
                return True
        else:           
            return True    
            
       
        
def tolerance_check_2(source, target, axis, axis2, tolerance):
    if source[axis] <= target[axis] + tolerance and source[axis] >= target[axis] - tolerance:
        if source[axis2] <= target[axis2] + tolerance and source[axis2] >= target[axis2] - tolerance:
            #left side only
            if source[0] > 0:
                return True
            
def tolerance_check_3(source, target, tolerance, x_check):
    if source[0] <= target[0] + tolerance and source[0] >= target[0] - tolerance:
        if source[1] <= target[1] + tolerance and source[1] >= target[1] - tolerance:
            if source[2] <= target[2] + tolerance and source[2] >= target[2] - tolerance:
                #left side only
                if x_check:
                    if source[0] > 0:
                        return True
                else:
                    return True    
        
def clear_selection():
    bpy.ops.mesh.select_all(action='DESELECT')

def clear_object_selection():
    bpy.ops.object.select_all(action='DESELECT')
    
def set_active_object(object_name):
     bpy.context.scene.objects.active = bpy.data.objects[object_name]
     bpy.data.objects[object_name].select = True

    
#-- start create_hand_plane()
def create_hand_plane(_bound_up, _bound_top, _bound_bot, _bound_left, _bound_right, body_height, angle1, hand_offset, body, angle2):

    bpy.ops.object.mode_set(mode='OBJECT')        

    bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=True, location=(0.0, 0.0, _bound_up + (body_height * 10)), rotation=(0, 0, 0))
    bpy.context.object.name = "plane_matrix"    

    bpy.ops.mesh.select_all(action='DESELECT')
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    mesh.verts.ensure_lookup_table() #debug
    # index: 0 bot right, 1 up right, 2 bot left, 3 up left
    mesh.verts[0].co[0] = _bound_bot
    mesh.verts[0].co[1] = _bound_right
    mesh.verts[1].co[0] = _bound_top
    mesh.verts[1].co[1] = _bound_right
    mesh.verts[2].co[0] = _bound_bot
    mesh.verts[2].co[1] = _bound_left
    mesh.verts[3].co[0] = _bound_top
    mesh.verts[3].co[1] = _bound_left

    # rotate it according to hand rotation
     #enlarge borders safe
    bpy.ops.mesh.select_all(action='SELECT') 
    bpy.ops.transform.resize(value=(1.2+(math.degrees(angle2/100)), 1.2, 1.2), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
  
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    hand_offset[0] = bpy.context.object.location[0]
    hand_offset[1] = bpy.context.object.location[1]
    hand_offset[2] = bpy.context.object.location[2]
    
        #Y rotate
    bpy.ops.object.mode_set(mode='EDIT') 
    bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.rotate(value=angle2, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.00168535)

        #Z rotate    
            
    bpy.context.object.rotation_euler[2] = -angle1
    
   
  
    #subdivide it 
    bpy.ops.object.mode_set(mode='OBJECT')      
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subsurf"].subdivision_type = 'SIMPLE'
    bpy.context.object.modifiers["Subsurf"].levels = 7
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
    #shrink on body
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = body
    bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'PROJECT'
    bpy.context.object.modifiers["Shrinkwrap"].use_negative_direction = True
    bpy.context.object.modifiers["Shrinkwrap"].use_project_z = True

   
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
    bpy.ops.object.editmode_toggle()
    #delete upper part
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    bpy.ops.mesh.select_all(action='DESELECT')

    
    
    for v in mesh.verts:
        mesh.verts.ensure_lookup_table() #debug  
        if tolerance_check(v.co, 0.0, 2, body_height/5, False):      
            v.select = True                
    bpy.ops.mesh.delete(type='VERT')
   
    
    
#-- end create_hand_plane()    
    

def copy_list(list1, list2):
    for pikwik in range(0, len(list1)):
        list2[pikwik] = list1[pikwik]

# START find_finger_top() ------------------------------------------------------ 
def find_finger_top(finger_top, vertex_border, dist, finger):   
    
    clear_selection()
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    go_up = True
    mesh.verts[vertex_border.index].select = True
    count = 0

    while go_up:
    
        go_up = False
        found_right = False     
        found_up = False
        found_bot = False


        for edge in vertex_border.link_edges:          
            for v in edge.verts:
                if v.select == False: # it not selected
                    if len(v.link_faces) < 4 and len(v.link_faces) > 0: #if it's a border vert
                        if v.co[0] > vertex_border.co[0]+(dist/100): #if found a right vert
                            found_right = True
                            v_right = v
                        if v.co[1] > vertex_border.co[1]+(dist/100): #if found an up vert
                            found_up = True
                            v_up = v
                        if v.co[1] < vertex_border.co[1]-(dist/100): #if found a bot vert
                            found_bot = True
                            v_bot = v                      
                        
                        
        if (found_right and found_up) or (found_right and not found_up):
            v_right.select = True
            go_up = True
            vertex_border = v_right
            count += 1
        
        if found_up and not found_right:
            v_up.select = True
            go_up = True
            vertex_border = v_up
            count += 1
            
        if found_bot and not found_right:
            v_bot.select = True
            go_up = True
            vertex_border = v_bot
            count += 1
            
           
    #if finger == 'pinky':
    #    print(br)
    copy_list(vertex_border.co, finger_top) 
 
    return vertex_border
                
    

 

def find_finger_bot(finger_bot, vertex_border, dist, phal_1_pos, phal_2_pos, finger_type, middle_bot):
    
    #clear_selection()
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    go_down = True

    finger_top_vert= [0.0,0.0,0.0]
    copy_list(finger_bot, finger_top_vert)   
    finger_top_vert_index = vertex_border.index
    found_phal_1 = False
    found_phal_2 = False 
    count = 0
    x_min = 0
    direction_tolerance = 2
    
 
    while go_down:
    
        go_down = False
        found_left = False     
        found_up = False
        found_bot = False

        for edge in vertex_border.link_edges:          
            for v in edge.verts:
                if v.select == False: # it not selected
                    if len(v.link_faces) < 4 and len(v.link_faces) > 0: #if it's a border vert
                        if v.co[0] < vertex_border.co[0]-(dist/100): #if found a left vert
                            found_left = True
                            v_left = v
                        if v.co[1] > vertex_border.co[1]+(dist/100): #if found an up vert
                            found_up = True
                            v_up = v
                        if v.co[1] < vertex_border.co[1]-(dist/100): #if found a bot vert
                            found_bot = True
                            v_bot = v                      
                        
                        
        if (found_left and found_up) or (found_left and not found_up):
            v_left.select = True
            go_down = True
            vertex_border = v_left
            count += 1
        
        if found_up and not found_left:
            v_up.select = True
            go_down = True
            vertex_border = v_up
            count += 1
            
        if found_bot and not found_left:
            v_bot.select = True
            go_down = True
            vertex_border = v_bot
            count += 1
                                    
                                    
                      
    #if finger_type == 'pinky':
    #    print(br)
    copy_list(vertex_border.co, finger_bot) 
    
    # Find the 2 phalanxes positions          
    clear_selection()
    mesh.verts.ensure_lookup_table() #debug   
    mesh.verts[finger_top_vert_index].select = True
    lower_bound = 1000
    _finger_bot = [0,0,0]
    copy_list(finger_bot, _finger_bot)
    
    if finger_type == "index":
        _finger_bot[0] = middle_bot[0]
    
    phal1_count = 0    
    while found_phal_1 == False and phal1_count < 50:
        phal1_count += 1
        bpy.ops.mesh.select_more()
        
        # find the lower bound of the selection
        for mv in mesh.verts:
            mesh.verts.ensure_lookup_table() #debug             
            if mv.select == True:
                if mv.co[0] < lower_bound:
                    lower_bound = mv.co[0]
                    
        # if it's lower than 1/3 of the finger, set the vert pos as the phalanx pos
        if lower_bound <= (finger_top_vert[0] - (finger_top_vert[0]-_finger_bot[0])/3):
            # select the last line only
            for mv in mesh.verts:
                mesh.verts.ensure_lookup_table() #debug             
                if mv.select == True:
                    if not tolerance_check(mv.co, lower_bound, 0, 0.0001, False):
                        mv.select = False                    
            
            copy_list(find_selection_center(), phal_1_pos)               

            
            found_phal_1 = True
    
            
    phal2_count = 0
    while found_phal_2 == False and phal2_count < 50:
        phal2_count += 1
        bpy.ops.mesh.select_more()
        # find the lower vert in selection
        for mv2 in mesh.verts:
            mesh.verts.ensure_lookup_table() #debug             
            if mv2.select == True:
                if mv2.co[0] < lower_bound:
                    lower_bound = mv2.co[0]
                    
        # if it's lower than 2/3 of the finger, set the vert pos as the phalanx pos
        if lower_bound <= (finger_top_vert[0] - ((finger_top_vert[0]-_finger_bot[0])/3)*2):
            # select the last line only
            for mv3 in mesh.verts:
                mesh.verts.ensure_lookup_table() #debug             
                if mv3.select == True:
                    if not tolerance_check(mv3.co, lower_bound, 0, 0.0001, False):
                        mv3.select = False
                        
            # find the center of this line                           
            copy_list(find_selection_center(), phal_2_pos)                        
      
            found_phal_2 = True
    
    if phal1_count > 49 or phal2_count > 49:
        bpy.context.scene.do_finger_detection = False

    return vertex_border

# end find_finger_bot() ------------------------------------------------------

def find_thumb_phalanxes(thumb_top, thumb_bot, phal_1_pos, phal_2_pos, body_height):
    
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)   
  
    found_phal_1 = False
    found_phal_2 = False 
    
    
    # Find the 2 phalanxes positions          
    
    mesh.verts.ensure_lookup_table() #debug   
        #select top vertice
    clear_selection()
    has_selected = False
    sel_radius = body_height/400
    
    while has_selected == False:
        sel_radius += body_height/600        
        for v in mesh.verts:                
            if tolerance_check_3(v.co, thumb_top, sel_radius, False):
                v.select = True
                has_selected = True
          
   
   
    lower_bound = 1000 
    phal1_count = 0
    
    while found_phal_1 == False and phal1_count < 50:
        phal1_count += 1
        bpy.ops.mesh.select_more()
        
        # find the lower bound of the selection
        for mv in mesh.verts:
            mesh.verts.ensure_lookup_table() #debug             
            if mv.select == True:
                if mv.co[0] < lower_bound:
                    lower_bound = mv.co[0]
                    
        # if it's lower than 1/4 of the finger, set the vert pos as the phalanx pos
        if lower_bound <= thumb_top[0] + (thumb_bot[0]-thumb_top[0])*0.3:
            
            # select the last line only
            for mv in mesh.verts:
                mesh.verts.ensure_lookup_table() #debug            
                if mv.select == True:                   
                    if not tolerance_check(mv.co, lower_bound, 0, 0.0001, False):                        
                        mv.select = False             
            
            copy_list(find_selection_center(), phal_1_pos)   
            
            found_phal_1 = True           
    
    phal2_count = 0 
    while found_phal_2 == False and phal2_count< 50:
        phal2_count += 1
        bpy.ops.mesh.select_more()
        # find the lower vert in selection
        for mv2 in mesh.verts:
            mesh.verts.ensure_lookup_table() #debug             
            if mv2.select == True:
                if mv2.co[0] < lower_bound:
                    lower_bound = mv2.co[0]
                    
        # if it's lower than 1/2 of the finger, set the vert pos as the phalanx pos
        if lower_bound <= thumb_top[0] + (thumb_bot[0]-thumb_top[0])*0.5:
            # select the last line only
            for mv3 in mesh.verts:
                mesh.verts.ensure_lookup_table() #debug             
                if mv3.select == True:
                    if not tolerance_check(mv3.co, lower_bound, 0, 0.0001, False):
                        mv3.select = False
                    
            # find the center of this line                           
            copy_list(find_selection_center(), phal_2_pos)                        
             
            found_phal_2 = True
      
    if phal1_count > 49 or phal2_count > 49:
        bpy.context.scene.do_finger_detection = False

def find_selection_center():    
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    c_x = []
    c_y = []
    c_z = []
    total_x = 0
    total_y = 0
    total_z = 0            
    center = [0,0,0]

    for vert in mesh.verts:
        if vert.select == True:
            c_x.append(vert.co[0])
            c_y.append(vert.co[1])
            c_z.append(vert.co[2])
            
    for v in c_x:
        total_x += v                
    for v in c_y:
        total_y += v                
    for v in c_z:
        total_z += v
        
    center[0] = total_x/len(c_x)
    center[1] = total_y/len(c_y)
    center[2] = total_z/len(c_z)
    
    return center 

def create_empty_loc(radii, pos, name):
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius = radii, view_align=True, location=(pos), rotation=(0, 0, 0))  
    # rename it     
    bpy.context.object.name = name + "_auto"
    # parent it
    bpy.context.object.parent = bpy.data.objects["auto_detect_loc"]
    
def vectorize3(list):
    return Vector((list[0], list[1], list[2]))

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
    
def mirror_hack():
    bpy.ops.transform.translate(value=(0, 0, 0), constraint_orientation='NORMAL', proportional='DISABLED')
   
def get_edit_bone(name):
    return bpy.context.object.data.edit_bones[name]

def get_object(name):
    return bpy.data.objects[name]
    
    # CLASS FUNCTIONS -------------------------------------------------------------   
    
def _match_ref():
    
    #scale the rig object according to the character height
    b_name = bpy.context.scene.body_name

    bpy.context.object.dimensions = bpy.data.objects[b_name].dimensions*3.0
    bpy.context.object.scale[1] = bpy.context.object.scale[2] 
    bpy.context.object.scale[0] = bpy.context.object.scale[2] 

    bpy.ops.object.mode_set(mode='EDIT')
        #enable x-axis mirror edit
    bpy.context.object.data.use_mirror_x = True
        
    #display layer 17 only
    _layers = bpy.context.object.data.layers
    #must enabling one before disabling others
    _layers[17] = True  
    for i in range(0,31):
        if i != 17:
            _layers[i] = False 
    
    side = ".l"
    
    rig_matrix_world = bpy.data.objects["rig"].matrix_world.inverted()
    
    
    # FOOT
    init_selection("foot_ref"+side)
    foot = get_edit_bone("foot_ref"+side)    
    foot.head = rig_matrix_world * get_object("ankle_loc_auto").location
    foot.tail = rig_matrix_world * get_object("toes_start_auto").location
    mirror_hack()
    
    init_selection("toes_ref"+side)
    toes_ref = get_edit_bone("toes_ref"+side)    
    toes_ref.head = rig_matrix_world * get_object("toes_start_auto").location
    toes_ref.tail = rig_matrix_world * get_object("toes_end_auto").location   
    mirror_hack()
    
    init_selection("toes_end_ref"+side)
    toes_end_ref = get_edit_bone("toes_end_ref"+side)
    toes_end_auto = get_object("toes_end_auto").location  
    toes_end_ref.head = rig_matrix_world * vectorize3([toes_end_auto[0], toes_end_auto[1], 0])
    toes_end_ref.tail = toes_end_ref.head + vectorize3([0,0,0.01])
    mirror_hack()
    
    init_selection("foot_bank_01_ref"+side)
    foot_bank_01_ref = get_edit_bone("foot_bank_01_ref"+side)
    bank_right = get_object("bank_right_loc_auto").location  
    foot_bank_01_ref.head = rig_matrix_world * bank_right
    foot_bank_01_ref.tail = foot_bank_01_ref.head + vectorize3([0,-0.01,0])
    mirror_hack()
    
    init_selection("foot_bank_02_ref"+side)
    foot_bank_02_ref = get_edit_bone("foot_bank_02_ref"+side)
    bank_left = get_object("bank_left_loc_auto").location  
    foot_bank_02_ref.head = rig_matrix_world * bank_left
    foot_bank_02_ref.tail = foot_bank_02_ref.head + vectorize3([0,-0.01,0])
    mirror_hack()
    
    init_selection("foot_heel_ref"+side)
    foot_heel_ref = get_edit_bone("foot_heel_ref"+side)
    heel_auto = get_object("bank_mid_loc_auto").location
    foot_heel_ref.head = rig_matrix_world * heel_auto
    foot_heel_ref.tail = foot_heel_ref.head + vectorize3([0,-0.01,0])
    mirror_hack()
    
    toes_end_auto = get_object("toes_end_auto").location 
    heel_auto = get_object("bank_mid_loc_auto").location
    foot_length = toes_end_auto[1] - heel_auto[1]
    
        # toes fingers
    toes_list=["toes_pinky", "toes_ring", "toes_middle", "toes_index", "toes_thumb"]
    foot_bank_01_ref = get_edit_bone("foot_bank_01_ref"+side)
    foot_bank_02_ref = get_edit_bone("foot_bank_02_ref"+side)
    toes_ref = get_edit_bone("toes_ref"+side)
    
    for t in range(0,5):
        max = 4
        if t == 4:
            max = 3 #thumb has less phalanges
        for p in range (1,max):
            bones_mirrored = [toes_list[t]+str(p)+"_ref.l", toes_list[t]+str(p)+"_ref.r"]
            for bon in bones_mirrored:
                bone = get_edit_bone(bon)
                bone.head[0] =  -(foot_bank_01_ref.head[0] + ((foot_bank_02_ref.head[0] - foot_bank_01_ref.head[0])*t)/5)
                bone.head[1] =  toes_ref.head[1] + ((toes_ref.tail[1] - toes_ref.head[1])*p)/max
                bone.head[2] = toes_ref.head[2]
                #if last phalanges
                if p == max-1:
                    bone.tail[0] = bone.head[0]
                    bone.tail[1] = toes_ref.tail[1]
                    bone.tail[2] = toes_ref.tail[2]

    # LEGS
    init_selection("thigh_ref"+side)
    thigh_ref = get_edit_bone("thigh_ref"+side)
    knee_auto = get_object("knee_loc_auto").location  
    thigh_ref.tail = rig_matrix_world * knee_auto
    thigh_ref.head = rig_matrix_world * get_object("leg_loc_auto").location  
    mirror_hack()
    
    init_selection("bot_bend_ref"+side)
    bot_bend_ref = get_edit_bone("bot_bend_ref"+side)
    bot_auto = get_object("bot_empty_loc_auto").location  
    bot_bend_ref.head = rig_matrix_world * bot_auto

    bot_bend_ref.tail = bot_bend_ref.head + (rig_matrix_world * vectorize3([0, -foot_length/4, 0]))
    mirror_hack()
    
    # SPINE
    init_selection("root_ref.x")
    root_ref = get_edit_bone("root_ref.x")
    root_auto = get_object("root_loc_auto").location  
    root_ref.head = rig_matrix_world * root_auto
    root_ref.tail = rig_matrix_world * get_object("spine_01_loc_auto").location
    
    init_selection("spine_01_ref.x")
    spine_01_ref = get_edit_bone("spine_01_ref.x")   
    spine_01_ref.tail = rig_matrix_world * get_object("spine_02_loc_auto").location
    
    init_selection("spine_02_ref.x")
    spine_02_ref = get_edit_bone("spine_02_ref.x")   
    spine_02_ref.tail = rig_matrix_world * get_object("neck_loc_auto").location 
    
    init_selection("neck_ref.x")
    neck_ref = get_edit_bone("neck_ref.x")
    neck_ref.head = rig_matrix_world * get_object("neck_loc_auto").location
    neck_ref.tail = rig_matrix_world * get_object("head_loc_auto").location
    
    init_selection("head_ref.x")
    head_ref = get_edit_bone("head_ref.x")
    head_ref.tail = rig_matrix_world * get_object("head_end_loc_auto").location
    
    init_selection("breast_01_ref"+side)
    breast_01_ref = get_edit_bone("breast_01_ref"+side)
    breast_01_ref.head = rig_matrix_world * get_object("breast_01_loc_auto").location
    spine_02_ref = get_edit_bone("spine_02_ref.x")   
    breast_01_ref.tail = breast_01_ref.head + (vectorize3([0,0,(spine_02_ref.tail[2]-spine_02_ref.head[2])*0.3]))
    mirror_hack()
    
    init_selection("breast_02_ref"+side)
    breast_02_ref = get_edit_bone("breast_02_ref"+side)
    breast_02_ref.head = rig_matrix_world * get_object("breast_02_loc_auto").location
    spine_02_ref = get_edit_bone("spine_02_ref.x")   
    breast_02_ref.tail = breast_02_ref.head + vectorize3([0,0,(spine_02_ref.tail[2]-spine_02_ref.head[2])*0.3])
    mirror_hack()
    
    # ARMS
    init_selection("shoulder_ref"+side)
    shoulder_ref = get_edit_bone("shoulder_ref"+side)    
    shoulder_ref.head = rig_matrix_world * get_object("shoulder_base_loc_auto").location
    shoulder_ref.tail = rig_matrix_world * get_object("shoulder_loc_auto").location
    mirror_hack()
    
    init_selection("arm_ref"+side)
    arm_ref = get_edit_bone("arm_ref"+side)    
    arm_ref.tail = rig_matrix_world * get_object("elbow_loc_auto").location
    mirror_hack()
    
    init_selection("forearm_ref"+side)
    forearm_ref = get_edit_bone("forearm_ref"+side)    
    forearm_ref.tail = rig_matrix_world * get_object("hand_loc_auto").location
    mirror_hack()
    
    
    init_selection("hand_ref"+side)
    hand_ref = get_edit_bone("hand_ref"+side)
    

    if bpy.context.scene.do_finger_detection:#check if fingers are detected
        hand_ref.tail = hand_ref.head + (rig_matrix_world*get_object("middle_top_auto").location - hand_ref.head)*0.4
       
    else:
        forearm_ref = get_edit_bone("forearm_ref"+side)
        hand_ref.tail = hand_ref.head + ((forearm_ref.tail - forearm_ref.head)/3)
        
        #hand roll
    bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')

    mirror_hack()
    
    
    # FINGERS --------------------------------------------
    
    scene = bpy.context.scene
        # make list of fingers bones
    finger_bones = []        
    init_selection("hand_ref"+side)
    bpy.ops.armature.select_similar(type='CHILDREN')
    
    for bone in bpy.context.object.data.edit_bones:
            if bone.select and bone.name != "hand_ref"+side:
                finger_bones.append(bone.name)  

    bpy.ops.armature.select_all(action='DESELECT')
    
    #reset fingers transforms if it's the second time the button is pressed
    if len(scene.fingers_init_transform) > 0:
        for i in finger_bones:
            current_bone = get_edit_bone(i)
            current_bone.head = scene.fingers_init_transform[i].head
            current_bone.tail = scene.fingers_init_transform[i].tail
            current_bone.roll = scene.fingers_init_transform[i].roll
        
    #save initial fingers transform in the property collection if it's the first time the button is pressed
    if len(scene.fingers_init_transform) == 0:
        for i in finger_bones:
            current_bone = get_edit_bone(i)
            item = scene.fingers_init_transform.add()       
            item.name = i  
            item.head = current_bone.head
            item.tail = current_bone.tail
            item.roll = current_bone.roll

        #root
    fingers = ["thumb", "index", "middle", "ring", "pinky"]    
        
    fingers_root = ["index1_base_ref"+side, "middle1_base_ref"+side, "ring1_base_ref"+side, "pinky1_base_ref"+side]
    
    if bpy.context.scene.do_finger_detection:
       
        auto_root = ["index_root_auto", "middle_root_auto", "ring_root_auto", "pinky_root_auto"]

        for i in range(0, len(fingers_root)):
            init_selection(fingers_root[i])      
            root_ref = get_edit_bone(fingers_root[i])
            root_ref.head = rig_matrix_world * get_object(auto_root[i]).location
            root_ref.tail = rig_matrix_world * get_object(fingers[i+1]+"_bot_auto").location
            bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')   
            mirror_hack()     
        
       
        for f in range(0,5):        
            #bot
            init_selection(fingers[f]+"1_ref"+side)      
            finger_bot = get_edit_bone(fingers[f]+"1_ref"+side)
            finger_bot.head = rig_matrix_world * get_object(fingers[f]+"_bot_auto").location
            finger_bot.tail = rig_matrix_world * get_object(fingers[f]+"_phal_2_auto").location
            if f != 0: #not thumb
                bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
            else:
                bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Y')

            mirror_hack()
            #phal1
            init_selection(fingers[f]+"2_ref"+side)
            finger_phal_1 = get_edit_bone(fingers[f]+"2_ref"+side)
            finger_phal_1.tail = rig_matrix_world * get_object(fingers[f]+"_phal_1_auto").location
            if f != 0: #not thumb
                bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
            else:
                bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Y')
                
            mirror_hack()
            #phal2
            init_selection(fingers[f]+"3_ref"+side)
            finger_phal_2 = get_edit_bone(fingers[f]+"3_ref"+side)
            finger_phal_2.tail = rig_matrix_world * get_object(fingers[f]+"_top_auto").location
            if f != 0: #not thumb
                bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
            else:
                bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Y')
            mirror_hack()
            
    else:#no finger detection case       
              
      
        # Offset all finger bones close the hand bone
            # calculate offset vector
        rig_scale = bpy.data.objects["rig"].scale[0]
        
        #head_height = get_edit_bone("head_ref.x").tail[2]-get_edit_bone("head_ref.x").head[2]
        #offset_pos = get_edit_bone("neck_ref.x").tail + vectorize3([0,-head_height*2,0])
        #offset_vec = (offset_pos - get_edit_bone("nose_01_ref.x").head)*rig_scale
        offset_vec = (get_edit_bone("hand_ref"+side).tail - get_edit_bone("index1_base_ref"+side).head)*rig_scale
        
        

        for b in finger_bones:
            get_edit_bone(b).select = True
      
        bpy.ops.object.mode_set(mode='POSE') 
        bpy.ops.object.mode_set(mode='EDIT')           
        bpy.ops.transform.translate(value=(offset_vec), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=True, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.0922959)
        
        bpy.ops.armature.select_all(action='DESELECT')
        
    # FACIAL
    
    # make list of facial bones
    facial_bones = ["chin_02_ref.x", "chin_01_ref.x", "nose_02_ref.x", "nose_01_ref.x", "nose_03_ref.x", "tong_01_ref.x", "tong_02_ref.x", "tong_03_ref.x", "jaw_ref.x", "lips_roll_bot_ref.x", "lips_roll_top_ref.x", "teeth_bot_ref.x", "teeth_top_ref.x", "lips_bot_ref.x", "lips_bot_ref"+side, "lips_bot_01_ref"+side,"lips_smile_ref"+side, "lips_corner_mini_ref"+side, "lips_top_01_ref"+side, "lips_top_ref"+side, "lips_top_ref.x", "cheek_inflate_ref"+side, "cheek_smile_ref"+side, "ear_01_ref"+side, "ear_02_ref"+side]
    
    init_selection("eye_offset_ref"+side)
    bpy.ops.armature.select_similar(type='CHILDREN')
    
    for bone in bpy.context.object.data.edit_bones:
        if bone.select:
            facial_bones.append(bone.name)
            
        
    init_selection("eyebrow_full_ref"+side)
    bpy.ops.armature.select_similar(type='CHILDREN')
    
    for bone1 in bpy.context.object.data.edit_bones:
        if bone1.select:
            facial_bones.append(bone1.name)
    

    # Offset all facial bones close the head ref bone

        # calculate offset vector
    rig_scale = bpy.data.objects["rig"].scale[0]
        
    head_height = get_edit_bone("head_ref.x").tail[2]-get_edit_bone("head_ref.x").head[2]
    offset_pos = get_edit_bone("neck_ref.x").tail + vectorize3([0,-head_height*2,0])
    offset_vec = (offset_pos - get_edit_bone("nose_01_ref.x").head)*rig_scale
    
    bpy.ops.armature.select_all(action='DESELECT')

    for b in facial_bones:
        get_edit_bone(b).select = True
    
    bpy.ops.object.mode_set(mode='POSE') 
    bpy.ops.object.mode_set(mode='EDIT')           
    bpy.ops.transform.translate(value=(offset_vec), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=True, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.0922959)
    
    bpy.ops.armature.select_all(action='DESELECT')

    
        
    
def _add_marker(name):
    
    body = bpy.data.objects[bpy.context.scene.body_name]
    body_height = body.dimensions[2]
    scaled_radius = body_height/20

    bpy.ops.object.mode_set(mode='OBJECT')
    
    # create an empty group for the markers
    try:
        #if the detect group already exist, don't create it
        bpy.data.objects["markers"]       
    
    except KeyError:
        # if not create it
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius = scaled_radius, view_align=False, location=(0,0,0), rotation=(0, 0, 0))   
        bpy.context.object.name = "markers"
    
    # create the marker if not exists already
    try: #it already exists
        bpy.ops.object.select_all(action='DESELECT')

        bpy.data.objects[name+"_loc"].select = True
        set_active_object(name+"_loc")
    except KeyError:
        #create it
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius = scaled_radius, view_align=False, location=(0,0,0), rotation=(0, 0, 0))  
        bpy.context.object.empty_draw_type = 'CIRCLE'
        bpy.context.object.empty_draw_size = scaled_radius    
        # rename it     
        bpy.context.object.name = name + "_loc"
        # parent it
        bpy.context.object.parent = bpy.data.objects["markers"]
        #enable xray
        bpy.context.object.show_x_ray = True
        
        
        if name == "shoulder" or name == "hand" or name == "foot":
            #limit mirror axis
            bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
            bpy.context.object.constraints["Limit Location"].use_min_x = True
            bpy.context.object.constraints["Limit Location"].use_transform_limit = True
    
            # create mirror object with constraint
            bpy.ops.object.empty_add(type='PLAIN_AXES', radius = scaled_radius, view_align=False, location=(0,0,0), rotation=(0, 0, 0))  
            bpy.context.object.empty_draw_type = 'CIRCLE'
            bpy.context.object.empty_draw_size = scaled_radius
            # rename it     
            bpy.context.object.name = name + "_sym_loc"
            # parent it
            bpy.context.object.parent = bpy.data.objects["markers"]
            #enable xray
            bpy.context.object.show_x_ray = True
            #add mirror constraint
            bpy.ops.object.constraint_add(type='COPY_LOCATION')
            bpy.context.object.constraints["Copy Location"].target = bpy.data.objects[name+"_loc"]
            bpy.context.object.constraints["Copy Location"].invert_x = True
            
            #select back the main empty
            set_active_object(name+"_loc")

    # markers specific options

    if name == "neck" or name == "root":
        bpy.context.object.lock_location[0] = True
    
    
       
          
def _auto_detect(): 
    
    debug = True    

    if debug:
        print("START AUTO DETECTION \n")

    #get character mesh name
    body = bpy.data.objects[bpy.context.scene.body_name]
    
    #apply transforms
    bpy.ops.object.select_all(action='DESELECT')
    body.select = True
    bpy.context.scene.objects.active = body
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    #get its dimension
    body_width = body.dimensions[0]
    body_height = body.dimensions[2]
    body_depth = body.dimensions[1]
    
    hand_offset = [0,0,0]

    # create an empty group for the auto detected empties
    try:
        #if the detect group already exist, delete it
        bpy.data.objects["auto_detect_loc"].select = True
        _delete_detected()
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius = 0.01, view_align=True, location=(0,0,0), rotation=(0, 0, 0))   
        bpy.context.object.name = "auto_detect_loc"
    
    except KeyError:
        # if not create it
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius = 0.01, view_align=True, location=(0,0,0), rotation=(0, 0, 0))   
        bpy.context.object.name = "auto_detect_loc"


    # get the loc guides
    foot_loc = bpy.data.objects["foot_loc"]
    hand_loc = bpy.data.objects["hand_loc"]

        #enter character mesh edit mode
    body.select = True
    bpy.context.scene.objects.active = body
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    #get the mesh (in edit mode only)
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    # HAND DETECTION -------------------------------------------------------
    
    if debug:
        print("find hands boundaries...\n")

    
    #store hands verts in a list
    selected_index = []
    for v in mesh.verts:    
        if v.co[0] > hand_loc.location[0]:
            v.select = True
            selected_index.append(v.index)

    #find the hand boundaries  
    bound_left = -10000
    bound_right = 10000
    bound_top = 0.0
    bound_bot = 10000
    bound_up = 0.0    
    middle_top = 0 # vertex id at the top of the middle finger
    clear_selection()

    for i in selected_index:
        mesh.verts.ensure_lookup_table() #debug
        vert_x = mesh.verts[i].co[0]
        vert_y = mesh.verts[i].co[1]  
        vert_z = mesh.verts[i].co[2]      
        if vert_y > bound_left:
            bound_left = vert_y
        if vert_y < bound_right:
            bound_right = vert_y
        if vert_x < bound_bot:
            bound_bot = vert_x
        if vert_x > bound_top:
            bound_top = vert_x
            middle_top = i
        if vert_z > bound_up:
            bound_up = vert_z
            
    # Find the wrist center
        #select vertices around hand_loc
    if debug:
        print("find wrist...\n")
        
    wrist_selected_index = []    
    clear_selection()
    has_selected_vert = False
    increase_select = body_width / 100
    
    while has_selected_vert == False:
        for v in mesh.verts:    
            if tolerance_check(v.co, hand_loc.location[0], 0, increase_select, True):
                v.select = True
                has_selected_vert = True      
                wrist_selected_index.append(v.index)
        # if not vert selected, increase selection radius        
        if has_selected_vert == False:
            increase_select *= 2  
    
   
    
    #find the wrist boundaries
    wrist_bound_back = -10000.0
    wrist_bound_front = 10000.0
    wrist_bound_left = 10000.0
    wrist_bound_right = 0.0   
    
    clear_selection()
    
    if debug:
        print("find wrist boundaries...\n")    
    
    for vi in wrist_selected_index:
        mesh.verts.ensure_lookup_table() #debug
        vert_y = mesh.verts[vi].co[1]
        vert_x = mesh.verts[vi].co[0]
        #back    
        if vert_y > wrist_bound_back:
            wrist_bound_back = vert_y
        #front
        if vert_y < wrist_bound_front:
            wrist_bound_front = vert_y        
        #left
        if vert_x < wrist_bound_left:
            wrist_bound_left = vert_x
        #right
        if vert_x > wrist_bound_right:
            wrist_bound_right = vert_x
    

    hand_loc_x = hand_loc.location[0]
    hand_loc_y = wrist_bound_back + ((wrist_bound_front - wrist_bound_back)*0.4)
    hand_loc_z = hand_loc.location[2]    
    hand_empty_loc = [hand_loc_x, hand_loc_y, hand_loc_z]
    
   
    # FINGERS DETECTION
    
    if debug:
        print("find fingers...\n")
    
        # find the hand rotation by finding the middle finger angle
    finger_end_center = [0,0,0]
    finger_start_center = [0,0,0]
    mesh.verts.ensure_lookup_table() #debug  
    mesh.verts[middle_top].select = True
    selected_length = 0.0
    current_length = 0.0
    start = True
    vertex_top = -10000
    separate_phalanx = False
    
    while selected_length < (bound_top - bound_bot)/3.5 and separate_phalanx == False:
        
        bpy.ops.mesh.select_more()
        bpy.ops.view3d.snap_cursor_to_selected()
        if start == True:
            copy_list(bpy.context.space_data.cursor_location, finger_end_center)
            start = False 
                 
        else:
            copy_list(bpy.context.space_data.cursor_location, finger_start_center)
      

        #find the selected length
        for v in mesh.verts:
            if v.select == True:
                if v.co[0] < bound_top - selected_length:                
                    selected_length = bound_top - v.co[0]
                    
                if v.co[2] > vertex_top:
                    vertex_top = v.co[2]
                    
        # check the separate phalanx case to avoid infinite loop
        if debug:
            print("selected length = ", selected_length, " current_length = ", current_length)
        if selected_length > current_length:
            current_length = selected_length
        elif selected_length == current_length:
            separate_phalanx = True
            
                    
    if debug:
        print("find fingers thickness...\n")
    
    #find the finger thickness for later
    f_thickness = finger_start_center[2] - vertex_top
  

    if finger_start_center[2] == 0:
        print("Non standard fingers, skip fingers detection")
        bpy.context.scene.do_finger_detection = False
    
    if bpy.context.scene.do_finger_detection:
        finger_start_x = [finger_start_center[0], finger_start_center[1], 0.0] 
        finger_end_x = [finger_end_center[0], finger_end_center[1], 0.0]   
        
        finger_start_y = [finger_start_center[0], 0.0, finger_start_center[2]] 
        finger_end_y = [finger_end_center[0], 0.0, finger_end_center[2]]
        
        if debug:
            print("find finger angle...\n")                    
           
        #calculate X angle
        v1 = Vector((finger_end_x)) - Vector((finger_start_x)) 
        v2 = Vector((1, 0, 0))
       
        try:
            angle_1 = v1.angle(v2)
        except ValueError:
            angle_1 = 0
            print("\n ERROR: Can't find hand location -> can't find hand angle")
            
        if angle_1 > pi * 0.5:
            angle_1 = pi - angle_1
        if finger_end_x[1] > finger_start_x[1]:
            angle_1 *= -1
            
         #calculate Y angle
        v2 = Vector((finger_end_y)) - Vector((finger_start_y)) 
        v3 = Vector((1, 0, 0))
       
        try:
            angle_2 = v2.angle(v3)
        except ValueError:
            angle_2 = 0
            print("\n ERROR: Can't find hand location -> can't find hand angle")
            
        if angle_2 > pi * 0.5:
            angle_2 = pi - angle_2
        if finger_end_y[1] > finger_start_y[1]:
            angle_2 *= -1

        finger_normal = (v2.cross(vectorize3([0,1,0]))).normalized()
        f_thickness *= 1/1+(math.degrees(angle_2)/20)
        f_thickness *= 0.2
      
        if debug:
            print("create hand matrix ...\n")
            
        #create plane matrix
        create_hand_plane(bound_up, bound_top, bound_bot, bound_left, bound_right, body_height, angle_1, hand_offset, body, angle_2)


        #declare the fingers pos
        pinky_top = [-10000,0.0,0.0]
        pinky_bot = [-10000,0.0,0.0]
        pinky_phal_1 = [0.0,0.0,0.0]
        pinky_phal_2 = [0.0,0.0,0.0]
        
        ring_top = [-10000,0.0,0.0]
        ring_bot = [-10000,0.0,0.0]
        ring_phal_1 = [0.0,0.0,0.0]
        ring_phal_2 = [0.0,0.0,0.0]
        
        middle_top =[-10000,0.0,0.0]
        middle_bot =[-10000,0.0,0.0]
        middle_phal_1 = [0.0,0.0,0.0]
        middle_phal_2 = [0.0,0.0,0.0] 
        
        index_top = [-10000,0.0,0.0]
        index_bot = [-10000,0.0,0.0]
        index_phal_1 = [0.0,0.0,0.0]
        index_phal_2 = [0.0,0.0,0.0] 
        
        thumb_top = [-10000,0.0,0.0]
        thumb_bot = [-10000,0.0,0.0]
        thumb_phal_1 = [-10000,0.0,0.0]
        thumb_phal_2 = [-10000,0.0,0.0]

        # list verts under y_progress
        mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
        
        if debug:
            print("find grid distance...\n")

            #find the distance y between verts
        dist = 100
        mesh.verts.ensure_lookup_table() #debug
        mesh.verts[0].select = True   

        bpy.ops.mesh.select_more()
        mesh.verts[0].select = False   
        
        for i in mesh.verts:
            if i.select:
                current_dist = abs(abs(mesh.verts[0].co[1]) - abs(i.co[1]))

                if current_dist < dist and current_dist > 0.00001:
                    dist = current_dist

        
        print("grid_dist = ", dist)
        
        # Find matrix-plane left bound        
        bound_left = -100
        vertex_border = 0
        
        for v in mesh.verts:
            
            mesh.verts.ensure_lookup_table() #debug  
            vert_y = v.co[1]
            if vert_y > bound_left:
                bound_left = vert_y
                vertex_border = v
                clear_selection()
                v.select = True
      
        if debug:
            print("start finger detection...\n")
            
        # Start detection     
        #pinky
        vertex_border = find_finger_top(pinky_top, vertex_border, dist, "pinky")
        copy_list(pinky_top, pinky_bot)
        vertex_border = find_finger_bot(pinky_bot, vertex_border, dist, pinky_phal_1, pinky_phal_2, "pinky", middle_bot)    
        
        #ring        
        vertex_border = find_finger_top(ring_top, vertex_border, dist, "ring")        
        copy_list(ring_top, ring_bot)
        vertex_border = find_finger_bot(ring_bot, vertex_border, dist, ring_phal_1, ring_phal_2, "ring", middle_bot)
        
        #middle        
        vertex_border = find_finger_top(middle_top, vertex_border, dist, "middle")          
        copy_list(middle_top, middle_bot)
        vertex_border = find_finger_bot(middle_bot, vertex_border, dist, middle_phal_1, middle_phal_2, "middle", middle_bot)   
      

        #index   
        vertex_border = find_finger_top(index_top, vertex_border, dist, "index")        
        copy_list(index_top, index_bot)       
        vertex_border = find_finger_bot(index_bot, vertex_border, dist, index_phal_1, index_phal_2, "index", middle_bot)
       
        #thumb       
        vertex_border = find_finger_top(thumb_top, vertex_border, dist, "thumb")
        
        #thumb_bot        
        thumb_top_vec = bpy.data.objects["plane_matrix"].matrix_world * Vector((thumb_top[0], thumb_top[1], thumb_top[2]))
        hand_pos_vec = Vector((hand_loc_x, hand_loc_y, hand_loc_z))
          
        thumb_bot_vec = hand_pos_vec + (thumb_top_vec - hand_pos_vec)*0.1
        
        thumb_bot = bpy.data.objects["plane_matrix"].matrix_world.inverted() * thumb_bot_vec
        
        find_thumb_phalanxes(thumb_top , thumb_bot, thumb_phal_1, thumb_phal_2, body_height)   
        
        if debug:
            print("end finger detection, analyze data...\n")

       
            # create empties for each finger location
        bpy.ops.object.mode_set(mode='OBJECT')
        
         # Fingers bot        
        
            # pinky bot
        print(pinky_top[1], pinky_bot[1])
        pinky_bot[1] = (pinky_top[1] + pinky_bot[1])*0.5# - (bound_right-bound_left)*0.05
        pinky_bot[0] -= (bound_top-bound_bot)/13    
        pinky_bot_vec = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(pinky_bot)
        
        pinky_bot_vec[2] += -f_thickness/3
        
        

            # ring bot
        ring_bot[1] = (ring_bot[1] + ring_top[1])*0.5 - (bound_right-bound_left)*0.05
        ring_bot[0] -= (bound_top-bound_bot)/13
        ring_bot_vec = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(ring_bot)
        #ring_bot_vec[2] += -f_thickness/1.5
        #print("thickness = ", f_thickness/1.5)
       
            # middle bot        
        middle_bot[1] = (middle_bot[1] + middle_top[1])*0.4 - (bound_right-bound_left)*0.05
        middle_bot[0] -= (bound_top-bound_bot)/13
        middle_bot_vec = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(middle_bot)
        middle_bot_vec[2] += -f_thickness/3
        create_empty_loc(0.01, middle_bot_vec, "middle_bot")

        
        #ring bot second iteration
        ring_bot_vec[2] = middle_bot_vec[2]  
        ring_bot_vec[1] = pinky_bot_vec[1] + (middle_bot_vec[1] - pinky_bot_vec[1])/2   
        create_empty_loc(0.01, ring_bot_vec, "ring_bot")
        
            # index bot
        hand_loc_local = bpy.data.objects["plane_matrix"].matrix_world.inverted()*vectorize3(hand_empty_loc)#convert global to local coord
        index_bot[1] = ((hand_loc_local[1] - index_top[1])*0.25)+ index_top[1] #(index_bot[1] + index_top[1])*0.4# - (bound_right-bound_left)*0.05
        #index_bot[2] = middle_bot[2]
        #index_bot[0] -= (bound_top-bound_bot)/13
        index_bot[0] = middle_bot[0]
        index_bot_vec = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(index_bot)
        index_bot_vec[2] = middle_bot_vec[2]
        create_empty_loc(0.01, index_bot_vec, "index_bot")
        
        # Fingers root
        pinky_root = []
        ring_root = []
        middle_root = []
        index_root = []
        
        fingers_root_list = [pinky_root, ring_root, middle_root, index_root]
        fingers_bot_list = [pinky_bot_vec, ring_bot_vec, middle_bot_vec, index_bot_vec]    
        
        for i in range(0,4):
            fingers_root_list[i] = hand_pos_vec + (fingers_bot_list[i] - hand_pos_vec)*0.3
           
            fingers_root_list[i][1] = (fingers_root_list[i][1] + (wrist_bound_back + (wrist_bound_front-wrist_bound_back)*i/4))/2
            
        
        fingers_root_dict = {'pinky_root' : [fingers_root_list[0], "pinky_root"], 'ring_root':[fingers_root_list[1], "ring_root"], 'middle_root':[fingers_root_list[2], "middle_root"], 'index_root':[fingers_root_list[3],"index_root"]}
            
        for key, value in fingers_root_dict.items():               
            create_empty_loc(0.01, value[0], value[1])     
                
        
        thumb_bot_vec = fingers_root_list[3] + fingers_root_list[3]-fingers_root_list[2]
        create_empty_loc(0.01, thumb_bot_vec, "thumb_bot")
        
        # Fingers top    
        fingers_dict = {'pinky_top' : [pinky_top, "pinky_top"], 'ring_top' : [ring_top, "ring_top"], 'middle_top' : [middle_top, "middle_top"], 'index_top' : [index_top, "index_top"], 'thumb_top' : [thumb_top, "thumb_top"]}

        for key, value in fingers_dict.items():        
                # convert "list" coordinates to "vector" (matrix)
            co = Vector((value[0][0], value[0][1], value[0][2]))          
            global_pos = bpy.data.objects["plane_matrix"].matrix_world * co
            #global_pos[2] += f_thickness/2   
            global_pos += finger_normal * (f_thickness/2)
            create_empty_loc(0.01, global_pos, value[1])
         
        # pinky second iteration refine
        
        if pinky_bot_vec[0] > ring_bot_vec[0]:
            pinky_bot_vec[0] = ring_bot_vec[0]   
            pinky_bot_vec[2] = ring_bot_vec[2]
        
              
        create_empty_loc(0.01, pinky_bot_vec, "pinky_bot")
        
        # Phalanxes
            # thumb phalanxes
        thumb_top_vec = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(thumb_top) 
                 
        thumb_phal_2 = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(thumb_phal_2)
        #thumb_phal_2 += finger_normal * (f_thickness/3)
        create_empty_loc(0.01, thumb_phal_2, "thumb_phal_2")
        
        thumb_phal_1 = bpy.data.objects["plane_matrix"].matrix_world * vectorize3(thumb_phal_1)
        #thumb_phal_1 += finger_normal * (f_thickness/3)
        create_empty_loc(0.01, thumb_phal_1, "thumb_phal_1")
        
        phalanxes_dict = {'pinky_phal_1':[pinky_phal_1, "pinky_phal_1"], 'pinky_phal_2':[pinky_phal_2,"pinky_phal_2"], 'ring_phal_1':[ring_phal_1,"ring_phal_1"], 'ring_phal_2':[ring_phal_2,"ring_phal_2"],'middle_phal_1':[middle_phal_1,"middle_phal_1"],'middle_phal_2':[middle_phal_2,"middle_phal_2"],'index_phal_1':[index_phal_1,"index_phal_1"],'index_phal_2':[index_phal_2,"index_phal_2"]}
        
        for key, value in phalanxes_dict.items():        
                # convert "list" coordinates to "vector" (matrix)
            co1 = Vector((value[0][0], value[0][1], value[0][2]))          
            global_pos1 = bpy.data.objects["plane_matrix"].matrix_world * co1
            #global_pos1[2] += f_thickness/2   
            # depth patate
            global_pos1 += finger_normal * (f_thickness/3)
            
                # pinky refine
            if value[1] == "pinky_phal_1":
                global_pos1 = pinky_bot_vec + (get_object("pinky_top_auto").location - pinky_bot_vec)*0.70
            if value[1] == "pinky_phal_2":
                global_pos1 = pinky_bot_vec + (get_object("pinky_top_auto").location - pinky_bot_vec)*0.3
              
                   
            create_empty_loc(0.01, global_pos1, value[1])
        
     
        # hand empty         
        create_empty_loc(0.04, hand_empty_loc, "hand_loc")  
        
        #remove the matrix plane
        clear_object_selection()
        bpy.data.objects["plane_matrix"].select = True
        bpy.ops.object.delete()
        
    else:#no finger detection
        # hand empty  
        bpy.ops.object.mode_set(mode='OBJECT')
        create_empty_loc(0.04, hand_empty_loc, "hand_loc")  
        
        
    if debug:
        print("find foot...\n")
    
    # FOOT POSITION -------------------------------------------------------------------------
    body.select = True
    set_active_object(body.name)
    
    bpy.ops.object.mode_set(mode='EDIT')
    foot_loc_z_loc = foot_loc.location[2]
    foot_loc_x_loc = foot_loc.location[0]

    #select vertices around the foot_loc 
    selected_index = []
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    for v in mesh.verts:    
        if tolerance_check(v.co, foot_loc_z_loc, 2, body_height / 8.825, True):
            if v.co[2] <= foot_loc_z_loc:
                v.select = True
                selected_index.append(v.index)  

    bound_back = -10000.0
    bound_front = 10000.0
    bound_left = 10000.0
    bound_right = 0.0   
    
    #find the boundaries
    
    if debug:
        print("find foot boundaries...\n")
        
    clear_selection()
    
    for vi in selected_index:
        mesh.verts.ensure_lookup_table() #debug
        vert_y = mesh.verts[vi].co[1]
        vert_x = mesh.verts[vi].co[0]
        #back    
        if vert_y > bound_back:
            bound_back = vert_y
        #front
        if vert_y < bound_front:
            bound_front = vert_y        
        #left
        if vert_x < bound_left:
            bound_left = vert_x
        #right
        if vert_x > bound_right:
            bound_right = vert_x
   
    if debug:
        print("find toes...\n")
                 
    # Toes top
    bound_toes_top = 0.0

    for vi in selected_index:
        mesh.verts.ensure_lookup_table() #debug        
        #find the toes end vertices
        vert_co = mesh.verts[vi].co
        vert_y = mesh.verts[vi].co[1]
        vert_z = mesh.verts[vi].co[2]
        
        if tolerance_check(vert_co, bound_front, 1, body_depth / 7, True):
            if vert_z > bound_toes_top:
                bound_toes_top = vert_z
                mesh.verts[vi].select = True
                
    if debug:
        print("find ankle...\n")
                    
    # Ankle    
    clear_selection()
    ankle_selection = [] 
    for v in mesh.verts:    
        if tolerance_check(v.co, foot_loc.location[2], 2, body_height / 80, True):
            v.select = True    
            ankle_selection.append(v.index)            
    

    ankle_back = -10000
    ankle_front = 10000
    
    for va in ankle_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[va].co[1]        
        #front    
        if vert_y < ankle_front:
            ankle_front = vert_y
        # back
        if vert_y > ankle_back:
            ankle_back = vert_y        
    
  
    ankle_empty_loc = [foot_loc.location[0], 0, foot_loc.location[2]] 
    ankle_empty_loc[1] = ankle_back + (ankle_front - ankle_back)*0.25 
    
    if debug:
        print("find bank bones...\n")
    # Bank bones
    clear_selection()
    foot_bot_selection = [] 
    for v in mesh.verts:    
        if tolerance_check(v.co, 0.0, 2, body_height / 60, True):
            v.select = True    
            foot_bot_selection.append(v.index)            

    foot_bot_left = -10000
    foot_bot_right = 10000
    
    for vf in foot_bot_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_x = mesh.verts[vf].co[0]        
        #left    
        if vert_x < foot_bot_right:
            foot_bot_right = vert_x
        # back
        if vert_x > foot_bot_left:
            foot_bot_left = vert_x

    bpy.ops.object.mode_set(mode='OBJECT')

    toes_end_loc = [ankle_empty_loc[0], bound_front, bound_toes_top /2]
    toes_start_loc = [ankle_empty_loc[0], (bound_front + bound_back/2)*0.75, bound_toes_top /2]    
    bank_right_loc = [foot_bot_left, bound_back, 0]
    bank_left_loc = [foot_bot_right, bound_back, 0]
    bank_mid_loc = [(foot_bot_left+foot_bot_right)/2, bound_back, 0]
    
    # create empty location   
    foot_dict = {'ankle_loc':[ankle_empty_loc, "ankle_loc"], 'bank_left_loc':[bank_left_loc,"bank_left_loc"],'bank_right_loc':[bank_right_loc, "bank_right_loc"],'bank_mid_loc':[bank_mid_loc,"bank_mid_loc"],'toes_end':[toes_end_loc,"toes_end"],'toes_start':[toes_start_loc,"toes_start"]}

    for key, value in foot_dict.items():
        create_empty_loc(0.04, value[0], value[1])
        
    
    # ROOT POSITION --------------------------------------------------------------------------------------------
    if debug:
        print("find root position...\n")
    
        # get the loc guides
    root_loc = bpy.data.objects["root_loc"]
    set_active_object(body.name)
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    #select vertices in the overlapping sphere
    root_selection = []
    
    clear_selection()     
    for v in mesh.verts:    
        if tolerance_check_2(v.co, root_loc.location, 0, 2, body_width / 15):
            v.select = True   
    for i in range(0,3):
        bpy.ops.mesh.select_more()
        #exclude verts too high or too low
    for v in mesh.verts:    
        if not tolerance_check(v.co, root_loc.location[2], 2, body_width / 15, True):
            v.select = False
        if v.select == True:
            root_selection.append(v.index) 
    
   
    
    
    #find the hips boundaries
    if debug:
        print("find hips boundaries...\n")
        
    hips_back = 1000.0
    hips_front = -1000.0
    hips_left = 1000.0
    hips_right = 0.0   
   
    #find the boundaries
    clear_selection()
    for vr in root_selection:        
        mesh.verts.ensure_lookup_table() #debug
        mesh.verts[vr].select = True
        vert_y = mesh.verts[vr].co[1]
        vert_x = mesh.verts[vr].co[0]
        #back    
        if vert_y < hips_back:
            hips_back = vert_y
        #front
        if vert_y > hips_front:
            hips_front = vert_y        
        #left
        if vert_x < hips_left:
            hips_left = vert_x
        #right
        if vert_x > hips_right:
            hips_right = vert_x    
   
    
    
    # create root, legs and knee empty          
    root_empty_loc = [0, (hips_back+hips_front)/2, root_loc.location[2]]
    
    
     # LEGS POSITION --------------------------------------------------------------------------------------------
    
    if debug:
        print("find legs...\n")
     
    leg_empty_loc = [(hips_left+hips_right)/2, root_empty_loc[1], root_empty_loc[2]]
    knee_empty_loc = [(leg_empty_loc[0] + ankle_empty_loc[0])/2, 0, (leg_empty_loc[2] + ankle_empty_loc[2])/2]
    bot_empty_loc = [leg_empty_loc[0], hips_front, leg_empty_loc[2]]
     
    # find the knee boundaries
    
    if debug:
        print("find knee boundaries...\n")
        
    clear_selection()
    knee_selection = []     
    has_selected_knee = False
    sel_dist = body_height / 25
        
    while has_selected_knee == False:
        for vb in mesh.verts:    
            if tolerance_check(vb.co, knee_empty_loc[2], 2, sel_dist, True):
                vb.select = True    
                knee_selection.append(vb.index)
                has_selected_knee = True
                
        sel_dist *= 2        
    """
    for v in mesh.verts:    
        if tolerance_check(v.co, knee_empty_loc[2], 2, body_height / 25, True):
            v.select = True
            knee_selection.append(v.index)
    """
    knee_back = -1000
    knee_front = 1000
    
    for vk in knee_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vk].co[1]        
        #front    
        if vert_y < knee_front:
            knee_front = vert_y
        # back
        if vert_y > knee_back:
            knee_back = vert_y        
     
    knee_empty_loc[1] = knee_back + (knee_front - knee_back)*0.7            

    bpy.ops.object.mode_set(mode='OBJECT')
        
    create_empty_loc(0.04, root_empty_loc, "root_loc")
    create_empty_loc(0.04, leg_empty_loc, "leg_loc")
    create_empty_loc(0.04, knee_empty_loc, "knee_loc")
    create_empty_loc(0.04, bot_empty_loc, "bot_empty_loc")
    
    # SPINE POSITION ---------------------------------------------------------
    
    if debug:
        print("find neck...\n")
    
        # Neck
    neck_loc = bpy.data.objects["neck_loc"]
    set_active_object(body.name)
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    #select vertices in the overlapping neck sphere    
    neck_selection = []    
    clear_selection() 
    
    has_selected_neck = False
    sel_dist = body_height / 25
        
    while has_selected_neck == False:
        for vb in mesh.verts:    
            if tolerance_check_2(vb.co, neck_loc.location, 0, 2, sel_dist):
                vb.select = True    
                neck_selection.append(vb.index)
                has_selected_neck = True
                
        sel_dist *= 2        
    """
    for v in mesh.verts:    
        if tolerance_check_2(v.co, neck_loc.location, 0, 2, body_height / 25):
            v.select = True    
            neck_selection.append(v.index)
    """
    
    # find the neck bounds    
    if debug:
        print("find neck boundaries...\n")
    
    neck_back = -1000
    neck_front = 1000
 
    
    for vn in neck_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vn].co[1]        
        #front    
        if vert_y < neck_front:
            neck_front = vert_y
        # back
        if vert_y > neck_back:
            neck_back = vert_y  
     
        # Head        
    #select the top head vertices
    top_head_sel = []    
    clear_selection() 
        
    for v in mesh.verts:    
        if tolerance_check(v.co, body_height, 2, body_height / 20, True):
            v.select = True    
            top_head_sel.append(v.index)
    
    # find the head bounds
    
    if debug:
        print("find head boundaries...\n")
    
    top_head_back = -1000
    top_head_front = 1000
    
    for vh in top_head_sel:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vh].co[1]        
        #front    
        if vert_y < top_head_front:
            top_head_front = vert_y
        # back
        if vert_y > top_head_back:
            top_head_back = vert_y  
            
    
        
    
    # Neck         
    neck_empty_loc = [0, neck_back + (neck_front-neck_back)*0.3, neck_loc.location[2]]  
    # Spine 01
    spine_01_empty_loc = [0, root_empty_loc[1]+ (neck_empty_loc[1]-root_empty_loc[1])*1/3, root_empty_loc[2] + (neck_empty_loc[2]-root_empty_loc[2])*1/3]        
    # Spine 02
    spine_02_empty_loc = [0, root_empty_loc[1]+ (neck_empty_loc[1]-root_empty_loc[1])*2/3, root_empty_loc[2] + (neck_empty_loc[2]-root_empty_loc[2])*2/3] 
    # Head
    head_end_empty_loc = [0, (top_head_back+top_head_front)/2, body_height]
    head_empty_loc = [0, (head_end_empty_loc[1]+neck_empty_loc[1])/2, (neck_empty_loc[2]+head_end_empty_loc[2])*0.5]
    head_end_empty_loc[1] = head_empty_loc[1]
    
    # Breast        
    
    if debug:
        print("find breast...\n")
    
    #select vertices near spine02
    spine_02_selection = []    
    clear_selection() 
        
    for vb in mesh.verts:    
        if tolerance_check_2(vb.co, spine_02_empty_loc, 0, 2, body_height / 20):
            vb.select = True    
            spine_02_selection.append(vb.index)
          
    # find the spine 02 front bound
    spine_02_back = -1000
    spine_02_front = 1000
    
    if debug:
        print("find breast boundaries...\n")
    
    for vs in spine_02_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vs].co[1]        
        #front    
        if vert_y < spine_02_front:
            spine_02_front = vert_y
         #back    
        if vert_y > spine_02_back:
            spine_02_back = vert_y
            
    
    
    
    shoulder_pos = bpy.data.objects["shoulder_loc"].location
    
    breast_01_loc = [shoulder_pos[0]/2, spine_02_front, spine_02_empty_loc[2]] 
    breast_02_loc = [shoulder_pos[0]/2, breast_01_loc[1] + (shoulder_pos[1]-breast_01_loc[1])*0.4, spine_02_empty_loc[2]+ (shoulder_pos[2]-spine_02_empty_loc[2])*0.5] 
    
    spine_02_empty_loc[1] = spine_02_back + (spine_02_front - spine_02_back)*0.3
    
   
    if debug:
        print("find spine 01...\n")
    
    #select vertices near spine01
    spine_01_selection = []    
    clear_selection()
    has_selected_hips = False
    sel_dist = body_height / 30
        
    while has_selected_hips == False:
        for vb in mesh.verts:    
            if tolerance_check_2(vb.co, spine_01_empty_loc, 0, 2, sel_dist):
                vb.select = True    
                spine_01_selection.append(vb.index)
                has_selected_hips = True
                
        sel_dist *= 2
            
    #print(br)
          
    # find the spine 01 front bound
    spine_01_back = -1000
    spine_01_front = 1000
    
    for vs in spine_01_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vs].co[1]        
        #front    
        if vert_y < spine_01_front:
            spine_01_front = vert_y
         #back    
        if vert_y > spine_01_back:
            spine_01_back = vert_y
            

            
    
            
    spine_01_empty_loc[1] = spine_01_back + (spine_01_front - spine_01_back)*0.3 
      
    
    # create the empties       
    bpy.ops.object.mode_set(mode='OBJECT')
    create_empty_loc(0.04, neck_empty_loc, "neck_loc")
    create_empty_loc(0.04, spine_01_empty_loc, "spine_01_loc")
    create_empty_loc(0.04, spine_02_empty_loc, "spine_02_loc")
    create_empty_loc(0.04, head_end_empty_loc, "head_end_loc")
    create_empty_loc(0.04, head_empty_loc, "head_loc")
    create_empty_loc(0.04, breast_01_loc, "breast_01_loc")
    create_empty_loc(0.04, breast_02_loc, "breast_02_loc")
   
   # ARMS ---------------------------------------------------------------------
   
    if debug:
        print("find arms...\n")

    shoulder_loc = bpy.data.objects["shoulder_loc"]
    set_active_object(body.name)
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)
    
    #select vertices in the overlapping shoulder sphere
    shoulder_selection = []    
    clear_selection() 
    
    if debug:
        print("find shoulders vertices...\n")
        
    for v in mesh.verts:    
        if tolerance_check_2(v.co, shoulder_loc.location, 0, 2, body_height / 25):
            v.select = True    
            shoulder_selection.append(v.index)
    
    # find the shoulder bounds
    shoulder_back = -1000
    shoulder_front = 1000
    
    if debug:
        print("find shoulders boundaries...\n")
    
    for vs in shoulder_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[vs].co[1]        
        #front    
        if vert_y < shoulder_front:
            shoulder_front = vert_y
        # back
        if vert_y > shoulder_back:
            shoulder_back = vert_y  
    print(shoulder_front, shoulder_front)
    shoulder_empty_loc = [shoulder_loc.location[0], shoulder_back + (shoulder_front-shoulder_back)*0.4, shoulder_loc.location[2]]
    
    # shoulder_base
    shoulder_base_loc = [shoulder_empty_loc[0]/4, shoulder_empty_loc[1], shoulder_empty_loc[2]]
   
    
    # Elbow
    elbow_empty_loc = [(shoulder_empty_loc[0] + hand_empty_loc[0])/2, 0, (shoulder_empty_loc[2] + hand_empty_loc[2])/2]
     
        # find the elbow boundaries
        
    if debug:
        print("find elbow boundaries...\n")
        
    clear_selection()
    elbow_selection = []
    has_selected_v = False
    sel_rad = body_width / 20
    
    while has_selected_v == False:
        for v in mesh.verts:    
            if tolerance_check_2(v.co, elbow_empty_loc, 0, 2, sel_rad):
                v.select = True  
                has_selected_v = True  
                elbow_selection.append(v.index)
                
        if has_selected_v == False:
            sel_rad *= 2       
            
           
    
    elbow_back = -1000
    elbow_front = 1000
    
    for ve in elbow_selection:        
        mesh.verts.ensure_lookup_table() #debug        
        vert_y = mesh.verts[ve].co[1]        
        #front    
        if vert_y < elbow_front:
            elbow_front = vert_y
        # back
        if vert_y > elbow_back:
            elbow_back = vert_y        
     
    elbow_empty_loc[1] = elbow_back + (elbow_front - elbow_back)*0.3   
    
    # create the empties       
    bpy.ops.object.mode_set(mode='OBJECT')
    create_empty_loc(0.04, shoulder_empty_loc, "shoulder_loc")
    create_empty_loc(0.04, shoulder_base_loc, "shoulder_base_loc")
    create_empty_loc(0.04, elbow_empty_loc, "elbow_loc") 


    # END - UPDATE VIEW --------------------------------------------------
    bpy.ops.transform.translate(value=(0, 0, 0))
    
    if debug:
        print("END AUTO DETECTION...\n")
    
    
    
#-- end _auto_detect()     
    
def _delete_detected():
    clear_object_selection()
    bpy.data.objects["auto_detect_loc"].select = True
    bpy.context.scene.objects.active = bpy.data.objects["auto_detect_loc"]
    
    bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
    bpy.ops.object.delete()
    bpy.data.objects["auto_detect_loc"].select = True
    bpy.ops.object.delete()
    
def _delete_big_markers():
    clear_object_selection()
    bpy.data.objects["markers"].select = True
    bpy.context.scene.objects.active = bpy.data.objects["markers"]
    
    bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
    bpy.ops.object.delete()
    bpy.data.objects["markers"].select = True
    bpy.ops.object.delete()
    

def _set_front_view():
    
    bpy.context.scene.body_name = bpy.context.scene.objects.active.name

    bpy.ops.object.mode_set(mode='OBJECT')
    
    #get character mesh name
    body = bpy.data.objects[bpy.context.scene.body_name]
    
    #apply transforms
    bpy.ops.object.select_all(action='DESELECT')
    body.select = True
    bpy.context.scene.objects.active = body
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
   
    bpy.ops.object.mode_set(mode='EDIT')
    # set to vertex selection mode
    bpy.ops.mesh.select_mode(type="VERT")
    # remove double
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.remove_doubles(threshold=1e-006)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #center front view
    bpy.ops.view3d.viewnumpad(type='FRONT')
    bpy.ops.view3d.view_selected(use_all_regions=False)
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius = 0.01, view_align=False, location=(0,0,0), rotation=(0, 0, 0))   
    bpy.context.object.name = "markers"
    bpy.ops.object.select_all(action='DESELECT')
    #set ortho
    bpy.context.space_data.region_3d.view_perspective = 'ORTHO'


# COLLECTION PROPERTIES DEFINITION
class bone_transform(bpy.types.PropertyGroup):    
    head = bpy.props.FloatVectorProperty(name="Head Position", default=(0.0, 0.0, 0.0), subtype='TRANSLATION', size=3)
    tail = bpy.props.FloatVectorProperty(name="Tail Position", default=(0.0, 0.0, 0.0), subtype='TRANSLATION', size=3)
    roll = bpy.props.FloatProperty(name="Head Position", default=0.0)
    

# END FUNCTIONS

###########  UI PANEL  ###################

class proxy_utils_ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Auto-Rig Pro : Smart"
    bl_idname = "id_auto_rig_detect"
    
    @classmethod
    # buttons visibility conditions
    
    def poll(cls, context):
        if context.mode == 'POSE' or context.mode == 'OBJECT' or context.mode == 'EDIT_ARMATURE':
            return True
        else:
            return False
        
    def draw(self, context):
        layout = self.layout
        object = context.object
        scene = context.scene
        col = layout.column(align=False)
        
        button_state = 0
        
        #BUTTONS      

        try:
            bpy.data.objects["markers"]
            button_state = 1
            
            try:
                bpy.data.objects["neck_loc"]
                button_state = 2
            except:
                pass
            try:
                bpy.data.objects["shoulder_loc"]
                button_state = 3
            except:
                pass
            try:
                bpy.data.objects["hand_loc"]
                button_state = 4
            except:
                pass
            try:
                bpy.data.objects["root_loc"]
                button_state = 5
            except:
                pass
            try:
                bpy.data.objects["foot_loc"]
                button_state = 6
            except:
                pass
        
        except:
            pass
        
            
        if button_state == 0:
            layout.operator("id.set_front_view", text="Get Selected Body")
        
            
        if button_state > 0:   
            try:
                layout.label("Body: " + bpy.context.scene.body_name)   
            except:
                pass        
                
        if button_state == 1:    
            props = layout.operator("id.add_marker", text="Add Neck", icon = 'PLUS') 
            props.body_part = "neck"
        if button_state == 2:    
            props = layout.operator("id.add_marker", text="Add Shoulders", icon = 'PLUS') 
            props.body_part = "shoulder"    
        if button_state == 3:    
            props = layout.operator("id.add_marker", text="Add Wrists", icon = 'PLUS') 
            props.body_part = "hand"   
        if button_state == 4:    
            props = layout.operator("id.add_marker", text="Add Spine Root", icon = 'PLUS') 
            props.body_part = "root" 
        if button_state == 5:    
            props = layout.operator("id.add_marker", text="Add Ankles", icon = 'PLUS') 
            props.body_part = "foot"         

        if button_state == 6:
            
            layout.label("Auto-Detection:")     
            layout.operator("id.match_ref", text="Go!", icon='MOD_PARTICLES') 
            layout.prop(scene, "do_finger_detection", text="Find 5 Fingers")
            layout.separator() 
            
        if button_state > 0:           
            layout.operator("id.delete_big_markers", text="Delete Markers", icon='PANEL_CLOSE')
        
        layout.separator() 
        """
        layout.label("Beta testing tools")     
        layout.operator("id.auto_detect", text="Auto-Detect")
        layout.operator("id.delete_detected", text="Delete Detected", icon='X')
        layout.operator("id.match_ref_only", text="Match Ref Only")
        layout.separator() 
        
        #check
        """    
        
        

###########  REGISTER  ##################

def register():   
    bpy.types.Scene.body_name  = bpy.props.StringProperty(name="Body name", description = "Get the body object name")
    bpy.types.Scene.do_finger_detection = bpy.props.BoolProperty(name="Has Fingers", description = "Find 5 fingers on this character, if there are less than 5 or none it may result in buggy placement, turn it off and press the Go! button again", default = True)
    bpy.types.Scene.fingers_init_transform = bpy.props.CollectionProperty(type=bone_transform)
    
def unregister():   
    del bpy.types.Scene.body_name
    del bpy.types.Scene.do_finger_detection
    del bpy.types.Scene.fingers_init_transform
    


    