import bpy
from bpy.props import BoolProperty, PointerProperty, FloatProperty, CollectionProperty, IntProperty, StringProperty
from . window_operations import splitV3DtoBLS
from . light_profiles import ListItem, update_list_index
from . common import isFamily, family, findLightGrp, refreshMaterials
import os

_ = os.sep


def getLightMesh():
    obs = bpy.context.scene.objects
    lightGrp = obs.active
    light_no = lightGrp.name.split('.')[1]
    return obs[obs.find('BLS_LIGHT_MESH.' + light_no)]


class Blender_Light_Studio_Properties(bpy.types.PropertyGroup):
    initialized = BoolProperty(default=False)

    def get_light_x(self):
        return getLightMesh().location.x

    def set_light_x(self, context):
        getLightMesh().location.x = context

    def get_light_hidden(self):
        return getLightMesh().hide_render

    def set_light_hidden(self, context):
        light = getLightMesh()
        light.hide_render = context
        light.hide = context
        bpy.context.scene.frame_current = bpy.context.scene.frame_current  # refresh hack
        refreshMaterials()

    light_radius = FloatProperty(name="Light Distance", default=30.0, min=0.5, set=set_light_x, step=5, get=get_light_x)
    light_muted = BoolProperty(name="Mute Light", default=False, set=set_light_hidden, get=get_light_hidden)

    ''' Profile List '''
    profile_list = CollectionProperty(type=ListItem)
    list_index = IntProperty(name="Index for profile_list", default=0, update=update_list_index)
    last_empty = StringProperty(name="Name of last Empty holding profile", default="")


class CreateBlenderLightStudio(bpy.types.Operator):
    bl_idname = "scene.create_blender_light_studio"
    bl_label = "Create Light Studio"
    bl_description = "Append Blender Light Studio to current scene"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and not context.scene.BLStudio.initialized

    def execute(self, context):
        script_file = os.path.realpath(__file__)
        dir = os.path.dirname(script_file)

        bpy.ops.wm.append(filepath=_ + 'BLS_V1_02_simple.blend' + _ + 'Object' + _,
                          directory=os.path.join(dir, "BLS_V1_02_simple.blend" + _ + "Object" + _),
                          filename="BLENDER_LIGHT_STUDIO",
                          active_layer=False)

        bpy.ops.wm.append(filepath=_ + 'BLS_V1_02_simple.blend' + _ + 'Object' + _,
                          directory=os.path.join(dir, "BLS_V1_02_simple.blend" + _ + "Object" + _),
                          filename="BLS_PANEL",
                          active_layer=False)

        cpanel = [ob for ob in bpy.context.scene.objects if ob.name.startswith('BLS_PANEL')][0]
        cpanel.parent = [ob for ob in bpy.context.scene.objects if ob.name.startswith('BLENDER_LIGHT_STUDIO')][0]

        bpy.ops.bls_list.new_profile()

        context.scene.BLStudio.initialized = True

        return {"FINISHED"}


class DeleteBlenderLightStudio(bpy.types.Operator):
    bl_idname = "scene.delete_blender_light_studio"
    bl_label = "Delete Studio"
    bl_description = "Delete Blender Light Studio from current scene"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def execute(self, context):
        scene = context.scene
        scene.BLStudio.initialized = False

        ''' for each profile from this scene: delete objects then remove from list '''
        while len(context.scene.BLStudio.profile_list):
            bpy.ops.bls_list.delete_profile()

        obsToRemove = [ob for ob in scene.objects if isFamily(ob)]
        for ob in obsToRemove:
            scene.objects.unlink(ob)
            for gr in ob.users_group:
                gr.objects.unlink(ob)
            ob.user_clear()
            ob.use_fake_user = False
            bpy.data.objects.remove(ob)

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Deleting Studio is irreversible!")
        col.label(text="Your lighting setup will be lost.")


class AddBSLight(bpy.types.Operator):
    bl_idname = "scene.add_blender_studio_light"
    bl_label = "Add Studio Light"
    bl_description = "Add Light to Studio"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def execute(self, context):
        script_file = os.path.realpath(__file__)
        dir = os.path.dirname(script_file)

        scene = context.scene
        bls = [ob for ob in bpy.context.scene.objects if ob.name.startswith('BLENDER_LIGHT_STUDIO')][0]

        # before
        A = set(bpy.data.groups[:])

        bpy.ops.wm.append(filepath=_ + 'BLS_V1_02_simple.blend' + _ + 'Group' + _,
                          directory=os.path.join(dir, "BLS_V1_02_simple.blend" + _ + "Group" + _),
                          filename="BLS_Light",
                          active_layer=False)

        # after operation
        B = set(bpy.data.groups[:])

        # whats the difference
        new_objects = (A ^ B).pop().objects

        for ob in new_objects:
            ob.use_fake_user = True

        lightGrp = [l for l in new_objects if l.name.startswith('BLS_LIGHT_GRP')][0]
        lightGrp.parent = [ob for ob in bpy.context.scene.objects if ob and ob.name.startswith('BLS_PROFILE') and isFamily(ob)][0]

        bpy.ops.object.select_all(action='DESELECT')
        light = [p for p in new_objects if p.name.startswith('BLS_LIGHT_MESH')][0]
        light.select = True
        panel = [p for p in new_objects if p.name.startswith('BLS_CONTROLLER')][0]
        panel.select = True
        context.scene.objects.active = panel

        bpy.context.scene.frame_current = bpy.context.scene.frame_current  # refresh hack
        refreshMaterials()

        return {"FINISHED"}


