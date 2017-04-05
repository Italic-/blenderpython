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

# @author Lionel Zamouth, Matej Moderc (1.5+ version maintenance)
# This directory is a Python package.

bl_info = {
    "name": "OctaneRender Community Plugin",
    "author": "Lionel Zamouth, Matej Moderc",
    "version": (1, 5, 1),
    "blender": (2, 6, 2),
    "api": 45110,
    "location": "Info Header - Engine dropdown",
    "description": "OctaneRender community plugin - UNOFFICIAL",
    "warning": " This is NOT the official plugin from Otoy",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "Render"}
Version = 'v1.51'
Supported = False


Verbose = True
Status_Display = False
Status_Text = ""
Status_Severity = 0
replace_project = False

cameraUpdateOnly = False
launchOctane = False
flyMode = False
bucketMode = False
pullImage = False
maxSamples = 0
frameStart = 1
frameStop = 1
frameCurrent = 1
frameStep = 1
delayed_copies = []
dst_dir = ""

# To support reload properly, try to access a package var, if it's there, reload everything
if "octane_data" in locals():
    import imp
    imp.reload(scripting)
    imp.reload(settings)
    imp.reload(utils)
    imp.reload(operators)
    imp.reload(ui_render)
    imp.reload(ui_world)
    imp.reload(ui_material)
    #imp.reload(ui_texture)
    imp.reload(ui_camera)
    imp.reload(properties)
    imp.reload(instances)
    imp.reload(export)
    imp.reload(engine)

else:
    from . import scripting
    from . import settings
    from . import utils
    from . import operators
    from . import ui_render
    from . import ui_world
    from . import ui_material
    #from . import ui_texture
    from . import ui_camera
    from . import properties
    from . import instances
    from . import export
    from . import engine

octane_data = True

# force reload
def reload():
    print("Octanerender: forced reload")
    import imp
    from . import scripting
    from . import settings
    from . import utils
    from . import operators
    from . import ui_render
    from . import ui_world
    from . import ui_material
    from . import ui_camera
    from . import properties
    from . import instances
    from . import export
    from . import engine
    imp.reload(scripting)
    imp.reload(settings)
    imp.reload(utils)
    imp.reload(operators)
    imp.reload(ui_render)
    imp.reload(ui_world)
    imp.reload(ui_material)
    imp.reload(ui_camera)
    imp.reload(properties)
    imp.reload(instances)
    imp.reload(export)
    imp.reload(engine)
    register()


def register():
    import bpy
    bpy.utils.register_module(__name__)
    settings.addProperties()


def unregister():
    import bpy
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.octane_render
