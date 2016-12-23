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
    "name": "TP Modifier",
    "author": "MKB",
    "version": (0, 1, 2),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N]",
    "description": "Modifier Tools Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}


from toolplus_modifier.mods_menu           import (VIEW3D_TP_Modifier_Menu)
from toolplus_modifier.mods_stack_ui       import (VIEW3D_TP_Modifier_Stack_Panel_UI)
from toolplus_modifier.mods_stack_tools    import (VIEW3D_TP_Modifier_Stack_Panel_TOOLS)

##################################

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_modifier'))

if "bpy" in locals():
    import imp
    imp.reload(mods_action)
    imp.reload(mods_automirror)
    imp.reload(mods_batch)
    imp.reload(mods_batch_atm)
    imp.reload(mods_display)
    imp.reload(mods_normals)
    imp.reload(mods_pivot)
    imp.reload(mods_remove)
    imp.reload(mods_show)
    imp.reload(mods_toall)
    imp.reload(mods_tools)


else:
    from . import mods_action         
    from . import mods_automirror                
    from . import mods_batch                       
    from . import mods_batch_atm                       
    from . import mods_display                       
    from . import mods_normals         
    from . import mods_pivot                   
    from . import mods_remove               
    from . import mods_show               
    from . import mods_toall               
    from . import mods_tools               



import bpy
from bpy import*

import bpy.utils.previews
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)


def update_panel_position(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Panel_UI)
       
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Panel_TOOLS)
   
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':
        
        VIEW3D_TP_Modifier_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        
        bpy.utils.register_class(VIEW3D_TP_Modifier_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Modifier_Panel_UI)
  

    if context.user_preferences.addons[__name__].preferences.tab_location == 'off':
        pass



