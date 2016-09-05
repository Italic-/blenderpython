bl_info = {
    "name": "Alternate Object Hiding",
    "author": "Jonathan Williamson",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D",
    "description": "Unhides objects while keeping them deselected",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}


import bpy


class AlternateUnhide(bpy.types.Operator):
    '''Unhide objects in the current scene while keeping them deselected.'''
    bl_idname = "objects.alternate_unhide"
    bl_label = "Unhide Objects and Keep Deselected"

    def execute(self, context):
        scene = context.scene
        unhide_objects(scene)

        return {'FINISHED'}


def unhide_objects(scene):
    for obj in scene.objects:
        if obj.hide is True:
            obj.hide = False


def register():
    bpy.utils.register_class(AlternateUnhide)


def unregister():
    bpy.utils.unregister_class(AlternateUnhide)


if __name__ == "__main__":
    register()
