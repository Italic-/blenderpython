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
    "name": "TP CopyShop",
    "author": "MKB",
    "version": (0, 1, 2),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N]",
    "description": "Copy Tools Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}


from toolplus_copyshop.copy_menu            import (View3D_TP_Copy_Menu)
from toolplus_copyshop.copy_mifthcloning    import (MFTProperties)

##################################

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_copyshop'))

if "bpy" in locals():
    import imp
    imp.reload(copy_action)
    imp.reload(copy_attributes)
    imp.reload(copy_copy_to_face)
    imp.reload(copy_mifthcloning)
    imp.reload(copy_pivot)
    imp.reload(copy_replicator)
    imp.reload(copy_toall)
    imp.reload(copy_fpath)
    imp.reload(copy_display)

else:
    from . import copy_action         
    from . import copy_attributes         
    from . import copy_copy_to_face                   
    from . import copy_mifthcloning          
    from . import copy_pivot       
    from . import copy_replicator     
    from . import copy_toall       
    from . import copy_fpath       
    from . import copy_display       
    

##################################


import bpy, re
from bpy import *
import bpy.utils.previews

from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)


def update_panel_position(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Copy_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Copy_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Copy_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':
        VIEW3D_TP_Copy_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        bpy.utils.register_class(VIEW3D_TP_Copy_Panel_TOOLS)
    
    else:
        bpy.utils.register_class(VIEW3D_TP_Copy_Panel_UI)
  

def update_display_tools(self, context):

    try:
        return True
    except:
        pass

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'on':
        return True

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'off':
        pass 



addon_keymaps_menu = []

def update_menu(self, context):
    try:
        bpy.utils.unregister_class(View3D_TP_Copy_Menu)
        
        # Keymapping
        # remove keymaps when add-on is deactivated
        wm = bpy.context.window_manager
        for km in addon_keymaps_menu:
            wm.keyconfigs.addon.keymaps.remove(km)
        del addon_keymaps_menu[:]
        
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'menu':
     
        View3D_TP_Copy_Menu.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_menu
    
        bpy.utils.register_class(View3D_TP_Copy_Menu)
    
        # booltool: create the booleanhotkey in opjectmode
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', shift=True, alt=True) #,ctrl=True 
        kmi.properties.name = 'tp_menu.copyshop_menu'

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
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]')),
               default='tools', update = update_panel_position)

    tab_menu_view = EnumProperty(
        name = '3d View Menu',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('menu', 'Menu on', 'enable menu for 3d view'),
               ('off', 'Menu off', 'enable or disable menu for 3d view')),
               default='menu', update = update_menu)


    tab_dynamics = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Dymanic on', 'enable tools in panel'), ('off', 'Dymanic off', 'disable tools in panel')), default='off', update = update_display_tools)

    tab_array = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Array on', 'enable tools in panel'), ('off', 'Array off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_dupli = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Dupli on', 'enable tools in panel'), ('off', 'Dupli off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_linked = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Optimize on', 'enable tools in panel'), ('off', 'Optimize off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)


    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position)

    tools_category_menu = bpy.props.BoolProperty(name = "CopyShop Menu", description = "enable or disable menu", default=True, update = update_menu)


    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            box = layout.box().column(1)
             
            row = box.column(1)   
            row.label(text="Welcome to CopyShop!")  
            row.label(text="This custom addon set is for object duplication")   
            row.label(text="There are three ways to execute the tools:")   
            row.label(text="> use the panel function or the included menu")   
            row.label(text="> or use the dynamic tools in your own custom pie menu")   
            row.label(text="Have Fun! :)")   
       

        #Tools
        if self.prefs_tabs == 'toolsets':
          
            box = layout.box().column(1)

            row = box.row()
            row.prop(self, 'tab_dynamics', expand=True)
            row.prop(self, 'tab_array', expand=True)
            row.prop(self, 'tab_dupli', expand=True)
            
            box.separator() 
            
            row = box.row()
            row.prop(self, 'tab_linked', expand=True)
            row.prop(self, 'tab_history', expand=True)

            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 


        #Location
        if self.prefs_tabs == 'location':
            
            box = layout.box().column(1)
             
            row = box.row(1) 
            row.label("Location CopyShop:")
            
            row = box.row(1)
            row.prop(self, 'tab_location', expand=True)
          
            box.separator() 
        
            row = box.row(1)            
            if self.tab_location == 'tools':
                
                box.separator() 
                
                row.prop(self, "tools_category")

            row = layout.row()
            row.label(text="! please reboot blender after changing the panel location !", icon ="INFO")

            box.separator() 
            
        #Keymap
        if self.prefs_tabs == 'keymap':

            box = layout.box().column(1)
             
            row = box.column(1)  
            row.label("CopsShop Menu:", icon ="COLLAPSEMENU") 
            
            row.separator()           
            row.label("Menu: 'Q', 'PRESS', alt=True, shift=True")

            row = box.row(1)          
            row.prop(self, 'tab_menu_view', expand=True)
            
            if self.tab_menu_view == 'off':
                
                box.separator() 
                
                row = box.row(1) 
                row.label(text="! menu hidden with next reboot durably!", icon ="INFO")

            box.separator() 
             
            row.operator('wm.url_open', text = 'recommended: is key free addon', icon = 'PLUGIN').url = "https://github.com/Antonioya/blender/tree/master/iskeyfree"


            box.separator() 
            
            row = layout.row(1) 
            row.label(text="! if needed change keys durably in TAB Input !", icon ="INFO")


        #Weblinks
        if self.prefs_tabs == 'url':
            
            box = layout.box().column(1)
             
            row = box.column_flow(2) 
            row.operator('wm.url_open', text = 'MifthTools', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?346588-MifthTools-Addon"
            row.operator('wm.url_open', text = 'ARewO', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Animation/ARewO"
            row.operator('wm.url_open', text = 'To All', icon = 'HELP').url = "https://www.artunchained.de/tiny-new-addon-to-all/"
            row.operator('wm.url_open', text = 'Follow Path', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?325179-Follow-Path-Array"
            row.operator('wm.url_open', text = 'Copy Attributes', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Copy_Attributes_Menu"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?409893-Addon-T-CopyShop&p=3116714#post3116714"



# property group containing all properties for the gui in the panel
class Dropdown_TP_CopyShop_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    tp_props = context.window_manager.tp_collapse_copyshop_props
    """

    display_copy_to_faces = bpy.props.BoolProperty(name = "Copy to Faces Tools", description = "open / close props", default = False)
    display_toall = bpy.props.BoolProperty(name = "Copy to All", description = "open / close props", default = False)
    display_pfath = bpy.props.BoolProperty(name = "Follow Path Array", description = "open / close props", default = False)
    display_empty = bpy.props.BoolProperty(name = "Empty Array", description = "open / close props", default = False)
    display_array = bpy.props.BoolProperty(name = "Curve Array", description = "open / close props", default = False)
    display_axis_array = bpy.props.BoolProperty(name = "Axis Array", description = "open / close props", default = False)
    display_array_tools = bpy.props.BoolProperty(name = "Array Tools", description = "open / close props", default = False)


def draw_copy_panel_layout(self, context, layout):
        
        tp_props = context.window_manager.tp_collapse_copyshop_props
        
        icons = icon_collections["main"]
  
        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)  
         
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


        if context.mode == 'OBJECT':

            box = layout.box().column(1)
             
            row = box.column(1)
            row.operator("object.duplicate_move", text="Duplicate", icon="MOD_BOOLEAN")
            row.operator("object.duplicate_move_linked", text="Duplicate Linked", icon="CONSTRAINT_DATA")            
                      
             
            box = layout.box().column(1)
             
            row = box.row(1)
            if tp_props.display_copy_to_faces:
                row.prop(tp_props, "display_copy_to_faces", text="", icon='TRIA_DOWN')
            else:
                row.prop(tp_props, "display_copy_to_faces", text="", icon='TRIA_RIGHT')

            Display_Dynamics = context.user_preferences.addons[__name__].preferences.tab_dynamics
            if Display_Dynamics == 'on':     
                row.operator("tp_ops.copy_to_faces", text="",icon="UV_FACESEL")
            else:
                pass
            
            row.operator("tp_ops.copy_to_faces_panel", text="Copy to Faces", icon='BLANK1') 
         
            if tp_props.display_copy_to_faces:
                
                box = layout.box().column(1)
                    
                row = box.row(1)            
                row.label("Origin to:")       
                
                row = box.row(1) 
                row.prop(context.scene, "pl_set_plus_z")       
                row.prop(context.scene, "pl_set_minus_z")  
                
                box.separator() 
                
                row = box.row(1)            
                row.label("Duplication:")

                row = box.row(1)                                           
                row.prop(context.scene, "pl_dupli_linked", text = "Linked")
                row.prop(context.scene, "pl_dupli", text = "Unlinked")

                box.separator() 
                
                row = box.row(1)            
                row.label("To Edit:")     
                
                row = box.row(1) 
                row.prop(context.scene, "pl_set_edit_target", text = "Target")                           
                row.prop(context.scene, "pl_set_edit_source", text = "Source")
                

            box.separator()  

            box = layout.box().column(1) 
             
            row = box.row(1)
            
            Display_Dynamics = context.user_preferences.addons[__name__].preferences.tab_dynamics
            if Display_Dynamics == 'on':          
                row.operator("mft.radialclone", text="", icon="FILE_REFRESH")
            else:
                pass    
            row.operator("mft.radialclone_panel", text="Radial Z-Axis Clone", icon="BLANK1")

            row = box.row(1) 
            row.prop(context.scene, "radialClonesAngle", text="")
            row.prop(context.scene, "clonez", text="")

            box.separator()  
                        
            box = layout.box().column(1) 
             
            row = box.row(1)                     

            Display_Dynamics = context.user_preferences.addons[__name__].preferences.tab_dynamics
            if Display_Dynamics == 'on':
                row.operator("tp_ops.copy_to_cursor", text="", icon="NEXT_KEYFRAME")
            else:
                pass    
                                     
            row.operator("tp_ops.copy_to_cursor_panel", text="Copy to Cursor", icon="BLANK1")                     
            
            row = box.row(1)  
            row.prop(context.scene, "ctc_total", text="How many?")
                                   
            box.separator()            

            box = layout.box().column(1) 
             
            row = box.row(1)  
            row.operator("object.simplearewo", text="ARewO Replicator", icon="FRAME_NEXT")   
          
            box.separator()   

            Display_ModsArray = context.user_preferences.addons[__name__].preferences.tab_array
            if Display_ModsArray == 'on':

                box = layout.box().column(1) 
                 
                row = box.row(1)  
                
                if tp_props.display_array_tools:
                    row.prop(tp_props, "display_array_tools", text="Array Tools", icon='RESTRICT_VIEW_OFF')
                else:
                    row.prop(tp_props, "display_array_tools", text="Array Tools", icon='RESTRICT_VIEW_ON')  

                if tp_props.display_array_tools:
                   
                    box = layout.box().column(1) 

                    row = box.row(1) 
                    if tp_props.display_axis_array:
                        row.prop(tp_props, "display_axis_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_axis_array", text="", icon='TRIA_RIGHT')   
                                      
                    row.operator("tp_ops.x_array", text="X Array")    
                    row.operator("tp_ops.y_array", text="Y Array")    
                    row.operator("tp_ops.z_array", text="Z Array")      

                    if tp_props.display_axis_array:
                                            
                        mod_types = []
                        append = mod_types.append

                        obj = context.active_object     
                        if obj:
                            if obj.modifiers:
                                  
                                box = layout.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                row.operator("tp_ops.expand_mod","" ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", "" ,icon = 'TRIA_UP') 

                                row = box.row(1) 
                                row.operator("tp_ops.modifier_off","off" ,icon = 'VISIBLE_IPO_OFF')  
                                row.operator("tp_ops.modifier_on", "on" ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text="del." , icon='X') 
                                row.operator("tp_ops.apply_mod", text="set" , icon='FILE_TICK') 
                   
                                box.separator()
                                
                                for mod in context.active_object.modifiers:

                                    row = box.row(1)

                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)                                       
                                            
                                            box = layout.box().column(1)
                                            
                                            row = box.row(1)                                        
                                            row.label(mod.name)
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                row.prop(mod, "count", text = "")                    

                                            box.separator()
                                            
                                            row = box.row(1)
                                            row.prop(mod, "relative_offset_displace", text="")

                                            box.separator()
                                            
                                            row = box.row(1)
                                            row.prop(mod, "use_merge_vertices", text="Merge")
                                            row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                            
                                            row = box.row(1)
                                            row.prop(mod, "merge_threshold", text="Distance")

                                    else:
                                        box.separator()  
                            
                            else:
                                box = layout.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.axis_array", text = "! nothing selected !", icon ="INFO")  
                                    
                        else:
                            box = layout.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.axis_array", text = "! nothing selected !", icon ="INFO") 
                            ###                           

                                      
                    box.separator()
                                      
                    box = layout.box().column(1) 

                    row = box.row(1) 
                    if tp_props.display_empty:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_RIGHT')                  
                    
                    row.operator("tp_ops.add_empty_array_mods", text="Empty Plane", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_empty_array", text="", icon="OUTLINER_DATA_EMPTY")

                    row = box.row(1) 
                    if tp_props.display_empty:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_empty", text="", icon='TRIA_RIGHT')                  
                    
                    row.operator("tp_ops.add_empty_curve_mods", text="Empty Array", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_empty_curve", text="", icon="OUTLINER_DATA_CURVE")
                    

                    if tp_props.display_empty:  

                        mod_types = []
                        append = mod_types.append
                                              
                        obj = context.active_object       
                        if obj:

                            if obj.modifiers:
                        
                                box = layout.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                row.operator("tp_ops.expand_mod","" ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", "" ,icon = 'TRIA_UP') 

                                row = box.row(1) 
                                row.operator("tp_ops.modifier_off","off" ,icon = 'VISIBLE_IPO_OFF')  
                                row.operator("tp_ops.modifier_on", "on" ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text="del." , icon='X') 
                                row.operator("tp_ops.apply_mod", text="set" , icon='FILE_TICK') 

                                box.separator()

                                for mod in context.active_object.modifiers:
                                      
                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)
                                            
                                            box = layout.box().column(1) 
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                
                                                row = box.row(1)                                        
                                                row.label("Mesh Array")
                                                
                                                if mod.fit_type == 'FIXED_COUNT':
                                                    row.prop(mod, "count", text = "")                    

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text="")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")

                                                box.separator()   
                                                
                                                row = box.column(1)
                                                row.prop(mod, "offset_object", text="")   
                                                
                                                box.separator()

                                            elif mod.fit_type == 'FIT_CURVE':
                                               
                                                box.separator()
                                            
                                                row = box.row(1)
                                                row.label(text="Mesh Offset")                                                                                      
                                               
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text = "")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")
                                                
                                                box.separator()   
                                                
                                                row = box.row(1)                                          
                                                row.prop(mod, "curve", text = "")    

                                                box.separator()                      
                                       
                                        elif mod.type == 'CURVE':
                                            append(mod.type)                         
                                            
                                            box = layout.box().column(1) 
                                            
                                            row = box.column(1)
                                            row.label(text="Curve Deformation Axis")
                                            
                                            row = box.column(1)                                        
                                            row.row().prop(mod, "deform_axis", expand=True)
                                            
                                            box.separator()
                                            
                                            row = box.column(1) 
                                            row.prop(mod, "object", text="")
                                                                                    
                                            box.separator()
                                
                                    else:
                                        box.separator()  
                            
                            else:
                                box = layout.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.empty_array", text = "! nothing selected !", icon ="INFO")   
                            
                                box = layout.box().column(1) 
                                    
                        else:
                            box = layout.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.empty_array", text = "! nothing selected !", icon ="INFO")             
                            
                            box = layout.box().column(1) 
                          
                          
                    box.separator() 

                    row = box.row(1) 
                    if tp_props.display_array:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_RIGHT')                  

                    row.operator("tp_ops.add_curve_array_mods", text="Curve Array", icon="MOD_ARRAY")     
                    row.operator("tp_ops.add_curve_array", text="", icon="CURVE_BEZCURVE")    
                          
                    row = box.row(1) 
                    if tp_props.display_array:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_array", text="", icon='TRIA_RIGHT')                           

                    row.operator("tp_ops.add_circle_array_mods", text="Circle Array", icon="MOD_ARRAY")
                    row.operator("tp_ops.add_circle_array", text="", icon="CURVE_BEZCIRCLE")
                    
                    if tp_props.display_array:

                        mod_types = []
                        append = mod_types.append
                        
                        obj = context.active_object       
                        if obj:

                            if obj.modifiers:
                         
                                box = layout.box().column(1)                 
                                
                                row = box.row(1)
                                row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                row.operator("tp_ops.expand_mod","" ,icon = 'TRIA_DOWN')  
                                row.operator("tp_ops.collapse_mod", "" ,icon = 'TRIA_UP') 

                                row = box.row(1) 
                                row.operator("tp_ops.modifier_off","off" ,icon = 'VISIBLE_IPO_OFF')  
                                row.operator("tp_ops.modifier_on", "on" ,icon = 'RESTRICT_VIEW_OFF') 
                                row.operator("tp_ops.remove_mod", text="del." , icon='X') 
                                row.operator("tp_ops.apply_mod", text="set" , icon='FILE_TICK') 

                                box.separator() 
                        
                                for mod in context.active_object.modifiers:
                                      
                                    if mod.show_expanded == True:
                                        if mod.type == 'ARRAY':
                                            append(mod.type)
                                            
                                            box = layout.box().column(1) 
                                            
                                            if mod.fit_type == 'FIXED_COUNT':
                                                
                                                row = box.row(1)                                        
                                                row.label("Mesh Array")
                                                
                                                if mod.fit_type == 'FIXED_COUNT':
                                                    row.prop(mod, "count", text = "")                    

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text="")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")

                                                box.separator()   
                                                
                                                row = box.column(1)
                                                row.prop(mod, "offset_object", text="")   
                                                
                                                box.separator()

                                            elif mod.fit_type == 'FIT_CURVE':
                                               
                                                box.separator()
                                            
                                                row = box.row(1)
                                                row.label(text="Mesh Offset")                                                                                      
                                               
                                                row = box.row(1)
                                                row.prop(mod, "relative_offset_displace", text = "")

                                                box.separator()
                                                
                                                row = box.row(1)
                                                row.prop(mod, "use_merge_vertices", text="Merge")
                                                row.prop(mod, "use_merge_vertices_cap", text="First Last")
                                                
                                                row = box.row(1)
                                                row.prop(mod, "merge_threshold", text="Distance")
                                                
                                                box.separator()   
                                                
                                                row = box.row(1)                                          
                                                row.prop(mod, "curve", text = "")    

                                                box.separator()                      
                                       
                                        elif mod.type == 'CURVE':
                                            append(mod.type)                         
                                            
                                            box = layout.box().column(1) 
                                            
                                            row = box.column(1)
                                            row.label(text="Curve Deformation Axis")
                                            
                                            row = box.column(1)                                        
                                            row.row().prop(mod, "deform_axis", expand=True)
                                            
                                            box.separator()
                                            
                                            row = box.column(1) 
                                            row.prop(mod, "object", text="")
                                                                                    
                                            box.separator()
                                
                                    else:
                                        box.separator()  
                            
                            else:
                                box = layout.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.curve_array", text = "! nothing selected !", icon ="INFO")   
                            
                                box = layout.box().column(1) 
                                    
                        else:
                            box = layout.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.curve_array", text = "! nothing selected !", icon ="INFO")             
                            
                            box = layout.box().column(1) 
                          
                      
                    box.separator()                        
                     
                    row = box.row(1) 
                    if tp_props.display_pfath:
                        row.prop(tp_props, "display_pfath", text="", icon='TRIA_DOWN')
                    else:
                        row.prop(tp_props, "display_pfath", text="", icon='TRIA_RIGHT')            

                    Display_Dynamics = context.user_preferences.addons[__name__].preferences.tab_dynamics
                    if Display_Dynamics == 'on':     
                        row.operator("object.fpath_array", text="", icon ="ALIGN")                              
                    else:
                        pass
                    
                    row.operator("tp_ops.add_fpath_con", text="Add Follow Path", icon="CONSTRAINT_DATA")          
                    row.operator("tp_ops.add_fpath_curve", text="", icon="CURVE_BEZCIRCLE")
                   
                    box.separator() 
                    
                    if tp_props.display_pfath:
                        
                        con_types = []
                        append = con_types.append
                        
                        obj = context.active_object     
                        if obj:                                            
                            if obj.constraints:
                                                                                            
                                for con in context.active_object.constraints:

                                    box = layout.box().column(1)
                            
                                    row = box.row(1)
                                    row.operator("object.fpath_array_panel", text="Set FPath Array", icon ="MOD_ARRAY")  
                                    
                                    box.separator()
                                    
                                    row = box.row(1)
                                    row.prop(context.scene, "type", )    
                                    
                                    row = box.row(1)                            
                                    row.prop(context.scene, "count")

                                                                     
                                    box.separator() 

                                    row = box.row(1)
                                    layout.operator_context = 'INVOKE_REGION_WIN'                    
                                    row.prop(context.scene, "frame_current", text="Frame")
                                    row.operator("object.select_grouped", text="Select Group").type='GROUP'
                                        
                                    row = box.row(1)      
                                    row.operator("tp_ops.linked_fpath",text="Set Linked")                  
                                    row.operator("tp_ops.single_fpath",text="Set Unlinked")  

                                    box.separator() 
                                    
                                    box = layout.box().column(1)                 
                                    
                                    row = box.row(1)
                                      
                                    row.operator("object.transform_apply", text="Applied Scale?", icon="OUTLINER_DATA_EMPTY").scale=True
                                    row.operator("tp_ops.expand_con","" ,icon = 'TRIA_DOWN')  
                                    row.operator("tp_ops.collapse_con", "" ,icon = 'TRIA_UP') 

                                    row = box.row(1) 
                                    row.operator("tp_ops.constraint_off","off" ,icon = 'VISIBLE_IPO_OFF')  
                                    row.operator("tp_ops.constraint_on", "on" ,icon = 'RESTRICT_VIEW_OFF') 
                                    row.operator("object.constraints_clear", text="clear" , icon='X') 

                                    box.separator()                                     

                                    if con.show_expanded == True:  
                                                                                
                                        box = layout.box().column(1) 
                                
                                        row = box.row(1)  
                                        
                                        if con.type == 'FOLLOW_PATH':
                                           
                                            append(con.type)

                                            box.label(con.name)
                                            
                                            box.prop(con, "target")

                                            box.separator() 
                                            
                                            row = box.column(1)                                                      
                                            row.operator("constraint.followpath_path_animate", text="Animate Path", icon='ANIM_DATA')
                                            row.label("!need activation in properties!")  
                                            
                                            box.separator()
                                            
                                            if context.scene.type == "OFFSET":
                                                row.prop(context.scene,"offset")
                                       
                                            elif context.scene.type == "FIXED_POSITION":
                                                row.prop(context.scene,"factor", "Offset")
                                                                                         
                                            box.separator() 
                                            
                                            row.prop(con, "use_curve_follow")
                                            
                                            row = box.row(1)
                                            row.label("Axis")
                                            row.prop(con, "forward_axis", expand=True)

                                            box.separator() 
                                            
                                            row = box.row(1)                            
                                            row.prop(con, "up_axis", text="Up")
                                            row.label()

                                            ###
                                            box.separator()   
                                    
                            else:
                                box = layout.box().column(1) 
                                
                                row = box.row(1)
                                row.operator("tp_help.follow_path", text ="! no constraint active !", icon ="INFO")  
                                    
                        else:
                            box = layout.box().column(1) 
                            
                            row = box.row(1)
                            row.operator("tp_help.follow_path", text = "! nothing selected !", icon ="INFO")             

            else:
                pass

            Display_DupliTools = context.user_preferences.addons[__name__].preferences.tab_dupli 
            if Display_DupliTools == 'on':     

                obj = context.active_object     
                if obj:
                    obj_type = obj.type
                                                                          
                    if obj_type in {'MESH'}:

                        box = layout.box().column(1)
                        
                        row = box.row(1)
                        row.operator("tp_ops.dupli_set_panel", "Duplication to Active", icon = "CONSTRAINT_DATA") 

                        box.separator()
                                    
                        row = box.row(1)
                        row.prop(context.object, "dupli_type", expand=True)            

                        box.separator()
                                   
                        if context.object.dupli_type == 'FRAMES':
                            row = box.row(1)   
                            row.prop(context.object, "dupli_frames_start", text="Start")
                            row.prop(context.object, "dupli_frames_end", text="End")

                            row = box.row(1)                           
                            row.prop(context.object, "dupli_frames_on", text="On")
                            row.prop(context.object, "dupli_frames_off", text="Off")

                            row = box.row(1)   
                            row.prop(context.object, "use_dupli_frames_speed", text="Speed")

                        elif context.object.dupli_type == 'VERTS':
                            row = box.row(1)   
                            row.prop(context.object, "use_dupli_vertices_rotation", text="Rotation")

                        elif context.object.dupli_type == 'FACES':
                            row = box.row(1)                       
                            row.prop(context.object, "use_dupli_faces_scale", text="Scale")
                           
                            sub = row.row()
                            sub.active = context.object.use_dupli_faces_scale
                            sub.prop(context.object, "dupli_faces_scale", text="Inherit Scale")

                        elif context.object.dupli_type == 'GROUP':
                            row = box.row(1)
                            row.prop(context.object, "dupli_group", text="Group")

                        row = box.row(1)
                        row.prop(context.scene, "dupli_align", text="Align")
                        row.prop(context.scene, "dupli_single", text="Single")
                        
                        if context.scene.dupli_single == True:
                            
                            row = box.row(1)            
                            row.prop(context.scene, "dupli_separate", text="Separate")
                            row.prop(context.scene, "dupli_link", text="As Instance")


            box.separator() 
             
            box = layout.box().column(1) 
             
            row = box.row(1)
            
            if tp_props.display_toall:
                row.prop(tp_props, "display_toall", text="", icon='TRIA_DOWN')
            else:
                row.prop(tp_props, "display_toall", text="", icon='TRIA_RIGHT')

            row.menu("VIEW3D_MT_copypopup", text="Advance Copy", icon = "DISCLOSURE_TRI_RIGHT") 
         
            if tp_props.display_toall:
                scene = context.scene
                
                box = layout.box().column(1)
                    
                row = box.row(1) 
                row.alignment = 'CENTER'                
                row.label("Material", icon='MATERIAL') 

                row = box.row(1) 
                row.label("copy to:") 
                                  
                row = box.row(1)   
                row.operator("scene.to_all", text="Selected").mode = "material, selected"
                row.operator("scene.to_all", text="Children").mode = "material, children"

                box.separator()
                                
                row = box.row(1) 
                row.label("append to:") 
                                  
                row = box.row(1)   
                row.operator("scene.to_all", text="Selected").mode = "material, selected, append"
                row.operator("scene.to_all", text="Children").mode = "material, children, append"

                box.separator()

                box = layout.box().column(1)
                    
                row = box.row(1) 
                row.alignment = 'CENTER'                
                row.label("Modifier", icon='MODIFIER') 
 
                row = box.row(1) 
                row.label("copy to:") 
                                  
                row = box.row(1)   
                row.operator("scene.to_all", text="Selected").mode = "modifier, selected"
                row.operator("scene.to_all", text="Children").mode = "modifier, children"

                box.separator()                

                row = box.row(1) 
                row.label("append to:") 
                                  
                row = box.row(1)   
                row.operator("scene.to_all", text="Selected").mode = "modifier, selected, append"
                row.operator("scene.to_all", text="Children").mode = "modifier, children, append"
                
                box.separator()  

                row = box.row(1)
                row.prop(context.scene, "excludeMod")              
                


            Display_LinkedTools = context.user_preferences.addons[__name__].preferences.tab_linked
            if Display_LinkedTools == 'on':
                
                box.separator()      

                box = layout.box().column(1) 
                 
                row = box.column(1)
                row.label("Linked Instances", icon = "CONSTRAINT_DATA")
                
                box.separator() 
                                 
                row = box.row(1)     
                row.operator("object.make_links_data","Set", icon="LINKED").type='OBDATA'
                row.operator("tp_ops.make_single","Clear", icon="UNLINKED")
               
                box.separator() 
               
                row = box.row(1)                 
                row.operator("object.select_linked", text="Select Linked", icon="RESTRICT_SELECT_OFF")   
                row.operator("object.join", text="Join all", icon="AUTOMERGE_ON")             

                box.separator() 
               
                row = box.row(1)  

                row.operator_menu_enum("object.make_links_data", "type","links",  icon="CONSTRAINT")
                
                sub = row.row(1)
                sub.scale_x = 0.3333            
                sub.operator("tp_ops.origin_plus_z", text="T", icon="LAYER_USED")  
                sub.operator("object.origin_set", text="M", icon="LAYER_USED").type='ORIGIN_GEOMETRY'
                sub.operator("tp_ops.origin_minus_z", text="B", icon="LAYER_USED")

                box.separator()

            else:
                pass


        if context.mode == 'EDIT_MESH':

            box = layout.box().column(1)
             
            row = box.column(1)
            row.operator("mesh.duplicate_move", text="Duplicate", icon="MOD_BOOLEAN")
            
            box = layout.box().column(1) 
             
            row = box.column(1)  
            row.operator("tp_ops.copy_to_cursor_panel", text="Copy to Cursor", icon="NEXT_KEYFRAME")                      
            row.prop(context.scene, "ctc_total", text="How many?")

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

        else:
            pass     
  
  
        

class VIEW3D_TP_Copy_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Tools"
    bl_idname = "VIEW3D_TP_Copy_Panel_TOOLS"
    bl_label = "CopyShop"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)   
        return isModelingMode 


    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'

        draw_copy_panel_layout(self, context, layout) 
        

class VIEW3D_TP_Copy_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Copy_Panel_UI"
    bl_label = "CopyShop"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object) 
        return isModelingMode 


    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.operator_context = 'INVOKE_AREA'                                   

        draw_copy_panel_layout(self, context, layout) 




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
        
    update_panel_position(None, bpy.context)
    
    ### copyaction
    bpy.types.WindowManager.tp_collapse_copyshop_props = bpy.props.PointerProperty(type = Dropdown_TP_CopyShop_Props)
   
    ### miftthtools
    bpy.types.Scene.mifthTools = PointerProperty(name="Mifth Tools Variables", type=MFTProperties, description="Mifth Tools Properties")


    ### Tools
    update_menu(None, bpy.context)
    update_display_tools(None, bpy.context)


def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    ### copyaction
    del bpy.types.WindowManager.tp_collapse_copyshop_props 
 
    ### miftthtools
    del bpy.types.Scene.mifthTools     



if __name__ == "__main__":
    register()
        
        





