# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# This script by Lionel Zamouth

import bpy
from . import props
from . import settings
from .utils import *
from .labels import getLabel


def base_poll(cls, context):
    rd = context.scene.render
    return (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)

# Main Octane Panel


class OctaneRenderButtonsPanel():
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'OCT_RENDER' and rd.use_game_engine is False

# Octane Render Plugin Panel


class RENDER_OCT_render_settings(OctaneRenderButtonsPanel, bpy.types.Panel):
    bl_label = "Octane Community Plugin " + props.Version
    COMPAT_ENGINES = {'OCT_RENDER'}

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SEQUENCE')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        octane_render = scene.octane_render
        blender_render = scene.render

        layout.prop(octane_render, "export_mode", expand=True)
        if octane_render.export_mode == "MODE_GEOMETRY":
            layout.operator("ops.button_export_geometry", icon='MESH_DATA')
        else:
            if octane_render.export_mode == "MODE_IMAGE":
                layout.operator("ops.button_export_image", icon='RENDER_STILL')
                layout.prop(octane_render, "export_camera_only")
                row = layout.row()
                col = row.column()
                col.prop(octane_render, "export_samples_per_image")
                col = row.column()
                col.operator_menu_enum('ops.menu_export_presets', 'export_samples_presets', 'Samples Presets')
                layout.prop(octane_render, "import_render")
            elif octane_render.export_mode == "MODE_ANIMATION":
                layout.operator("ops.button_export_animation", icon='RENDER_ANIMATION')
                layout.prop(octane_render, "export_camera_only")
                row = layout.row()
                col = row.column()
                col.prop(octane_render, "image_output")
                row = layout.row()
                col = row.column()
                col.prop(octane_render, "export_samples_per_image")
                col = row.column()
                col.operator_menu_enum('ops.menu_export_presets', 'export_samples_presets', 'Samples Presets')
                layout.prop(octane_render, "output_mode", expand=True)

        if octane_render.import_render and octane_render.export_mode == "MODE_IMAGE":
            row = layout.row()
            col = row.column()
            col.prop(octane_render, "image_output")
            layout.prop(octane_render, "output_mode", expand=True)

# Dimensions Panel


class RENDER_OCT_dimensions(OctaneRenderButtonsPanel, bpy.types.Panel):
    bl_idname = "Dimensions"
    bl_label = "Dimensions"
    COMPAT_ENGINES = {'OCT_RENDER'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SEQUENCE')

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        octane_render = scene.octane_render
        rd = scene.render

        if rd.pixel_aspect_x != 1 or rd.pixel_aspect_y != 1:
            layout.label("Unsupported pixel aspect ratio - must be 1:1", icon='ERROR')
            layout.operator("octane.fixaspect")
            return

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text="", icon="ZOOMIN")
        row.operator("render.preset_add", text="", icon="ZOOMOUT").remove_active = True

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.prop(rd, "resolution_percentage", text="")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Settings:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")
        sub.prop(rd, "fps")

# Octane Project Settings Panel


class RENDER_OCT_project_settings(OctaneRenderButtonsPanel, bpy.types.Panel):
    bl_label = "Octane Project Settings"
    COMPAT_ENGINES = {'OCT_RENDER'}

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='URL')

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        octane_render = scene.octane_render

        if octane_render.path == "":
            layout.prop(octane_render, "path", icon='ERROR')
        else:
            layout.prop(octane_render, "path")

        if octane_render.project_name == "":
            layout.prop(octane_render, "project_name", icon='ERROR')
        else:
            layout.prop(octane_render, "project_name")

        layout.prop(octane_render, "unit_size")
        layout.prop(octane_render, "node_render_geometry")
        layout.prop(octane_render, "node_render_target")
        layout.prop(octane_render, "export_camera")
        layout.prop(octane_render, "export_resolution")
        # layout.prop(octane_render, "export_instances")
        # if octane_render.export_instances:
        #     row = layout.row()
        #     row.prop(octane_render, "instances_export_mode", expand=True)
        #     col = layout.column(align=True)
        #     col.prop(octane_render, "instances_write_dupli")
        #     if octane_render.instances_export_mode == 'Manual':
        #         col.operator("ops.instances_export_selected")


# Octane Export Settings
class RENDER_OCT_export_settings(OctaneRenderButtonsPanel, bpy.types.Panel):
    bl_label = "Octane Export Settings"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'OCT_RENDER'}

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SCRIPTWIN')

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        octane_render = scene.octane_render

        # Context
        row = layout.row()
        row.label(text=" Context", icon='GROUP')
        row = layout.row()
        split = row.split(align=True)
        col = split.column()
        col.prop(octane_render, "export_sel_only")
        col = split.column()
        col.prop(octane_render, "export_remove_hidden")
        col = split.column()
        col.prop(octane_render, "export_remove_invisible")

        # Output options
        layout.separator()
        row = layout.row()
        row.label(text=" Output Options", icon='MOD_MESHDEFORM')
        row = layout.row()
        split = row.split(align=True)

        col = split.column()
        col.prop(octane_render, "export_apply_modifiers")
        col = split.column()
        col.prop(octane_render, "export_ROTX90")
        col = split.column()
        col.prop(octane_render, "export_copy_images")

        layout.separator()
        row = layout.row()
        row.label(text=" Export Options", icon='SETTINGS')

        row = layout.row()
        split = row.split(align=True)
        col = split.column()
        col.prop(octane_render, "export_edges")
        col = split.column()
        col.prop(octane_render, "export_tri")
        col = split.column()
        col.prop(octane_render, "export_materials")
        col = split.column()
        col.prop(octane_render, "export_UV")

        row = layout.row()
        split = row.split(align=True)
        col = split.column()
        col.prop(octane_render, "export_normals")
        col = split.column()
        col.prop(octane_render, "export_HQ")
        col = split.column()
        col.prop(octane_render, "export_polygroups")
        col = split.column()
        col.prop(octane_render, "export_curves_as_nurbs")

# Octane System Settings


class RENDER_OCT_system_settings(OctaneRenderButtonsPanel, bpy.types.Panel):
    bl_label = "Octane System Settings"
    COMPAT_ENGINES = {'OCT_RENDER'}

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='RADIO')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        octane_render = scene.octane_render
        if octane_render.binary == "":
            layout.prop(octane_render, "binary", icon='ERROR')
        else:
            layout.prop(octane_render, "binary")

        row = layout.row()
        split = row.split(align=True)
        col = split.column()
        col.prop(octane_render, "GPU_selector")
        if octane_render.GPU_selector:
            col = split.column()
            col.prop(octane_render, "GPU_use_list")
        layout.prop(octane_render, "verbose")
        if octane_render.verbose is True:
            if octanerender.Verbose is False:
                octanerender.Verbose = True
                log('Turning verbose mode on')
            octanerender.Verbose = True
        else:
            if octanerender.Verbose is True:
                log('Turning verbose mode off')
            octanerender.Verbose = False
        layout.prop(octane_render, 'double_specular')
        # layout.prop(octane_render,'ignore_intensity')


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
