
#bl_info = {
#    "name": "Snap to Center (offset)",
#    "location": "Search tool",
#    "description": "Snap selected objects to center with offset.",
#    "author": "Spirou4D",
#    "version": (0,2),
#    "blender": (2, 6, 9),
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "3D View",
#    }
import bpy

###------ Create Snapping Operators -------###
   
class snapcenteroffset(bpy.types.Operator):
    """Snap the currently selected objects to Center with offset"""
    bl_idname = "mesh.snapcenteroffset"
    bl_label = "Selection to center (offset)"
    bl_options = {'REGISTER', 'UNDO'}     
    
    
    @classmethod        
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
    def execute(self, context):

        scene = bpy.context.scene
        #activeObj = context.active_object
        selected = context.selected_objects

        if selected:
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor()
        else:
            self.report({'INFO'}, "No objects selected") 

        return {"FINISHED"}     


## -----------------------------------SELECT LEFT---------------------
def side (self, nombre, offset):

    bpy.ops.object.mode_set(mode="EDIT", toggle=0)
    OBJECT = bpy.context.active_object
    ODATA = bmesh.from_edit_mesh(OBJECT.data)
    MODE = bpy.context.mode
    bpy.context.tool_settings.mesh_select_mode = (True, False, False)
    for VERTICE in ODATA.verts[:]:
        VERTICE.select = False
    if nombre == False:
        for VERTICES in ODATA.verts[:]:
            if VERTICES.co[0] < (offset):
                VERTICES.select = 1
    else:
        for VERTICES in ODATA.verts[:]:
            if VERTICES.co[0] > (offset):
                VERTICES.select = 1
    ODATA.select_flush(False)
    bpy.ops.object.mode_set(mode="EDIT", toggle=0)

class SelectMenor (bpy.types.Operator):
    bl_idname = "mesh.select_side_osc"
    bl_label = "Select Side"
    bl_options = {"REGISTER", "UNDO"}

    side = bpy.props.BoolProperty(name="Greater than zero", default=False)
    offset = bpy.props.FloatProperty(name="Offset", default=0)
    def execute(self,context):

        side(self, self.side, self.offset)

        return {'FINISHED'}

###------  Functions Menu add -------###
def menu_display(self, context):
    self.layout.operator(snapcenteroffset.bl_idname, icon="PLUGIN")

###------  Functions Menu add -------###
def menu_display(self, context):
    self.layout.operator(snapcenteroffset.bl_idname, icon="PLUGIN")

"""      
def register():
# Register menu
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(snapcenteroffset)
    bpy.types.VIEW3D_MT_snap.append(menu_display) 

def unregister():
# Unregister menu
    #bpy.utils.unregister_class(snapcenteroffset)
    bpy.types.VIEW3D_MT_snap.remove(menu_display)
    bpy.utils.unregister_module(__name__)

"""








