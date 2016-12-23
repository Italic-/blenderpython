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
    "name": "TP Origin",
    "author": "MKB",
    "version": (0, 1, 3),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N]",
    "description": "Origin Tools Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}


from toolplus_origin.origin_batch   import (View3D_TP_Origin_BBox)

##################################

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_origin'))

if "bpy" in locals():
    import imp
    imp.reload(origin_action)
    imp.reload(origin_align)
    imp.reload(origin_batch)
    imp.reload(origin_bbox)
    imp.reload(origin_distribute)
    imp.reload(origin_modal)
    imp.reload(origin_operators)
    imp.reload(origin_pivot)


else:
    from . import origin_action         
    from . import origin_align         
    from . import origin_batch         
    from . import origin_bbox         
    from . import origin_distribute         
    from . import origin_modal         
    from . import origin_operators         
    from . import origin_pivot         



import bpy
from bpy import*

import bpy.utils.previews
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)

def update_panel_position(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Origin_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Origin_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Origin_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':
        VIEW3D_TP_Origin_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        bpy.utils.register_class(VIEW3D_TP_Origin_Panel_TOOLS)
    
    else:
        bpy.utils.register_class(VIEW3D_TP_Origin_Panel_UI)
  


def update_display_tools(self, context):

    if context.user_preferences.addons[__name__].preferences.tab_dynamics == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_align == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_align_menu == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_transform == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_transform_menu == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_bbox == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_bbox_menu == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_history == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_history_menu == 'on':
        return True

    if context.user_preferences.addons[__name__].preferences.tab_dynamics == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_align == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_align_menu == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_transform == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_transform_menu == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_bbox == 'off':
        return False 
    elif context.user_preferences.addons[__name__].preferences.tab_bbox_menu == 'off':
        return False     
    elif context.user_preferences.addons[__name__].preferences.tab_history == 'off':
        return False     
    elif context.user_preferences.addons[__name__].preferences.tab_history_menu == 'off':
        return False 
    
    
    
addon_keymaps_menu = []

def update_menu(self, context):
    try:
        bpy.utils.unregister_class(View3D_TP_Origin_BBox)
        
        # Keymapping
        # remove keymaps when add-on is deactivated
        wm = bpy.context.window_manager
        for km in addon_keymaps_menu:
            wm.keyconfigs.addon.keymaps.remove(km)
        del addon_keymaps_menu[:]
        
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'menu':
     
        View3D_TP_Origin_BBox.bl_category = context.user_preferences.addons[__name__].preferences.tab_menu_view
    
        bpy.utils.register_class(View3D_TP_Origin_BBox)
    
        # Keymapping 
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('tp_batch.origin_bbox', 'TWO', 'PRESS', alt=True) #,ctrl=True, shift=True, 
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

    tab_align = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Align on', 'enable tools in panel'), ('off', 'Align off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_align_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Align on', 'enable tools in menu'), ('off', 'Align off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_transform = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Transform on', 'enable tools in panel'), ('off', 'Transform off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_transform_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Transform on', 'enable tools in menu'), ('off', 'Transform off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_bbox = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Bounds on', 'enable tools in panel'), ('off', 'Bounds off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_bbox_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Bounds on', 'enable tools in menu'), ('off', 'Bounds off', 'disable tools in menu')), default='on', update = update_display_tools)

    tab_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_history_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)


    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position)



    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            
            box = layout.box().column(1)
            
            row = box.column(1)   
            row.label(text="Welcome to Origin!")  
            row.label(text="This custom addon allows to correct your origin for:")
            row.label(text="> modifier or object align")   
            row.label(text="There are three ways to execute the tools:")   
            row.label(text="> use the panel function or the included menu")   
            row.label(text="> or use the dynamic tools in your own custom pie menu")     
            row.label(text="Have Fun! :)")         


        #Tools
        if self.prefs_tabs == 'toolsets':
          
            box = layout.box().column(1)

            row = box.row()
            row.prop(self, 'tab_dynamics', expand=True)
            row.prop(self, 'tab_align', expand=True)
            row.prop(self, 'tab_transform', expand=True)
            row.prop(self, 'tab_bbox', expand=True)
            row.prop(self, 'tab_history', expand=True)

            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 
            

        #Location
        if self.prefs_tabs == 'location':
            
            box = layout.box().column(1)
             
            row = box.row(1) 
            row.label("Location Origin:")
            
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
            row.label("Origin Menu:", icon ="COLLAPSEMENU") 
            
            row.separator()           
            row.label("Menu: 'TWO', 'PRESS', alt=True")

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
            row.prop(self, 'tab_align_menu', expand=True)
            row.prop(self, 'tab_transform_menu', expand=True)
            row.prop(self, 'tab_bbox_menu', expand=True)
            row.prop(self, 'tab_history_menu', expand=True)

            box.separator() 
            
            row = layout.row(1) 
            row.label(text="! if needed change keys durably in TAB Input !", icon ="INFO")


        #Weblinks
        if self.prefs_tabs == 'url':
            row = layout.row()
            row.operator('wm.url_open', text = 'Distribute', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Oscurart_Tools"
            row.operator('wm.url_open', text = 'Advance Origin', icon = 'HELP').url = "http://blenderlounge.fr/forum/viewtopic.php?f=18&t=1438"
            row.operator('wm.url_open', text = 'Advance Align', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?256114-Add-on-Advanced-align-tools"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?410351-Addon-T-Origin&p=3119318#post3119318"



class DropdownOriginToolProps(bpy.types.PropertyGroup):

    display_origin_editbox = bpy.props.BoolProperty(name="Origin BBox", description="open / close", default=False)
    display_origin_bbox = bpy.props.BoolProperty(name="Origin BBox", description="open / close", default=True)



def draw_origin_panel_layout(self, context, layout):
    
        lt = context.window_manager.bbox_origin_window     
          
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
            Display_Dynamics = context.user_preferences.addons[__name__].preferences.tab_dynamics
            if Display_Dynamics == 'on':       
                row.operator("tp_batch.origin_bbox", text="Origin Menu", icon="LAYER_ACTIVE")           

            row.operator("object.origin_set", text="3D Cursor", icon="LAYER_ACTIVE").type='ORIGIN_CURSOR' 
            row.operator("object.origin_set", text="Center of Mass", icon="LAYER_ACTIVE").type='ORIGIN_CENTER_OF_MASS' 
            row.operator("object.origin_set", text="Geometry to Origin", icon="LAYER_ACTIVE").type='GEOMETRY_ORIGIN' 

            box.separator() 

            if bpy.context.object.type == 'MESH':

                 box = layout.box().column(1)
                 row = box.row(1)
                
                 if lt.display_origin_bbox:
                     row.prop(lt, "display_origin_bbox", text="", icon='TRIA_DOWN')            
                     row.operator("object.origin_modal", text="BBox Origin", icon="BLANK1")           
                 else:                
                     row.prop(lt, "display_origin_bbox", text="", icon='TRIA_RIGHT')
                     row.operator("object.origin_modal", text="BBox Origin", icon="BLANK1")
                    
                 if lt.display_origin_bbox: 
                 
                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("+Y") 
                     row.label("Axis") 
                     row.label("Back") 
                     
                     #Top
                     row = box.column(1)                  
                     row.operator("tp_ops.cubeback_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")#"Back- Left -Top")
                     row.operator("tp_ops.cubefront_edgemiddle_minus_x", "", icon = "LAYER_ACTIVE")#"Back- Left")
                     row.operator("tp_ops.cubeback_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Back- Left -Bottom")
                      
                     #Middle
                     row = box.column(1)
                     row.operator("tp_ops.cubeback_edgetop_minus_y", "", icon = "LAYER_ACTIVE")#"Back - Top")                            
                     row.operator("tp_ops.cubefront_side_plus_y","", icon = "LAYER_ACTIVE")# "Back")                 
                     row.operator("tp_ops.cubefront_edgebottom_plus_y","", icon = "LAYER_ACTIVE")#"Back - Bottom") 
                      
                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubeback_cornertop_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Top ")                 
                     row.operator("tp_ops.cubefront_edgemiddle_plus_x","", icon = "LAYER_ACTIVE")#"Back- Right")      
                     row.operator("tp_ops.cubeback_cornerbottom_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Bottom")  
                
                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()
                     
                     ############################

                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("XZ") 
                     row.label("Axis") 
                     row.label("Center") 
                     
                     #Top
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_edgetop_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Top")
                     row.operator("tp_ops.cubefront_side_minus_x","", icon = "LAYER_ACTIVE")# "Left")         
                     row.operator("tp_ops.cubefront_edgebottom_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Bottom")
                      
                     #Middle
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_side_plus_z", "", icon = "LAYER_ACTIVE")#"Top")  
                     obj = context.object
                     if obj and obj.mode == 'EDIT':          
                         row.operator("mesh.origincenter", text="", icon="LAYER_ACTIVE") 
                     else:
                         row.operator("object.origin_set", text="", icon="LAYER_ACTIVE").type='ORIGIN_GEOMETRY'                    
                     row.operator("tp_ops.cubefront_side_minus_z","", icon = "LAYER_ACTIVE")# "Bottom")    

                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_edgetop_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Top")  
                     row.operator("tp_ops.cubefront_side_plus_x","", icon = "LAYER_ACTIVE")# "Right")            
                     row.operator("tp_ops.cubefront_edgebottom_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Bottom")  

                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()

                     ############################
                     
                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("-- Y") 
                     row.label("Axis") 
                     row.label("Front") 
                    
                     #Top
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")# "Front- Left -Top"
                     row.operator("tp_ops.cubefront_edgemiddle_minus_y","", icon = "LAYER_ACTIVE")# "Front- Left"  
                     row.operator("tp_ops.cubefront_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Front- Left -Bottom"  
                               
                     #Middle
                     row = box.column(1) 
                     row.operator("tp_ops.cubeback_edgetop_plus_y","", icon = "LAYER_ACTIVE")# "Front - Top"                                      
                     row.operator("tp_ops.cubefront_side_minus_y","", icon = "LAYER_ACTIVE")#  "Front"           
                     row.operator("tp_ops.cubefront_edgebottom_minus_y","", icon = "LAYER_ACTIVE")# "Front - Bottom"           

                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_cornertop_plus_xy","", icon = "LAYER_ACTIVE")#  "Front- Right -Top"
                     row.operator("tp_ops.cubefront_edgemiddle_plus_y","", icon = "LAYER_ACTIVE")# "Front- Right"    
                     row.operator("tp_ops.cubefront_cornerbottom_plus_xy", "", icon = "LAYER_ACTIVE")# "Front- Right -Bottom") 

                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()
                     

            Display_Transform = context.user_preferences.addons[__name__].preferences.tab_transform
            if Display_Transform == 'on':
                 
                box = layout.box().column(1) 
                 
                row = box.row(1)
                row.label("", icon = "MAN_TRANS")
                row.label("", icon = "MAN_ROT")
                row.label("", icon = "MAN_SCALE")
                row.label("Apply Transform")
                
                row = box.row(1)                
                row.operator("object.transform_apply", "Location").location=True 
                row.operator("object.transform_apply", "Rotation").rotation=True 
                row.operator("object.transform_apply", "Scale").scale=True 
                
                row = box.row(1)
                sub = row.row(1)
                sub.scale_x = 0.45                 
                sub.operator("object.location_clear", "ZeroObj").clear_delta=False
                sub.operator("tp_ops.zero_cursor", "Zero3dC")
                
                sub1 = row.row(1)
                sub1.scale_x = 0.15                
                sub1.operator("tp_ops.zero_x", "X")
                sub1.operator("tp_ops.zero_y", "Y")
                sub1.operator("tp_ops.zero_z", "Z")
                
                box.separator()
                

            Display_Align = context.user_preferences.addons[__name__].preferences.tab_align
            if Display_Align == 'on':
                 
                box = layout.box().column(1) 
                 
                row = box.column(1)
                row.operator("object.align_tools", icon = "MANIPUL")
                row.operator("object.distribute_osc", icon = "ALIGN")
                
                box.separator()
 
            box = layout.box().column(1) 
             
            row = box.row(1)            
            row.operator("tp_ops.bounding_box_simple", "add BoundBox", icon = "MOD_LATTICE")

            Display_BBox = context.user_preferences.addons[__name__].preferences.tab_bbox
            if Display_BBox == 'on':

                row = box.row(1)
                row.prop(context.object, "show_bounds", text="Show Bounds", icon='STICKY_UVS_LOC') 

                sub = row.row(1)
                sub.scale_x = 0.5  
                sub.prop(context.object, "draw_bounds_type", text="") 

            box.separator()                                     

        else:

            box = layout.box().row()
            
            row = box.column(1) 
            row.label("Origin", icon = "EDITMODE_HLT") 
            row.label("  in  ", icon = "BLANK1") 
            row.label("  Editmode") 
            
            row = box.column(1) 
            row.operator("tp_ops.origin_cursor_edm","> Cursor")
            row.operator("tp_ops.origin_edm","> Active")   
            row.operator("tp_ops.origin_edm","> Selected")   
            
            box.separator()  
            
            box = layout.box().row()            
                                
            row = box.column(1) 
            row.label("Origin", icon = "OBJECT_DATAMODE") 
            row.label("   to  ", icon = "BLANK1") 
            row.label("Objectmode") 
                                    
            row = box.column(1) 
            row.operator("tp_ops.origin_cursor_obm","> Cursor")  
            row.operator("tp_ops.origin_obm","> Active")             
            row.operator("tp_ops.origin_obm","> Selected")             
     
            box.separator() 

            if context.mode == 'EDIT_MESH':

                box = layout.box().column(1)
                row = box.row(1)
                
                if lt.display_origin_editbox:
                    row.prop(lt, "display_origin_editbox", text="BBox Origin", icon='TRIA_DOWN')            
                else:                
                    row.prop(lt, "display_origin_editbox", text="BBox Origin", icon='TRIA_RIGHT')
                    
                if lt.display_origin_editbox:        

                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("+Y") 
                     row.label("Axis") 
                     row.label("Back") 
                     
                     #Top
                     row = box.column(1)                  
                     row.operator("tp_ops.cubeback_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")#"Back- Left -Top")
                     row.operator("tp_ops.cubefront_edgemiddle_minus_x", "", icon = "LAYER_ACTIVE")#"Back- Left")
                     row.operator("tp_ops.cubeback_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Back- Left -Bottom")
                      
                     #Middle
                     row = box.column(1)
                     row.operator("tp_ops.cubeback_edgetop_minus_y", "", icon = "LAYER_ACTIVE")#"Back - Top")                            
                     row.operator("tp_ops.cubefront_side_plus_y","", icon = "LAYER_ACTIVE")# "Back")                 
                     row.operator("tp_ops.cubefront_edgebottom_plus_y","", icon = "LAYER_ACTIVE")#"Back - Bottom") 
                      
                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubeback_cornertop_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Top ")                 
                     row.operator("tp_ops.cubefront_edgemiddle_plus_x","", icon = "LAYER_ACTIVE")#"Back- Right")      
                     row.operator("tp_ops.cubeback_cornerbottom_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Bottom")  
                
                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()
                     
                     ############################

                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("XZ") 
                     row.label("Axis") 
                     row.label("Center") 
                     
                     #Top
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_edgetop_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Top")
                     row.operator("tp_ops.cubefront_side_minus_x","", icon = "LAYER_ACTIVE")# "Left")         
                     row.operator("tp_ops.cubefront_edgebottom_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Bottom")
                      
                     #Middle
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_side_plus_z", "", icon = "LAYER_ACTIVE")#"Top")  
                     row.operator("tp_ops.origin_set_editcenter", text="", icon="LAYER_ACTIVE")                
                     row.operator("tp_ops.cubefront_side_minus_z","", icon = "LAYER_ACTIVE")# "Bottom")    

                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_edgetop_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Top")  
                     row.operator("tp_ops.cubefront_side_plus_x","", icon = "LAYER_ACTIVE")# "Right")            
                     row.operator("tp_ops.cubefront_edgebottom_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Bottom")  

                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()

                     ############################
                     
                     box = layout.box().row(1)

                     row = box.column(1) 
                     row.label("-- Y") 
                     row.label("Axis") 
                     row.label("Front") 
                    
                     #Top
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")# "Front- Left -Top"
                     row.operator("tp_ops.cubefront_edgemiddle_minus_y","", icon = "LAYER_ACTIVE")# "Front- Left"  
                     row.operator("tp_ops.cubefront_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Front- Left -Bottom"  
                               
                     #Middle
                     row = box.column(1) 
                     row.operator("tp_ops.cubeback_edgetop_plus_y","", icon = "LAYER_ACTIVE")# "Front - Top"                                      
                     row.operator("tp_ops.cubefront_side_minus_y","", icon = "LAYER_ACTIVE")#  "Front"           
                     row.operator("tp_ops.cubefront_edgebottom_minus_y","", icon = "LAYER_ACTIVE")# "Front - Bottom"           

                     #Bottom
                     row = box.column(1) 
                     row.operator("tp_ops.cubefront_cornertop_plus_xy","", icon = "LAYER_ACTIVE")#  "Front- Right -Top"
                     row.operator("tp_ops.cubefront_edgemiddle_plus_y","", icon = "LAYER_ACTIVE")# "Front- Right"    
                     row.operator("tp_ops.cubefront_cornerbottom_plus_xy", "", icon = "LAYER_ACTIVE")# "Front- Right -Bottom") 

                     box.separator()
                     box.separator()
                     box.separator()
                     
                     row.separator()


            Display_Transform = context.user_preferences.addons[__package__].preferences.tab_transform_menu
            if Display_Transform == 'on':

                box = layout.box().column(1) 
                 
                row = box.row(1)
                row.label("", icon = "MAN_TRANS")
                row.label("", icon = "MAN_ROT")
                row.label("", icon = "MAN_SCALE")
                row.label("Apply Transform")

                
                row = box.row(1)
                sub = row.row(1)
                sub.scale_x = 0.45                 
                sub.operator("object.location_clear", "ZeroObj").clear_delta=False
                sub.operator("tp_ops.zero_cursor", "Zero3dC")
                
                sub1 = row.row(1)
                sub1.scale_x = 0.15                
                sub1.operator("tp_ops.zero_x", "X")
                sub1.operator("tp_ops.zero_y", "Y")
                sub1.operator("tp_ops.zero_z", "Z")


            
        Display_History = context.user_preferences.addons[__name__].preferences.tab_history 
        if Display_History == 'on':
            
            box = layout.box().column(1)  

            row = box.row(1)        
            row.operator("view3d.ruler", text="Ruler")   
             
            row.operator("ed.undo_history", text="History")
            row.operator("ed.undo", text="", icon="LOOP_BACK")
            row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
            box.separator()   




class VIEW3D_TP_Origin_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Origin"
    bl_idname = "VIEW3D_TP_Origin_Panel_TOOLS"
    bl_label = "Origin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_origin_panel_layout(self, context, layout) 



class VIEW3D_TP_Origin_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Origin_Panel_UI"
    bl_label = "Origin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'  

        draw_origin_panel_layout(self, context, layout) 




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

    bpy.types.WindowManager.bbox_origin_window = bpy.props.PointerProperty(type = DropdownOriginToolProps)
        
    update_menu(None, bpy.context)
    update_display_tools(None, bpy.context)
    update_panel_position(None, bpy.context)


def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    
    del bpy.types.WindowManager.bbox_origin_window
    
if __name__ == "__main__":
    register()
        
        




              