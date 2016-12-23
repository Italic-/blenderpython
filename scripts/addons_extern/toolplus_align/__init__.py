# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and / or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "T+ Align",
    "author": "MKB, Multi Authors (see URL)",
    "version": (0, 1, 1),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N]",
    "description": "Align Tools Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}


#line for the panels
from toolplus_align.align_batch         import (View3D_TP_Align_Menu)

from toolplus_align.align_ui_main       import (VIEW3D_TP_Align_Panel_TOOLS)
from toolplus_align.align_ui_main       import (VIEW3D_TP_Align_Panel_UI)

from toolplus_align.align_ui_snap       import (VIEW3D_TP_Align_Snap_Panel_TOOLS)
from toolplus_align.align_ui_snap       import (VIEW3D_TP_Align_Snap_Panel_UI)

from toolplus_align.align_ui_relax      import (VIEW3D_TP_Align_Relax_Panel_TOOLS)
from toolplus_align.align_ui_relax      import (VIEW3D_TP_Align_Relax_Panel_UI)

from toolplus_align.align_looptools     import (LoopToolsProps)
from toolplus_align.align_1d_scripts    import (paul_managerProps)



##################################

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_align'))

if "bpy" in locals():
    import imp
    imp.reload(align_1d_scripts)
    imp.reload(align_advanced)
    imp.reload(align_batch)
    imp.reload(align_by_normal)
    imp.reload(align_con_rotation)
    imp.reload(align_distribute_obj)
    imp.reload(align_face_to_face)
    imp.reload(align_lookatit)
    imp.reload(align_looptools)
    imp.reload(align_mirror)
    imp.reload(align_pivot)
    imp.reload(align_setups)
    imp.reload(align_shrinksmooth)
    imp.reload(align_simple)
    imp.reload(align_snap)
    imp.reload(align_snap_offset)
    imp.reload(align_straighten)
    imp.reload(align_to_ground)
    imp.reload(align_transform)
    imp.reload(align_vertices) 
else:
    from . import align_1d_scripts         
    from . import align_advanced           
    from . import align_batch          
    from . import align_by_normal          
    from . import align_con_rotation       
    from . import align_distribute_obj     
    from . import align_face_to_face       
    from . import align_lookatit           
    from . import align_looptools          
    from . import align_mirror             
    from . import align_pivot              
    from . import align_setups             
    from . import align_shrinksmooth       
    from . import align_simple             
    from . import align_snap               
    from . import align_snap_offset         
    from . import align_straighten          
    from . import align_to_ground           
    from . import align_transform           
    from . import align_vertices          


##################################

import bpy
from bpy import *

import bpy.utils.previews
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)


