import bpy
import bgl
import blf
 
step = 10
 
def draw_callback_px(self, context):
 
    font_id = 0
    x, y = self.mouse
    
    width = context.region.width 
    height = context.region.height
    if x < 0 or x > width:
        return 
    st = context.scene.frame_start
    et = context.scene.frame_end
    frame_width = width / (et - st)
    frame = int(st + x / frame_width)
    # draw some text
    blf.size(font_id, 15, 80)
    blf.position(font_id, 80, 30, 0)
    blf.draw(font_id, 'Time line')
    i = 0
    
    for i in range(0, width, int(width/ 10)):
        bgl.glColor4f(1, 1, 1, 0.5)
        blf.position(font_id, i+3, 2,0)
        blf.size(font_id, 12, 80)
        print(st, i, frame_width, x, frame)
        blf.draw(font_id, "%d" % (st + i / frame_width))
        bgl.glLineWidth(2)            
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_LINES)
        bgl.glColor4f(1,1,1,0.3)
        bgl.glVertex2i(i, 0)
        bgl.glVertex2i(i, 10)
        bgl.glEnd()
        i += int(20 * frame_width)
       
    blf.position(font_id, x, 60,50)
    blf.draw(font_id, "%d" % (frame))
   
    #pixel width line
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0, 1, 0, 0.5)
    bgl.glLineWidth(6)
 
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2i(x, 0)
    bgl.glVertex2i(x, 80)
    #bgl.glVertex2i(0, y)
    #bgl.glVertex2i(width, y)
    bgl.glColor4f(1, 1, 1, 0.5)
    bgl.glEnd()
 
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    context.scene.frame_set(frame)
 
 
class ScrubTimelineKey(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "anim.scrubberkey"
    bl_label = "Scrub timeline"
    bl_options = {'REGISTER', 'UNDO'}
   
    def __init__(self):
        print("Start")
 
    def __del__(self):
        print("End")
   
    Scale = bpy.props.FloatProperty(name="Sensitivity Scale", default=1)
    ScaleBySceneLength = bpy.props.BoolProperty(name="Adjust Sensitivity With Scene Length", default=True)
    StandardSceneLength = bpy.props.FloatProperty(name="Standard Scene Length", default=100)
    LengthScale = bpy.props.FloatProperty(name="Length Scale", default=1)
   
    def modal(self, context, event):
        context.area.tag_redraw()
        frame = context.scene.frame_current
        
        if event.type == 'MOUSEMOVE':  #move frames
            self.mouse = (event.mouse_region_x, event.mouse_region_y)
        elif event.type == 'LEFTMOUSE' and event.value == "RELEASE":  # Confirm
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        return {'RUNNING_MODAL'}
 
    def invoke(self, context, event):
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
 
        self.mouse = (0, 0)
        self.sframe = bpy.context.scene.frame_current
        self.dampedvalue = event.mouse_x / 10 * self.Scale * ((((bpy.context.scene.frame_end / self.StandardSceneLength)*self.LengthScale) * self.ScaleBySceneLength) + 1)
        self.looped = 0
   
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
 
       
# store keymaps here to access after registration
addon_fkeymaps = []
           
def register():
    bpy.utils.register_class(ScrubTimelineKey)
       
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('anim.scrubberkey', 'LEFTMOUSE', 'PRESS', alt=True)  
    addon_fkeymaps.append(km)
 
 
def unregister():
    bpy.utils.unregister_class(ScrubTimelineKey)
   
    wm = bpy.context.window_manager
    for km in addon_fkeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
   
    del addon_fkeymaps[:]
 
if __name__ == "__main__":
    register()