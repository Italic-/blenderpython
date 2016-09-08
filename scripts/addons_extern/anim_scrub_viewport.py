import bpy

bl_info = {
    "name": "Viewport Time Scrub",
    "author": "Frankie",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "3d view -> ALT+LMB drag",
    "description": "Allows scrubbing with the cursor over the viewport.",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
}


class ScrubTimelineKey(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "anim.scrubberkey"
    bl_label = "Scrub timeline"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        self.valued = event.mouse_x / 10
        if event.type == 'MOUSEMOVE':  # move frames
            if bpy.context.scene.frame_current > bpy.context.scene.frame_end:
                bpy.context.scene.frame_set(bpy.context.scene.frame_start)
                self.looped += 1
            elif bpy.context.scene.frame_current < bpy.context.scene.frame_start:
                bpy.context.scene.frame_set(bpy.context.scene.frame_end)
                self.looped -= 1
            else:
                bpy.context.scene.frame_set(self.valued - self.dampedvalue + self.sframe - (bpy.context.scene.frame_end * self.looped))
        elif event.type == 'LEFTMOUSE' and event.value == "RELEASE":  # Confirm
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sframe = bpy.context.scene.frame_current
        self.value = event.mouse_x
        self.dampedvalue = event.mouse_x / 10
        self.looped = 0
        # self.a = bpy.context.object.name

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


addon_fkeymaps = []


def register():
    bpy.utils.register_module(__name__)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    km.keymap_items.new('anim.scrubberkey', 'LEFTMOUSE', 'PRESS', alt=True)
    addon_fkeymaps.append(km)


def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager
    for km in addon_fkeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    addon_fkeymaps.clear()


if __name__ == "__main__":
    register()