class DeleteBSLight(bpy.types.Operator):
    bl_idname = "scene.delete_blender_studio_light"
    bl_label = "Delete Studio Light"
    bl_description = "Delete selected Light from Studio"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        light = context.scene.objects.active
        return context.area.type == 'VIEW_3D' and \
            context.mode == 'OBJECT' and \
            context.scene.BLStudio.initialized and \
            light and \
            (light.name.startswith('BLS_CONTROLLER') or light.name.startswith('BLS_LIGHT_MESH'))

    def execute(self, context):
        scene = context.scene
        oldlaysArea = context.area.spaces[0].layers[:]
        oldlaysScene = context.scene.layers[:]
        context.area.spaces[0].layers = [True] * 20
        context.scene.layers = [True] * 20

        light = bpy.context.active_object

        lightGrp = findLightGrp(light)
        ending = lightGrp.name.split('.')[1]

        #obsToRemove = [ob for ob in scene.objects if not ob.name.startswith('BLS_PROFILE.') and ob.name.endswith(ending) and isFamily(ob)]
        # print(obsToRemove)
        for ob in family(lightGrp):
            scene.objects.unlink(ob)
            for gr in ob.users_group:
                gr.objects.unlink(ob)
            ob.user_clear()
            ob.use_fake_user = False
            bpy.data.objects.remove(ob)

        context.area.spaces[0].layers = oldlaysArea
        context.scene.layers = oldlaysScene

        return {"FINISHED"}


class PrepareBSLV3D(bpy.types.Operator):
    bl_idname = "scene.prepare_blender_studio_light"
    bl_label = "Prepare Layout"
    bl_description = "Split current Viewport for easier Studio usage."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def execute(self, context):
        splitV3DtoBLS(context)
        context.scene.render.engine = "CYCLES"
        return {"FINISHED"}


class BSL_MuteOtherLights(bpy.types.Operator):
    bl_idname = "object.mute_other_lights"
    bl_label = "Show Only This Light"
    bl_description = "Show only this light."
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def execute(self, context):
        obs = context.scene.objects
        lightGrp = obs.active
        light_no = lightGrp.name.split('.')[1]

        for light in (ob for ob in obs if ob.name.startswith('BLS_LIGHT_MESH') and isFamily(ob)):
            if light.name[-3:] == light_no:
                light.hide_render = False
                light.hide = False
            else:
                light.hide_render = True
                light.hide = True

        context.scene.frame_current = context.scene.frame_current  # refresh hack
        refreshMaterials()

        return {"FINISHED"}


class BSL_ShowAllLights(bpy.types.Operator):
    bl_idname = "object.show_all_lights"
    bl_label = "Show All Lights"
    bl_description = "Show all lights."
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def execute(self, context):
        obs = context.scene.objects
        lightGrp = obs.active
        light_no = lightGrp.name.split('.')[1]

        for light in (ob for ob in obs if ob.name.startswith('BLS_LIGHT_MESH') and isFamily(ob)):
            light.hide_render = False
            light.hide = False

        context.scene.frame_current = context.scene.frame_current  # refresh hack
        refreshMaterials()

        return {"FINISHED"}


class BlenderLightStudioPanelStudio(bpy.types.Panel):
    bl_idname = "blender_light_studio_panel_studio"
    bl_label = "BLight Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        if not context.scene.BLStudio.initialized:
            col.operator('scene.create_blender_light_studio')
        if context.scene.BLStudio.initialized:
            col.operator('scene.delete_blender_light_studio')
        col.operator('scene.prepare_blender_studio_light')


class BlenderLightStudioPanelLight(bpy.types.Panel):
    bl_idname = "blender_light_studio_panel_light"
    bl_label = "BLights"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and len(context.scene.BLStudio.profile_list)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator('scene.add_blender_studio_light', text='Add Light')
        row.operator('scene.delete_blender_studio_light', text='Delete Light')


class BLS_ProfileList(bpy.types.Panel):
    bl_idname = "bls_profile_list"
    bl_label = "BLight Profiles"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT' and context.scene.BLStudio.initialized

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        props = scene.BLStudio

        row = layout.row()
        col = row.column()
        col.template_list("BLS_UL_List", "Profile_List", props, "profile_list", props, "list_index", rows=5)

        col = row.column(align=True)
        col.operator('bls_list.new_profile', icon='ZOOMIN', text="")
        col.operator('bls_list.delete_profile', icon='ZOOMOUT', text="")
        col.operator('bls_list.copy_profile', icon='GHOST', text="")

        col.separator()
        col.operator('bls_list.move_profile', text='', icon="TRIA_UP").direction = 'UP'
        col.operator('bls_list.move_profile', text='', icon="TRIA_DOWN").direction = 'DOWN'

        row = layout.row()


class BlenderLightStudioPanelSelected(bpy.types.Panel):
    bl_idname = "blender_light_studio_panel_selected"
    bl_label = "BLight Selected"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def draw(self, context):
        if context.scene.objects.active and (context.scene.objects.active.name.startswith('BLS_CONTROLLER') or context.scene.objects.active.name.startswith('BLS_LIGHT_MESH')):
            layout = self.layout
            col = layout.column(align=True)
            col.prop(context.scene.BLStudio, 'light_radius')

            col = layout.column(align=True)
            col.prop(context.scene.BLStudio, 'light_muted')
            col = layout.column(align=True)
            col.operator('object.mute_other_lights')
            col.operator('object.show_all_lights')