def update_panel_position_stack(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Stack_Panel_UI)
       
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Stack_Panel_TOOLS)
   
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Stack_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_stack == 'tools':
        
        VIEW3D_TP_Modifier_Stack_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_stack
        
        bpy.utils.register_class(VIEW3D_TP_Modifier_Stack_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_stack == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Modifier_Stack_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_stack == 'off':
        pass




def update_display_tools(self, context):

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'on':
        return True

    else:        
        if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'off':
            return False 



addon_keymaps_menu = []

def update_menu(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Modifier_Menu)
        
        # Keymapping
        # remove keymaps when add-on is deactivated
        wm = bpy.context.window_manager
        for km in addon_keymaps_menu:
            wm.keyconfigs.addon.keymaps.remove(km)
        del addon_keymaps_menu[:]
        
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'menu':
     
        VIEW3D_TP_Modifier_Menu.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_menu
    
        bpy.utils.register_class(VIEW3D_TP_Modifier_Menu)
    
        # Keymapping 
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=True) #,shift=True, alt=True, 
        kmi.properties.name = 'VIEW3D_TP_Modifier_Menu'

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

    tab_location = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'on or off for panel in the shelfs')),
               default='tools', update = update_panel_position)

    tab_location_stack = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'on or off for panel in the shelfs')),
               default='tools', update = update_panel_position_stack)

    tab_menu_view = EnumProperty(
        name = '3d View Menu',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('menu', 'Menu on', 'enable menu for 3d view'),
               ('off', 'Menu off', 'enable or disable menu for 3d view')),
               default='menu', update = update_menu)

    # Panel
    tab_display_tools = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Display Tools on', 'enable tools in panel'), ('off', 'Display Tools off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_automirror = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'AutoMirror on', 'enable tools in panel'), ('off', 'AutoMirror off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_mirror_cut = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'MirrorCut on', 'enable tools in panel'), ('off', 'MirrorCut off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_mirror = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Mirror on', 'enable tools in panel'), ('off', 'Mirror off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_bevel = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Bevel on', 'enable tools in panel'), ('off', 'Bevel off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_subsurf = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Subsurf on', 'enable tools in panel'), ('off', 'Subsurf off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_solidify = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Solidify on', 'enable tools in panel'), ('off', 'Solidify off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_simple = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'SDeform on', 'enable tools in panel'), ('off', 'SDeform off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_array = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Array on', 'enable tools in panel'), ('off', 'Array off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_transform = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Transform on', 'enable tools in panel'), ('off', 'Transform off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_shade = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Shade on', 'enable tools in panel'), ('off', 'Shade off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_remove_type = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Remove Type on', 'enable tools in panel'), ('off', 'Remove Type off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)

    # Menu
    tab_tp_menus = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Menus on', 'enable tools in menu'), ('off', 'Menus off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_tp_menus = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Menus on', 'enable tools in menu'), ('off', 'Menus off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_automirror_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'AutoMirror on', 'enable tools in menu'), ('off', 'AutoMirror off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_modstack_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'ModifierStack on', 'enable tools in menu'), ('off', 'ModifierStack off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_clear_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'ClearTools on', 'enable tools in menu'), ('off', 'ClearTools off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_hover_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'HoverTools on', 'enable tools in menu'), ('off', 'HoverTools off', 'disable tools in menu')), default='on', update = update_display_tools)


    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position)
    tools_category_stack = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_stack)

    tools_category_menu = bpy.props.BoolProperty(name = "Modifier Menu", description = "enable or disable menu", default=True, update = update_menu)


    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            
            box = layout.box().column(1)
            
            row = box.column(1)   
            row.label(text="Welcome to Modifier!")  
            row.label(text="This custom addon is for editing.")
            row.label(text="There are two ways to execute the tools:")   
            row.label(text="> use the functions in the panel")      
            row.label(text="> or the included menu")      
            row.label(text="Have Fun! :)")         


        #Tools
        if self.prefs_tabs == 'toolsets':
          
            box = layout.box().column(1)

            row = box.column_flow(4)
            row.prop(self, 'tab_subsurf', expand=True)
            row.prop(self, 'tab_automirror', expand=True)
            row.prop(self, 'tab_mirror_cut', expand=True)
            row.prop(self, 'tab_mirror', expand=True)
            row.prop(self, 'tab_bevel', expand=True)
            row.prop(self, 'tab_solidify', expand=True)
            row.prop(self, 'tab_simple', expand=True)
            row.prop(self, 'tab_array', expand=True)
            row.prop(self, 'tab_transform', expand=True)
            row.prop(self, 'tab_shade', expand=True)
            row.prop(self, 'tab_remove_type', expand=True)
            row.prop(self, 'tab_history', expand=True)

            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 
            

        #Location
        if self.prefs_tabs == 'location':
            
            box = layout.box().column(1)
             
            row = box.row(1) 
            row.label("Location Modifier Sets:")
            
            row = box.row(1)
            row.prop(self, 'tab_location', expand=True)
            
            box.separator()

            row = box.row(1)            
            if self.tab_location == 'tools':
                
                box.separator() 
                
                row.prop(self, "tools_category")

            box.separator()
            
            row = box.row(1) 
            row.label("Location Modifier Stack:")            
         
            row = box.row(1)             
            row.prop(self, 'tab_location_stack', expand=True)
          
            box.separator() 
        
            row = box.row(1)            
            if self.tab_location_stack == 'tools':
                
                box.separator() 
                
                row.prop(self, "tools_category_stack")
                
            row = layout.row()
            row.label(text="! please reboot blender after changing the panel location !", icon ="INFO")

            box.separator() 


        #Keymap
        if self.prefs_tabs == 'keymap':

            box = layout.box().column(1)
             
            row = box.column(1)  
            row.label("Modifier Menu:", icon ="COLLAPSEMENU") 
            
            row.separator()           
            row.label("Menu: 'D', 'PRESS', ctrl=True")

            row = box.row(1)          
            row.prop(self, 'tab_menu_view', expand=True)
            
            if self.tab_menu_view == 'off':
                
                box.separator() 
                
                row = box.row(1) 
                row.label(text="! menu hidden with next reboot durably!", icon ="INFO")

            box.separator() 
             
            row.operator('wm.url_open', text = 'recommended: is key free addon', icon = 'PLUGIN').url = "https://github.com/Antonioya/blender/tree/master/iskeyfree"

            box.separator() 
            
            row = box.row(1) 
            row.label(text="! if needed change keys durably in TAB Input !", icon ="INFO")

          
            box = layout.box().column(1)

            row = box.column_flow(3)
            row.prop(self, 'tab_tp_menus', expand=True)
            row.prop(self, 'tab_automirror_menu', expand=True)
            row.prop(self, 'tab_modstack_menu', expand=True)
            row.prop(self, 'tab_clear_menu', expand=True)
            row.prop(self, 'tab_hover_menu', expand=True)

            row = box.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 


        #Weblinks
        if self.prefs_tabs == 'url':
            
            box = layout.box().column(1)
            
            row = box.column_flow(2)
            row.operator('wm.url_open', text = 'AutoMirror', icon = 'HELP').url = "http://le-terrier-de-lapineige.over-blog.com/2014/07/automirror-mon-add-on-pour-symetriser-vos-objets-rapidement.html"
            row.operator('wm.url_open', text = 'Copy To All', icon = 'HELP').url = "https://www.artunchained.de/tiny-new-addon-to-all/"
            row.operator('wm.url_open', text = 'Display Tools', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Display_Tools"
            row.operator('wm.url_open', text = 'Modifier Tools', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/modifier_tools"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?411265-Addon-T-Modifier&p=3124733#post3124733"



class Dropdown_TP_Modifier_Props(bpy.types.PropertyGroup):


    display_subsurf = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_automirror = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=False)    
    display_mirror = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_bevel = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_solidify = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_sdeform = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_array = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    
    display_apply = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=False)    
    display_display = bpy.props.BoolProperty(name="Open / Close", description="Open / Close", default=True)    