def update_panel_position_align(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Align_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_align == 'tools':
        
        VIEW3D_TP_Align_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_align
        bpy.utils.register_class(VIEW3D_TP_Align_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_align == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Align_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_align == 'off':
        pass
  

def update_panel_position_snap(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Snap_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Align_Snap_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Snap_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_snap == 'tools':
        VIEW3D_TP_Align_Snap_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_snap
        bpy.utils.register_class(VIEW3D_TP_Align_Snap_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_snap == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Align_Snap_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_snap == 'off':
        pass


def update_panel_position_relax(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Relax_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Align_Relax_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Align_Relax_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_relax == 'tools':
        VIEW3D_TP_Align_Relax_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_relax
        bpy.utils.register_class(VIEW3D_TP_Align_Relax_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_relax == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Align_Relax_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_relax == 'off':
        pass



def update_display_tools(self, context):

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'on':
        return True

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'off':
        pass 




addon_keymaps_menu = []

def update_menu(self, context):
    try:
        bpy.utils.unregister_class(View3D_TP_Align_Menu)
        
        # Keymapping
        # remove keymaps when add-on is deactivated
        wm = bpy.context.window_manager
        for km in addon_keymaps_menu:
            wm.keyconfigs.addon.keymaps.remove(km)
        del addon_keymaps_menu[:]
        
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'menu':
     
        View3D_TP_Align_Menu.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_menu
    
        bpy.utils.register_class(View3D_TP_Align_Menu)
    
        # Keymapping 
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('tp_batch.align_menu', 'ONE', 'PRESS', alt=True) #,ctrl=True, shift=True, 
        #kmi.properties.name = ''

    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'off':
        pass




#Panel preferences
class TP_Panels_Preferences(AddonPreferences):
    bl_idname = __name__
    
    prefs_tabs = EnumProperty(
        items=(('info',       "Info",       "Info"),
               ('toolsets',   "Tools",      "Tools"),
               ('location',   "Location",   "Location"),
               ('keymap',     "Keymap",     "Keymap"),  
               ('url',        "URLs",       "URLs")),
               default='info')

    #Tab Location           
    tab_location_align = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'place panel in the property shelf [N]')),
               default='tools', update = update_panel_position_align)

    tab_location_snap = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'disable panel in the shelfs')),
               default='tools', update = update_panel_position_snap)

    tab_location_relax = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'disable panel in the shelfs')),
               default='tools', update = update_panel_position_relax)

    tab_menu_view = EnumProperty(
        name = '3d View Menu',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('menu', 'Menu on', 'enable menu for 3d view'),
               ('off', 'Menu off', 'enable or disable menu for 3d view')),
               default='menu', update = update_menu)


    #Align

    tab_normals = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Normals on', 'enable tools in panel'), ('off', 'Normals off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_orientation = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Orientation on', 'enable tools in panel'), ('off', 'Orientation off', 'disable tools in panel')), default='on', update = update_display_tools)


    tab_history_align = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)

    #Snap
    
    tab_snap = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Snap on', 'enable tools in panel'), ('off', 'Snap off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_snapset = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'SnapSet on', 'enable tools in menu'), ('off', 'SnapSet off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_propedit = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'PropEdit on', 'enable tools in panel'), ('off', 'PropEdit off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_view = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'View on', 'enable tools in panel'), ('off', 'View off', 'disable tools in panel')), default='on', update = update_display_tools)

    #Relax

    tab_history_relax = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)

    #Menu
    
    tab_normals_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Normals on', 'enable tools in panel'), ('off', 'Normals off', 'disable tools in panel')), default='on', update = update_display_tools)
    
    tab_history_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)


    tools_category_align = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_align)
    tools_category_snap = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_snap)
    tools_category_relax = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_relax)

    tools_category_menu = bpy.props.BoolProperty(name = "Align Menu", description = "enable or disable menu", default=True, update = update_menu)

    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':

            box = layout.box().column(1)
            
            row = box.column(1)   
            row.label(text="Welcome to custom Align, Snap & Relax addon!")  
            row.label(text="There are three ways to execute the tools:")   
            row.label(text="> use the panel function or the included menu")   
            row.label(text="> or add new shortcuts directly to the tools (rightclick)")       
            row.label(text="> to have them permant: save user settings in the user preferences")                      
            row.label(text="Have Fun! :)")  


        #Tools
        if self.prefs_tabs == 'toolsets':
          
            box = layout.box().column(1)

            row = box.row()
            row.label("Panel: Align")            
            
            row = box.row()
            row.prop(self, 'tab_normals', expand=True)
            row.prop(self, 'tab_orientation', expand=True)
            row.prop(self, 'tab_history_align', expand=True)
            
            box.separator()

            row = box.row()
            row.label("Panel: Snap")
            
            row = box.row()
            row.prop(self, 'tab_snap', expand=True)
            row.prop(self, 'tab_snapset', expand=True)
            row.prop(self, 'tab_propedit', expand=True)
            row.prop(self, 'tab_view', expand=True)
            
            box.separator()

            row = box.row()
            row.label("Panel: Relax")
            
            row = box.row()
            row.prop(self, 'tab_history_relax', expand=True)           
            
            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 


        #Locations
        if self.prefs_tabs == 'location':
            box = layout.box().column(1) 
            
            row = box.row(1) 
            row.label("Location Align: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_align', expand=True)
            
            if self.tab_location_align == 'tools':

                box.separator()

                row = box.row(1) 
                row.prop(self, "tools_category_align")

            box.separator()
        
            box = layout.box().column(1) 

            row = box.row(1) 
            row.label("Location Snap: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_snap', expand=True)

            if self.tab_location_snap == 'tools':
 
                box.separator()

                row = box.row(1) 
                row.prop(self, "tools_category_snap")

            box.separator()
        
            box = layout.box().column(1) 

            row = box.row(1) 
            row.label("Location Relax: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_relax', expand=True)

            if self.tab_location_relax == 'tools':
 
                box.separator()

                row = box.row(1) 
                row.prop(self, "tools_category_relax")

            box.separator()
            
            box = layout.box().column(1) 

            row = box.row(1)            
            row.label(text="...please reboot blender after changing the locations...", icon ="INFO")
            
            box.separator()


        #Keymap
        if self.prefs_tabs == 'keymap':

            box = layout.box().column(1)
             
            row = box.column(1)  
            row.label("Align Menu:", icon ="COLLAPSEMENU") 
            
            row.separator()           
            row.label("Menu: 'ONE', 'PRESS', alt=True")

            row = box.row(1)          
            row.prop(self, 'tab_menu_view', expand=True)
            
            if self.tab_menu_view == 'off':
                
                box.separator() 
                
                row = box.row(1) 
                row.label(text="! menu hidden with next reboot durably!", icon ="INFO")

            box.separator() 
             
            row.operator('wm.url_open', text = 'recommended: is key free addon', icon = 'PLUGIN').url = "https://github.com/Antonioya/blender/tree/master/iskeyfree"

            box.separator() 
        
            row = box.row()  
            row.prop(self, 'tab_normals_menu', expand=True)
            row.prop(self, 'tab_history_menu', expand=True)

            box.separator() 
            
            row = layout.row(1) 
            row.label(text="! if needed change keys durably in TAB Input !", icon ="INFO")


        #Weblinks
        if self.prefs_tabs == 'url':
            row = layout.column_flow(2)
            row.operator('wm.url_open', text = '1D_Scripts', icon = 'INFO').url = "https://blenderartists.org/forum/showthread.php?399882-1D_Scripts-Bargool_1D_tools-main-thread&highlight="
            row.operator('wm.url_open', text = 'Advanced Align Tools', icon = 'INFO').url = "https://blenderartists.org/forum/showthread.php?256114-Add-on-Advanced-align-tools"
            row.operator('wm.url_open', text = 'Rotate Constraine', icon = 'INFO').url = "http://blendscript.blogspot.de/2013/05/rotate-constraint-script.html?showComment=1367746477883#c794165451806396278"
            row.operator('wm.url_open', text = 'Distribute Objects', icon = 'INFO').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Oscurart_Tools"
            row.operator('wm.url_open', text = 'Align by Faces', icon = 'INFO').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Align_by_faces"
            row.operator('wm.url_open', text = 'Look at it', icon = 'INFO').url = "http://stonefield.cocolog-nifty.com/higurashi/2013/12/blenderaddonloo.html"
            row.operator('wm.url_open', text = 'LoopTools', icon = 'INFO').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/LoopTools"
            row.operator('wm.url_open', text = 'Kjartans Scripts', icon = 'INFO').url = "http://www.kjartantysdal.com/scripts"
            row.operator('wm.url_open', text = 'Simple Align', icon = 'INFO').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D%20interaction/Align_Tools"
            row.operator('wm.url_open', text = 'Vertex Tools', icon = 'INFO').url = "http://airplanes3d.net/scripts-254_e.xml"
            row.operator('wm.url_open', text = 'Drop to Ground', icon = 'INFO').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Drop_to_ground"
            row.operator('wm.url_open', text = 'THREAD', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?409510-Addon-T-Align&p=3114519#post3114519"



class Dropdown_TP_Align_Props(bpy.types.PropertyGroup):

    ### Transform
    display_align_help = bpy.props.BoolProperty(name = "Help ", description = "open/close help", default = False) 



# register
import traceback

icon_collections = {}

def register():

    mkb_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mkb_icons.load("my_image1", os.path.join(icons_dir, "icon_image1.png"), 'IMAGE')
    mkb_icons.load("my_image2", os.path.join(icons_dir, "icon_image2.png"), 'IMAGE')
    ###etc...

    icon_collections['main'] = mkb_icons
    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
        
    update_panel_position_align(None, bpy.context)
    update_panel_position_snap(None, bpy.context)
    update_panel_position_relax(None, bpy.context)

    update_menu(None, bpy.context)
    #update_display_tools(None, bpy.context)

    #align
    bpy.types.WindowManager.tp_collapse_menu_align = bpy.props.PointerProperty(type = Dropdown_TP_Align_Props)

    #LoopTools
    bpy.types.WindowManager.looptools = bpy.props.PointerProperty(type = LoopToolsProps)    

    #1d_scripts
    bpy.types.WindowManager.paul_manager = bpy.props.PointerProperty(type = paul_managerProps) 
    bpy.context.window_manager.paul_manager.display_align = False
    bpy.context.window_manager.paul_manager.align_dist_z = True
    bpy.context.window_manager.paul_manager.align_lock_z = False
    bpy.context.window_manager.paul_manager.step_len = 1.0
    bpy.context.window_manager.paul_manager.edge_idx_store = -1
    bpy.context.window_manager.paul_manager.object_name_store = ''
    bpy.context.window_manager.paul_manager.object_name_store_c = ''
    bpy.context.window_manager.paul_manager.object_name_store_v = ''
    bpy.context.window_manager.paul_manager.active_edge1_store = -1
    bpy.context.window_manager.paul_manager.active_edge2_store = -1
    bpy.context.window_manager.paul_manager.coner_edge1_store = -1
    bpy.context.window_manager.paul_manager.coner_edge2_store = -1

    ###
    bpy.types.WindowManager.looptools = bpy.props.PointerProperty(type = LoopToolsProps)



def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    #LoopTools
    del bpy.types.WindowManager.looptools
    
    #1d_scripts
    del bpy.types.WindowManager.paul_manager

    #align
    del bpy.types.WindowManager.tp_collapse_menu_align


    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    

if __name__ == "__main__":
    register()
        
        