def draw_modifier_panel_layout(self, context, layout):
    
        tp_props = context.window_manager.tp_collapse_menu_modifier
  
        ob = context.object  
        obj = context.object
        scene = context.scene
        scn = context.scene
        rs = bpy.context.scene 

        obj = context.active_object     
        if obj:
           obj_type = obj.type
                          
           if obj_type in {'MESH'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("MESH") 
                                  
           if obj_type in {'LATTICE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("LATTICE") 

           if obj_type in {'CURVE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("CURVE")               
               
           if obj_type in {'SURFACE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("SURFACE")                 
               
           if obj_type in {'META'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("MBall")                 
               
           if obj_type in {'FONT'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("FONT")  
                                              
           if obj_type in {'ARMATURE'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("ARMATURE") 

           if obj_type in {'EMPTY'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("EMPTY") 

           if obj_type in {'CAMERA'}:
              box = layout.box()
              row = box.row(1)                                        
              row.alignment = "CENTER"
              row.label("CAMERA") 

           if obj_type in {'LAMP'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("LAMP") 

           if obj_type in {'SPEAKER'}:
               box = layout.box()
               row = box.row(1)                                        
               row.alignment = "CENTER"
               row.label("SPEAKER") 


        box = layout.box()
        
        row = box.row(1)  
        sub = row.row(1)
        sub.scale_x = 7

        sub.operator("tp_ops.pivot_bounding_box", "", icon="ROTATE")
        sub.operator("tp_ops.pivot_3d_cursor", "", icon="CURSOR")
        sub.operator("tp_ops.pivot_active", "", icon="ROTACTIVE")
        sub.operator("tp_ops.pivot_individual", "", icon="ROTATECOLLECTION")
        sub.operator("tp_ops.pivot_median", "", icon="ROTATECENTER")          
        #row.menu("tp_ops.delete_menu", "", icon="PANEL_CLOSE")   
        
        box = layout.box().column(1)  
            
        row = box.row(1) 
        row.operator_menu_enum("object.modifier_add", "type","   Add new Modifier", icon="MODIFIER")     

        mod_list = context.active_object.modifiers
        if mod_list:
            
            row = box.row(1) 
            row.operator("tp_ops.mods_render"," ", icon = 'RESTRICT_RENDER_OFF') 
            row.operator("tp_ops.mods_view"," ", icon = 'RESTRICT_VIEW_OFF')                                                                       
            row.operator("tp_ops.mods_edit"," ", icon='EDITMODE_HLT')                                                    
            row.operator("tp_ops.mods_cage"," ", icon='OUTLINER_OB_MESH')                  
            row.operator("tp_ops.remove_mod", text=" ", icon='X') 
            row.operator("tp_ops.apply_mod", text=" ", icon='FILE_TICK')          

        else:
            pass


        box.separator()
        
        Display_Subsurf = context.user_preferences.addons[__package__].preferences.tab_subsurf
        if Display_Subsurf == 'on':

            box = layout.box().column(1)
            
            row = box.row(1)
            if tp_props.display_subsurf:            
                row.prop(tp_props, "display_subsurf", text="", icon="MOD_SUBSURF")
            else:
                row.prop(tp_props, "display_subsurf", text="", icon="MOD_SUBSURF")
                
            row.label("SubSurf")

            box.separator()  
            
            row = box.row(1)
            row.scale_x = 0.6             
            row.operator("tp_ops.subsurf_0")
            row.operator("tp_ops.subsurf_1")
            row.operator("tp_ops.subsurf_2")            
            row.operator("tp_ops.subsurf_3")
            row.operator("tp_ops.subsurf_4")
            row.operator("tp_ops.subsurf_5")
            #row.operator("tp_ops.subsurf_6")
            
            box.separator() 
            
            if tp_props.display_subsurf: 
            
                mo_types = []
                append = mo_types.append

                for mo in context.active_object.modifiers:
                    if mo.type == 'SUBSURF':
                        append(mo.type)

                        #box.label(mo.name)

                        row = box.row(1)
                        row.prop(mo, "use_subsurf_uv",text="UVs")
                        row.prop(mo, "show_only_control_edges",text="Optimal")                    
                        #row.prop(mo, "use_opensubdiv",text="OPSubdiv")                    
                        #row.prop(system, "opensubdiv_compute_type", text="")

                        box.separator() 



        Display_AutoMirror = context.user_preferences.addons[__package__].preferences.tab_automirror
        if Display_AutoMirror == 'on':

            obj = context.object
            if obj:
                if obj.type in {'MESH'}:
                    
                    box = layout.box().column(1)
                    
                    row = box.row(1)
                    if tp_props.display_automirror:            
                        row.prop(tp_props, "display_automirror", text="", icon="MOD_WIREFRAME")
                    else:
                        row.prop(tp_props, "display_automirror", text="", icon="MOD_WIREFRAME")
   
                    row.label("AutoMirror")

                    box.separator() 
                    
                    row = box.row()
                    row.prop(context.scene, "AutoMirror_orientation", text="")                                     
                    row.prop(context.scene, "AutoMirror_axis", text="")  
                
                    box.separator()                  
                 
                    row = box.row()
                    row.prop(context.scene, "AutoMirror_threshold", text="Threshold") 
                    row.operator("object.automirror", text="Execute") 

                    box.separator() 

                    if tp_props.display_automirror: 
                                          
                        box = layout.box().column(1) 
                        row = box.row(1)
                        row.prop(context.scene, "AutoMirror_toggle_edit", text="Editmode")
                        row.prop(context.scene, "AutoMirror_cut", text="Cut+Mirror")
                        
                        row = box.row(1)
                        row.prop(context.scene, "AutoMirror_use_clip", text="Use Clip")
                        row.prop(context.scene, "AutoMirror_show_on_cage", text="Editable")            

                        box.separator() 

                   
                    Display_Mirror_Cut = context.user_preferences.addons[__package__].preferences.tab_mirror_cut
                    if Display_Mirror_Cut == 'on':

                        box = layout.box().column(1)
                        
                        row = box.row(1)
                        row.label("", icon="MOD_MESHDEFORM")            
                        row.label("AutoCuts")   
                        
                        row = box.row(1)  
                        row.prop(context.scene, "tp_axis", text="")
                        sub = row.row(1)
                        sub.scale_x = 0.5
                        sub.prop(context.scene, "tp_axis_cut", text="")
                        row.operator("tp_ops.mods_autocut", text="Execute")                           
                       
                        box.separator() 
                        
            else:
                box = layout.box().column(1)
                
                row = box.row(1)                   
                row.label("nothing selected", icon ="INFO")                   
     
        
        Display_Mirror = context.user_preferences.addons[__package__].preferences.tab_mirror
        if Display_Mirror == 'on':
        
            box = layout.box().column(1)
            
            row = box.row(1)
            if tp_props.display_mirror:            
                row.prop(tp_props, "display_mirror", text="", icon="MOD_MIRROR")
            else:
                row.prop(tp_props, "display_mirror", text="", icon="MOD_MIRROR")
          
            row.label("Mirror")                   
           
            sub = row.row(1)
            sub.scale_x = 0.3  
            sub.operator("tp_ops.mod_mirror_x", "Add")
            
            box.separator()              
            
            if tp_props.display_mirror:             
            
                mo_types = []
                append = mo_types.append

                for mo in context.active_object.modifiers:
                                                  
                    if mo.type == 'MIRROR':
                        append(mo.type)

                        #box.label(mo.name)

                        row = box.row(1)
                        row.prop(mo, "use_x")
                        row.prop(mo, "use_y")
                        row.prop(mo, "use_z")
                        
                        row = box.row(1)
                        row.prop(mo, "use_mirror_merge", text="Merge")
                        row.prop(mo, "use_clip", text="Clipping")
         
                        box.separator() 

        
        Display_Bevel = context.user_preferences.addons[__package__].preferences.tab_bevel
        if Display_Bevel == 'on':
        
            if context.active_object.type in {'MESH'}:
                
                box = layout.box().column(1)
                
                row = box.row(1)
                if tp_props.display_bevel:            
                    row.prop(tp_props, "display_bevel", text="", icon="MOD_BEVEL")
                else:
                    row.prop(tp_props, "display_bevel", text="", icon="MOD_BEVEL")
                    
                row.label("Bevel")
              
                sub = row.row(1)
                sub.scale_x = 0.3   
                sub.operator("tp_ops.mods_bevel", text="Add")
                
                box.separator()  
                
                if tp_props.display_bevel: 
                                              
                    mo_types = []
                    append = mo_types.append

                    for mo in context.active_object.modifiers:
                                    
                        if mo.type == 'BEVEL':
                            
                            append(mo.type)
                            
                            row = box.row(1)  
                            row.prop(mo, "profile", text="")
                            row.prop(mo, "segments", text="")
                            row.prop(mo, "width", text="")

                            row = box.row(1)  
                            row.label(text="profile")                       
                            row.label(text="segments")
                            row.label(text="width")
            
                            box.separator() 


        Display_Solidify = context.user_preferences.addons[__package__].preferences.tab_solidify
        if Display_Solidify == 'on':
        
            if context.active_object.type in {'MESH'}:
                
                box = layout.box().column(1)
                                
                row = box.row(1)
                if tp_props.display_solidify:            
                    row.prop(tp_props, "display_solidify", text="", icon="MOD_SOLIDIFY")
                else:
                    row.prop(tp_props, "display_solidify", text="", icon="MOD_SOLIDIFY")
                               
                row.label("Solidify")
                
                sub = row.row(1)
                sub.scale_x = 0.3                                       
                sub.operator("tp_ops.mods_solidify", text="Add") 
                
                box.separator()  
                
                if tp_props.display_solidify:  
                                              
                    mo_types = []
                    append = mo_types.append

                    for mo in context.active_object.modifiers:
                                    
                        if mo.type == 'SOLIDIFY':
                            
                            append(mo.type)
                            
                            row = box.column(1)  
                            row.prop(mo, "thickness")
                            row.prop(mo, "thickness_clamp")        
                            row.prop(mo, "offset")
                            
                            row = box.row(1)
                            row.prop(mo, "use_rim", text ="Fill")
                            row.prop(mo, "use_rim_only", text ="Rim")    
                            row.prop(mo, "use_even_offset", text ="Even")
            
                            box.separator() 



        Display_Simple = context.user_preferences.addons[__package__].preferences.tab_simple
        if Display_Simple == 'on':
        
            if context.active_object.type in {'MESH'}:
                
                box = layout.box().column(1)
                
                row = box.row(1)
                if tp_props.display_sdeform:            
                    row.prop(tp_props, "display_sdeform", text="", icon="MOD_SIMPLEDEFORM")
                else:
                    row.prop(tp_props, "display_sdeform", text="", icon="MOD_SIMPLEDEFORM")
                                         
                row.label("SDeform")

                sub = row.row(1)
                sub.scale_x = 0.3                                   
                sub.operator("object.modifier_add", text="Add").type='SIMPLE_DEFORM'          
                
                box.separator()  

                if tp_props.display_sdeform:    
                           
                    mo_types = []
                    append = mo_types.append

                    for mo in context.active_object.modifiers:
                                    
                        if mo.type == 'SIMPLE_DEFORM':
                            
                            append(mo.type)
                            
                            row = box.row(1)  
                            row.prop(mo, "deform_method", expand=True)
                            
                            box.separator() 
                          
                            row = box.row(1)  
                            row.prop_search(mo, "vertex_group", ob, "vertex_groups", text="VGrp")
                            row.prop(mo, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

                            row = box.row(1)  
                            row.prop(mo, "origin", text="Axis")
                            row.label(text="", icon ="BLANK1")

                            if mo.deform_method in {'TAPER', 'STRETCH', 'TWIST'}:
                                
                                row = box.row(1) 
                                row.prop(mo, "lock_x")
                                row.prop(mo, "lock_y")

                            box.separator() 
                            
                            row = box.row(1)                         
                            if mo.deform_method in {'TAPER', 'STRETCH'}:
                                row.scale_x = 3
                                row.prop(mo, "factor", text="Deform Factor:")
                            else:
                                row.prop(mo, "angle", text="Deform Angle:")
                            
                            box.separator() 
                            
                            row = box.row(1) 
                            row.prop(mo, "limits", slider=True, text="Limits")

                            box.separator() 
                        
                        
       
        Display_Array = context.user_preferences.addons[__name__].preferences.tab_array
        if Display_Array == 'on':     

            box = layout.box().column(1)
                            
            row = box.row(1)
            if tp_props.display_array:            
                row.prop(tp_props, "display_array", text="", icon="MOD_ARRAY")
            else:
                row.prop(tp_props, "display_array", text="", icon="MOD_ARRAY")
           
            row.label("Array")  

            sub = row.row(1)
            sub.scale_x = 0.3                 
            sub.operator("tp_ops.x_array",  text="X")
            sub.operator("tp_ops.y_array",  text="Y")
            sub.operator("tp_ops.z_array",  text="Z")
                                 
            box.separator() 
           
            if tp_props.display_array: 
          
                mo_types = []
                append = mo_types.append

                for mo in context.active_object.modifiers:
                    if mo.type == 'ARRAY':
                        if mo.fit_type == 'FIXED_COUNT':
                            append(mo.type)

                            split = box.split()

                            row = box.row(1)
                            row.label(mo.name)  
                            row.prop(mo, "count")
                            
                            box.separator() 
                            
                            row = box.row(1)  
                            row.prop(mo, "relative_offset_displace", text="")
                            
                            row = box.row(1) 
                            row.prop(mo, "start_cap", text="")
                            row.prop(mo, "end_cap", text="")  
                                                 
                            box.separator() 
                                           

        Display_Transform = context.user_preferences.addons[__package__].preferences.tab_transform
        if Display_Transform == 'on':
            
            if context.mode == 'OBJECT':  
                
                box = layout.box().column(1)
                
                row = box.row(1)
                if tp_props.display_apply:            
                    row.prop(tp_props, "display_apply", text="", icon="MANIPUL")
                else:
                    row.prop(tp_props, "display_apply", text="", icon="MANIPUL")
                             
                row.label("Apply")  

                sub = row.row(1)
                sub.scale_x = 0.3           
                sub.operator("object.transform_apply", text=" ", icon ="MAN_TRANS").location=True
                sub.operator("object.transform_apply", text=" ", icon ="MAN_ROT").rotation=True                
                sub.operator("object.transform_apply", text=" ", icon ="MAN_SCALE").scale=True                             
                
                if tp_props.display_apply: 
                   
                    box = layout.box().column(1)
                    
                    row = box.column_flow(2)
                    row.label("Transforms to Deltas")  
                    row.operator("object.transforms_to_deltas", text="Location").mode='LOC'
                    row.operator("object.transforms_to_deltas", text="Rotation").mode='ROT' 
                    row.operator("object.transforms_to_deltas", text="All").mode='ALL'
                    row.operator("object.transforms_to_deltas", text="Scale").mode='SCALE'                    
                    row.operator("object.anim_transforms_to_deltas", text="Animated")
                    
                    box.separator() 
                   
                    row = box.column(1)
                    row.operator("object.visual_transform_apply")
                    row.operator("object.duplicates_make_real")
                                                  
                box.separator()                     

        Display_Shade = context.user_preferences.addons[__name__].preferences.tab_shade
        if Display_Shade == 'on':                                         

            box = layout.box().column(1)
            
            row = box.row(1)
            if tp_props.display_display:            
                row.prop(tp_props, "display_display", text="", icon="WORLD")
            else:
                row.prop(tp_props, "display_display", text="", icon="WORLD")
                
            row.label("Display")
            
            if tp_props.display_display: 
            
                box.separator()
                
                row = box.row(1)                                                          
                row.operator("tp_ops.wire_all", text="Wire all", icon='WIRE')
                
                active_wire = bpy.context.object.show_wire 
                if active_wire == True:
                    row.operator("tp_ops.wire_off", "Wire Select", icon = 'MESH_PLANE')              
                else:                       
                    row.operator("tp_ops.wire_on", "Wire Select", icon = 'MESH_GRID')            
               
                row = box.row(1)
                if context.object.draw_type == 'WIRE':
                    row.operator("tp_ops.draw_solid", text="Solid Shade", icon='GHOST_DISABLED')     
                else:
                    row.operator("tp_ops.draw_wire", text="Wire Shade", icon='GHOST_ENABLED')        

                row.prop(context.object, "draw_type", text="")

                row = box.row(1)
                row.prop(context.object, "show_bounds", text="ShowBounds", icon='STICKY_UVS_LOC') 
                row.prop(context.object, "draw_bounds_type", text="")    
                
                if context.mode == 'EDIT_MESH':          
                    
                    box.separator() 
                    
                    row = box.row(1)  
                    row.operator("mesh.faces_shade_flat", text="Flat", icon="MESH_CIRCLE") 
                    row.operator("mesh.faces_shade_smooth", text="Smooth", icon="SMOOTH") 
                    
                    row = box.row(1)  
                    row.operator("mesh.normals_make_consistent", text="Consistent Normals", icon="SNAP_NORMAL")  
                
                else:            
                    
                    box.separator() 
                    
                    if context.mode == 'OBJECT': 
                        
                        row = box.row(1)  
                        row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")
                        row.operator("object.shade_smooth", text="Smooth", icon="SMOOTH")  
                   
                    row = box.row(1)  
                    row.operator("tp_ops.rec_normals", text="Consistent Normals", icon="SNAP_NORMAL")  

                box.separator() 


        
        mod_list = context.active_object.modifiers
        if mod_list:
                                
            if context.mode == 'OBJECT':
                box = layout.box().column(1)
                
                row = box.column(1)
                row.operator("scene.to_all", text="copy active to selected", icon='FRAME_NEXT').mode = "modifier, selected"
                row.operator("scene.to_all", text="copy active to children", icon='LINKED').mode = "modifier, children"        
               
                box.separator()               


                Display_RemoveType = context.user_preferences.addons[__package__].preferences.tab_remove_type
                if Display_RemoveType == 'on':

                    box = layout.box().column(1)
                    
                    row = box.row(1)
                    row.label("", icon="COLLAPSEMENU")            
                    row.label("Remove Type")   
                    
                    row = box.row(1)  
                    row.prop(context.scene, "tp_mods_type", text="")
                    row.operator("tp_ops.remove_mods_type", text="Execute")                           
                   
                    box.separator() 

        else:

            box = layout.box().column(1)    
 
            row = box.row(1)                    
           
            box.label('no modifier on active' , icon ="ERROR")
            
            box.separator()



        Display_History = context.user_preferences.addons[__name__].preferences.tab_history 
        if Display_History == 'on':
            
            box = layout.box().column(1)  

            row = box.row(1)        
            row.operator("view3d.ruler", text="Ruler")   
             
            row.operator("ed.undo_history", text="History")
            row.operator("ed.undo", text="", icon="LOOP_BACK")
            row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
            box.separator()   




class VIEW3D_TP_Modifier_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Origin"
    bl_idname = "VIEW3D_TP_Modifier_Panel_TOOLS"
    bl_label = "Modifier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (isModelingMode)

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_modifier_panel_layout(self, context, layout) 



class VIEW3D_TP_Modifier_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Modifier_Panel_UI"
    bl_label = "Modifier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (isModelingMode)

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'  

        draw_modifier_panel_layout(self, context, layout) 




# register

import traceback

icon_collections = {}

def register():

    mkb_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mkb_icons.load("my_image1", os.path.join(icons_dir, "icon_image1.png"), 'IMAGE')
    mkb_icons.load("my_image2", os.path.join(icons_dir, "icon_image2.png"), 'IMAGE')

    icon_collections['main'] = mkb_icons
    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    bpy.types.WindowManager.tp_collapse_menu_modifier = bpy.props.PointerProperty(type = Dropdown_TP_Modifier_Props)

        
    update_menu(None, bpy.context)
    update_panel_position(None, bpy.context)
    update_panel_position_stack(None, bpy.context)


def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    
    del bpy.types.WindowManager.tp_collapse_menu_modifier
    
if __name__ == "__main__":
    register()
        
        




              
