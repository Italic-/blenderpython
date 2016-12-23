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
    "name": "TP Boolean",
    "author": "Multi Authors (see URL), MKB",
    "version": (0, 1, 2),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N] ",
    "description": "Boolean Tools Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}


from toolplus_boolean.bool_booltools3    import (BoolTool_Brush_TOOLS)
from toolplus_boolean.bool_booltools3    import (BoolTool_Brush_UI)

from toolplus_boolean.bool_booltools3    import (BoolTool_BViwer_TOOLS)
from toolplus_boolean.bool_booltools3    import (BoolTool_BViwer_UI)

from toolplus_boolean.bool_booltools3    import (BoolTool_Config_TOOLS)
from toolplus_boolean.bool_booltools3    import (BoolTool_Config_UI)

##################################

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_boolean'))

if "bpy" in locals():
    import imp
    imp.reload(bool_action)
    imp.reload(bool_boolean2d)
    imp.reload(bool_booltools3)

else:
    from . import bool_action         
    from . import bool_boolean2d         
    from . import bool_booltools3                                   

    
    
import bpy
from bpy import*

import bpy.utils.previews
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)

def update_panel_position(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Edit_Boolean_Panel_UI)
        
        bpy.utils.unregister_class(VIEW3D_TP_Edit_Boolean_Panel_TOOLS)
        
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Edit_Boolean_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':
     
        VIEW3D_TP_Edit_Boolean_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
    
        bpy.utils.register_class(VIEW3D_TP_Edit_Boolean_Panel_TOOLS)
    
    else:
        bpy.utils.register_class(VIEW3D_TP_Edit_Boolean_Panel_UI)
  


def update_panel_position_brush(self, context):
    try:
        bpy.utils.unregister_class(BoolTool_Brush_UI)
        bpy.utils.unregister_class(BoolTool_BViwer_UI)
        bpy.utils.unregister_class(BoolTool_Config_UI)
        
        bpy.utils.unregister_class(BoolTool_Brush_TOOLS)
        bpy.utils.unregister_class(BoolTool_BViwer_TOOLS)
        bpy.utils.unregister_class(BoolTool_Config_TOOLS)
        
    except:
        pass
    
    try:
        bpy.utils.unregister_class(BoolTool_Brush_UI)
        bpy.utils.unregister_class(BoolTool_BViwer_UI)
        bpy.utils.unregister_class(BoolTool_Config_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_brush == 'tools':
     
        BoolTool_Brush_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_brush
        BoolTool_BViwer_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_brush
        BoolTool_Config_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_brush
    
        bpy.utils.register_class(BoolTool_Brush_TOOLS)
        bpy.utils.register_class(BoolTool_BViwer_TOOLS)
        bpy.utils.register_class(BoolTool_Config_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_brush == 'ui':
        bpy.utils.register_class(BoolTool_Brush_UI)
        bpy.utils.register_class(BoolTool_BViwer_UI)
        bpy.utils.register_class(BoolTool_Config_UI)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_brush == 'off':
        pass



def update_display_tools(self, context):

    if context.user_preferences.addons[__name__].preferences.tab_history == 'on':
        return True
    elif context.user_preferences.addons[__name__].preferences.tab_history_menu == 'on':
        return True
   
    if context.user_preferences.addons[__name__].preferences.tab_history == 'off':
        return False     
    elif context.user_preferences.addons[__name__].preferences.tab_history_menu == 'off':
        return False 


addon_keymaps_menu = []

def update_menu(self, context):
    try:
        bpy.utils.unregister_class(BoolTool_Menu)
        
        # Keymapping
        # remove keymaps when add-on is deactivated
        wm = bpy.context.window_manager
        for km in addon_keymaps_menu:
            wm.keyconfigs.addon.keymaps.remove(km)
        del addon_keymaps_menu[:]
        
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'menu':
     
        BoolTool_Menu.bl_category = context.user_preferences.addons[__name__].preferences.tab_menu_view
    
        bpy.utils.register_class(BoolTool_Menu)
    
        # booltool: create the booleanhotkey in opjectmode
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu', 'T', 'PRESS', shift=True) #ctrl=True, alt=True, 
        kmi.properties.name = 'OBJECT_MT_BoolTool_Menu'


    if context.user_preferences.addons[__name__].preferences.tab_menu_view == 'off':
        pass



# booltool: Fast Transformations
def UpdateBoolTool_Pref(self, context):
    if self.fast_transform:
        RegisterFastT()
    else:
        UnRegisterFastT()

      

#Panel preferences
class TP_Panels_Preferences(AddonPreferences):
    bl_idname = __name__
    
    prefs_tabs = EnumProperty(
        items=(('info',       "Info",       "Info"),
               ('toolset',    "Tools",      "Tools"),
               ('location',   "Location",   "Location"),
               ('keys',       "Keys",       "Keys"),
               ('url',        "URLs",       "URLs")),
               default='info')

    #Tab Location           
    tab_location = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]')),
               default='tools', update = update_panel_position)

    tab_location_brush = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off Shelf', 'enable or disable panel in the shelf')),
               default='off', update = update_panel_position_brush)

    tab_menu_view = EnumProperty(
        name = '3d View Menu',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('menu', 'Menu on', 'enable menu for 3d view'),
               ('off', 'Menu off', 'enable or disable menu for 3d view')),
               default='menu', update = update_menu)

    
    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position)
    tools_category_brush = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_brush)

    fast_transform = bpy.props.BoolProperty(name="Fast Transformations", default=False, update=UpdateBoolTool_Pref, description="Replace the Transform HotKeys (G,R,S) for a custom version that can optimize the visualization of Brushes")
    make_vertex_groups = bpy.props.BoolProperty(name="Make Vertex Groups", default=False, description="When Apply a Brush to de Object it will create a new vertex group of the new faces" )
    make_boundary = bpy.props.BoolProperty(name="Make Boundary", default=False, description="When Apply a Brush to de Object it will create a new vertex group of the bondary boolean area")
    use_wire = bpy.props.BoolProperty(name="Use Bmesh", default=False, description="Use The Wireframe Instead Of Boolean")
   

    tab_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_history_menu = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='off', update = update_display_tools)


    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            row = layout.row()
            row.label(text="Welcome to T+ Boolean!")

            row = layout.column()
            row.label(text="This is custom version of different boolean addons.")
            row.label(text="It allows you to boolean more directly.")
            row.label(text="If needed can enabel or disable Brush Boolean: as Panel, in Menu and with HotKeys.")
            row.label(text="Also choose between toolshelf [T] or property shelf [N].")
            row.label(text="Have Fun! ;)")

        #Tools
        if self.prefs_tabs == 'toolset':
          
            box = layout.box().column(1)

            row = box.row(1)                            
            row.prop(self, 'tab_history', expand=True)

            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 
            

        #Location
        if self.prefs_tabs == 'location':
            box = layout.box().column(1)
             
            row = box.row(1)  
            row.label("Location Direct Boolean: ")
            
            row= box.row(1)
            row.prop(self, 'tab_location', expand=True)
                                   
            if self.tab_location == 'tools':
                
                box.separator()
                
                row = box.row(1)                                                
                row.prop(self, "tools_category")

            box = layout.box().column(1)
             
            row = box.row(1)  
            row.label("Location Brush Boolean: ")
            
            row= box.row(1)
            row.prop(self, 'tab_location_brush', expand=True)
                       
            if self.tab_location_brush == 'tools':
                
                box.separator()
                
                row = box.row(1)                
                row.prop(self, "tools_category_brush")
                
            if self.tab_location_brush == 'off':                

                row = box.row()
                row.label(text="! keys hidden with next reboot !", icon ="INFO")

            row = layout.row()
            row.label(text="! please reboot blender after changing the panel location !", icon ="INFO")


        #Keys
        if self.prefs_tabs == 'keys':
            box = layout.box().column(1)
             
            row = box.column(1)  
            
            row.label("Experimental Features:")
            
            row.separator()
                       
            row.prop(self, "fast_transform")
            row.prop(self, "use_wire", text="Use Wire Instead Of Bbox")

            box = layout.box().column(1)
             
            row = box.column(1)  
            row.label("Boolean Menu:", icon ="COLLAPSEMENU") 
            
            row.separator()           
            row.label("Menu: SHIF+T")

            row = box.row(1)          
            row.prop(self, 'tab_menu_view', expand=True)

            if self.tab_menu_view == 'off':

                row = box.row(1) 
                row.label(text="! menu hidden with next reboot durably!", icon ="INFO")

            box.separator() 
        
            row.prop(self, 'tab_history_menu', expand=True)


            box = layout.box().column(1)
             
            row = box.column(1)              
            row.label("Direct Operators:", icon ="MOD_WIREFRAME")
            
            row.separator()
            
            row.label("Direct_Union: 'NUMPAD_PLUS', 'PRESS', ctrl=True")
            row.label("Direct_Difference: 'NUMPAD_MINUS', 'PRESS', ctrl=True")
            row.label("Direct_Intersect: 'NUMPAD_ASTERIX', 'PRESS', ctrl=True")
            row.label("Direct_Slice: 'NUMPAD_SLASH', 'PRESS', ctrl=True")
            
            row.separator()
            
            row.label("Editmode:")
            row.separator()

            row.label("Direct_Union: 'NUMPAD_PLUS', 'PRESS', shift=True")
            row.label("Direct_Difference: 'NUMPAD_MINUS', 'PRESS', shift=True")
            row.label("Direct_Intersect: 'NUMPAD_ASTERIX', 'PRESS', shift=True")
            row.label("Direct_Slice: 'NUMPAD_SLASH', 'PRESS', shift=True")

            box = layout.box().column(1)
             
            row = box.column(1)              
            row.label("Brush Operators:", icon ="MOD_MESHDEFORM")
                                   
            row.separator()
            
            row.label("Union: 'NUMPAD_PLUS', 'PRESS', ctrl=True, shift=True")
            row.label("Diff: 'NUMPAD_MINUS', 'PRESS', ctrl=True, shift=True")
            row.label("Intersect: 'NUMPAD_ASTERIX', 'PRESS', ctrl=True, shift=True")
            row.label("Slice Rebool: 'NUMPAD_SLASH', 'PRESS', ctrl=True, shift=True")
          
            row.separator()
            
            row.label("BTool_BrushToMesh: 'NUMPAD_ENTER', 'PRESS', ctrl=True")
            row.label("BTool_AllBrushToMesh: 'NUMPAD_ENTER', 'PRESS', ctrl=True, shift=True")

            box.separator() 
            
            box = layout.box().column(1)
             
            row = box.column(1)               
            row.operator('wm.url_open', text = 'recommended: is key free addon', icon = 'PLUGIN').url = "https://github.com/Antonioya/blender/tree/master/iskeyfree"

            box.separator() 
            
            row = layout.row(1) 
            row.label(text="! if needed change keys durably in TAB Input !", icon ="INFO")



        #Weblinks
        if self.prefs_tabs == 'url':
            row = layout.row()
            row.operator('wm.url_open', text = 'Booltron', icon = 'HELP').url = "https://github.com/mrachinskiy/blender-addon-booltron"
            row.operator('wm.url_open', text = 'BoolTools', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/BoolTool"
            row.operator('wm.url_open', text = 'Boolean 2D Union', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?338703-Addon-Boolean-2D-Union"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?410098-Addon-T-Boolean&p=3118012#post3118012"




def draw_boolean_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)

        if context.mode == "OBJECT":

            box = layout.box().column(1)                     

            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("Direct Boolean", icon ="MOD_WIREFRAME") 

            box.separator()         
            
            row = box.row(1)   
            row.operator("btool.direct_union", text="Union")
            row.operator("btool.direct_intersect", text="Intersect")

            row = box.row(1)              
            row.operator("btool.direct_subtract")              
            row.operator("btool.direct_difference", text="Different")
                        
            box.separator()         
            
            row = box.row(1)   
            row.operator("object.origin_set", "", icon ="LAYER_ACTIVE").type='ORIGIN_GEOMETRY'
            row.operator("btool.direct_slice", "Slice Rebool from Active")

            box.separator()         
  


        if context.mode == "EDIT_MESH":


            box = layout.box().column(1)                     

            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("Direct Boolean", icon ="MOD_WIREFRAME") 
           
            box.separator()         
            
            row = box.row(1)                        
            row.operator("tp_ops.bool_union", text="Union") 
            row.operator("tp_ops.bool_intersect",text="Intersect") 
            row.operator("tp_ops.bool_different",text="Different")  

            box.separator()  

            box = layout.box().column(1)                     

            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("2d Union", icon="MOD_ARRAY") 

            box.separator()   
            
            row = box.row(1) 
            row.operator("bpt.boolean_2d_union", text= "Merge coplanar Faces", icon="AUTOMERGE_ON")        
                   
            box.separator()

            box = layout.box().column(1)                     

            row = box.row(1)              
            row.alignment = 'CENTER'
            row.label("Intersection Knife", icon ="MOD_DECIM")                                  
            
            box.separator()  
                     
            row = box.row(1)    
            row.label("select / unselect")                                           
            
            row = box.row(1)  
            row.operator("mesh.intersect", "Union", icon='ZOOMIN').use_separate = False
            row.operator("mesh.intersect", "Separate", icon='ZOOMOUT').use_separate = True   
            
            box.separator()          
            
            row = box.row(1)           
            row.label("Add Planes")         

            row = box.row(1)   
            row.operator("tp_ops.plane_x",text="X Axis")      
            row.operator("tp_ops.plane_y",text="Y Axis")       
            row.operator("tp_ops.plane_z",text="Z Axis") 

            box.separator()          
            
            row = box.row(1)           
            row.label("Optimize")         

            row = box.column(1)  
            row.operator("mesh.select_linked",text="Select Linked", icon="EDIT")
            row.operator("mesh.remove_doubles",text="Remove Doubles", icon="PANEL_CLOSE")             
            row.operator("mesh.normals_make_consistent", text="Recalc. Normals", icon="SNAP_NORMAL")
            row.operator("tp_ops.origin_edm",text="Origin 2 Selected", icon="LAYER_ACTIVE")

            ###
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
            
            



class VIEW3D_TP_Edit_Boolean_Panel_TOOLS(bpy.types.Panel):
    bl_category = "T+"
    bl_idname = "VIEW3D_TP_Edit_Boolean_Panel_TOOLS"
    bl_label = "Boolean"
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
        return (isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_boolean_panel_layout(self, context, layout) 
        
                

class VIEW3D_TP_Edit_Boolean_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Edit_Boolean_Panel_UI"
    bl_label = "Boolean"
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
        return (isModelingMode)
    
    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_boolean_panel_layout(self, context, layout) 


# Hide boolean objects
def update_BoolHide(self, context):
    ao = context.scene.objects.active
    objs = [i.object for i in ao.modifiers if i.type == 'BOOLEAN']
    hide_state = context.scene.BoolHide

    for o in objs:
        o.hide = hide_state

# Object is a Canvas
def isCanvas(_obj):
    try:
        if _obj["BoolToolRoot"]:
            return True
    except:
        return False


# Object is a Brush Tool Bool
def isBrush(_obj):
    try:
        if _obj["BoolToolBrush"]:
            return True
    except:
        return False

# 3Dview Header Menu
class BoolTool_Menu(bpy.types.Menu):
    bl_label = "TP Boolean :)"
    bl_idname = "OBJECT_MT_BoolTool_Menu"

    def draw(self, context):
        layout = self.layout

        if context.mode == 'OBJECT':
                
            layout.operator("btool.direct_union", icon="ROTATECOLLECTION")
            layout.operator("btool.direct_difference", icon="ROTACTIVE")
            layout.operator("btool.direct_intersect",text="Intersection", icon="ROTATECENTER")
            
            layout.separator()

            layout.operator("btool.direct_subtract", icon="ROTACTIVE")
            layout.operator("btool.direct_slice", text="Slice Rebool", icon="ROTATECENTER")


            active_brush = context.user_preferences.addons[__name__].preferences.tab_location_brush 
            if active_brush == 'tools' or active_brush == 'ui':

                layout.separator()

                layout.operator("btool.boolean_union", icon="ROTATECOLLECTION")
                layout.operator("btool.boolean_diff", icon="ROTACTIVE")
                layout.operator("btool.boolean_inters", icon="ROTATECENTER")
            
                layout.separator()

                layout.operator("btool.boolean_slice", text="Brush Slice Rebool", icon="ROTATECENTER")

                layout.separator()
                layout.operator_context = 'INVOKE_REGION_WIN'
                #layout.operator_context = 'EXEC_REGION_WIN'
                layout.operator("btool.draw_polybrush", icon="LINE_DATA")

                if (isCanvas(context.active_object)):
                    layout.separator()
                    layout.operator("btool.to_mesh", icon="MOD_LATTICE", text="Apply All")
                    Rem = layout.operator("btool.remove", icon="CANCEL", text="Remove All")
                    Rem.thisObj = ""
                    Rem.Prop = "CANVAS"

                if (isBrush(context.active_object)):
                    layout.separator()
                    layout.operator("btool.brush_to_mesh", icon="MOD_LATTICE", text="Apply Brush")
                    Rem = layout.operator("btool.remove", icon="CANCEL", text="Remove Brush")
                    Rem.thisObj = ""
                    Rem.Prop = "BRUSH"

            else:
                pass

            layout.separator()
            layout.operator("object.origin_set", text="Origin 2 Geometry", icon ="LAYER_ACTIVE").type='ORIGIN_GEOMETRY'
            

        if context.mode == 'EDIT_MESH':
                      
            layout.operator("tp_ops.bool_union", text="Union", icon="ROTATECOLLECTION") 
            layout.operator("tp_ops.bool_different",text="Different", icon="ROTACTIVE")  
            layout.operator("tp_ops.bool_intersect",text="Intersection", icon="ROTATECENTER") 

            layout.separator()  
           
            layout.operator("bpt.boolean_2d_union", text= "2d Union Faces", icon='MOD_ARRAY')        
                   
            layout.separator()
                                
            layout.operator("mesh.intersect", "Intersec Union", icon='ZOOMIN').use_separate = False
            layout.operator("mesh.intersect", "Intersec Separate", icon='ZOOMOUT').use_separate = True   
            
            layout.menu("tp_menu.intersetion_planes", icon ="MOD_WIREFRAME")      

            layout.separator()          

            layout.operator("mesh.select_linked",text="Select Linked", icon ="EDIT")
            layout.operator("mesh.remove_doubles",text="Remove Doubles", icon ="PANEL_CLOSE")
            layout.operator("mesh.normals_make_consistent", text="Recalc. Normals", icon="SNAP_NORMAL")
           
            layout.separator()          

            layout.operator("tp_ops.origin_edm",text="Origin 2 Selected", icon ="LAYER_ACTIVE")


        Display_History = context.user_preferences.addons[__name__].preferences.tab_history_menu 
        if Display_History == 'on':
            
            layout.separator() 
                   
            layout.operator("ed.undo", text=" ", icon="LOOP_BACK")
            layout.operator("ed.redo", text=" ", icon="LOOP_FORWARDS") 
            
        else:
            pass
        
        
        
# register Keymaps
addon_keymaps = []
addon_keymapsFastT = []

# booltool: Fast Transform HotKeys Register
def RegisterFastT():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(BTool_FastTransform.bl_idname, 'G', 'PRESS')
    kmi.properties.operator = "Translate"
    addon_keymapsFastT.append((km, kmi))

    kmi = km.keymap_items.new(BTool_FastTransform.bl_idname, 'R', 'PRESS')
    kmi.properties.operator = "Rotate"
    addon_keymapsFastT.append((km, kmi))

    kmi = km.keymap_items.new(BTool_FastTransform.bl_idname, 'S', 'PRESS')
    kmi.properties.operator = "Scale"
    addon_keymapsFastT.append((km, kmi))


# booltool: Fast Transform HotKeys UnRegister
def UnRegisterFastT():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    for km, kmi in addon_keymapsFastT:
        km.keymap_items.remove(kmi)
    addon_keymapsFastT.clear()


# register
import traceback

icon_collections = {}

def register():

    mkb_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mkb_icons.load("my_image1", os.path.join(icons_dir, "icon_image1.png"), 'IMAGE')
    mkb_icons.load("my_image2", os.path.join(icons_dir, "icon_image2.png"), 'IMAGE')

    icon_collections['main'] = mkb_icons

    # booltool: Scene variables
    bpy.types.Scene.BoolHide = bpy.props.BoolProperty(default=False, description='Hide boolean objects', update=update_BoolHide)
    
    # booltool: Handlers
    #bpy.app.handlers.scene_update_post.append(HandleScene)

    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
        
    # booltool: create the booleanhotkey in opjectmode
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')

    # booltool: Direct Operators
    kmi = km.keymap_items.new("btool.direct_union", 'NUMPAD_PLUS', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new("btool.direct_difference", 'NUMPAD_MINUS', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new("btool.direct_intersect", 'NUMPAD_ASTERIX', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new("btool.direct_slice", 'NUMPAD_SLASH', 'PRESS', ctrl=True)
    
    
    # edit: create the boolean menu hotkey in editmode
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh')

    # edit: Direct Operators
    kmi = km.keymap_items.new("tp_ops.bool_union", 'NUMPAD_PLUS', 'PRESS', shift=True)
    kmi = km.keymap_items.new("tp_ops.bool_different", 'NUMPAD_MINUS', 'PRESS', shift=True)
    kmi = km.keymap_items.new("tp_ops.bool_intersect", 'NUMPAD_ASTERIX', 'PRESS', shift=True)
    kmi = km.keymap_items.new("bpt.boolean_2d_union", 'NUMPAD_SLASH', 'PRESS', shift=True)


    #km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    #kmi = km.keymap_items.new('wm.call_menu', 'T', 'PRESS', shift=True) #ctrl=True, alt=True, 
    #kmi.properties.name = 'OBJECT_MT_BoolTool_Menu'


    active_brush = context.user_preferences.addons[__name__].preferences.tab_location_brush 
    if active_brush == 'tools' or active_brush == 'ui':

        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')

        # booltool: Brush Operators
        kmi = km.keymap_items.new("btool.boolean_union", 'NUMPAD_PLUS', 'PRESS', ctrl=True, shift=True)
        kmi = km.keymap_items.new("btool.boolean_diff", 'NUMPAD_MINUS', 'PRESS', ctrl=True, shift=True)
        kmi = km.keymap_items.new("btool.boolean_inters", 'NUMPAD_ASTERIX', 'PRESS', ctrl=True, shift=True)
        kmi = km.keymap_items.new("btool.boolean_slice", 'NUMPAD_SLASH', 'PRESS', ctrl=True, shift=True)

        kmi = km.keymap_items.new("btool.brush_to_mesh", 'NUMPAD_ENTER', 'PRESS', ctrl=True)
        kmi = km.keymap_items.new("btool.to_mesh", 'NUMPAD_ENTER', 'PRESS', ctrl=True, shift=True)



    addon_keymaps.append(km)

    update_menu(None, bpy.context)
    update_panel_position(None, bpy.context)
    update_panel_position_brush(None, bpy.context)



def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    # booltool
    del bpy.types.Scene.BoolHide

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()


    # Keymapping
    # remove keymaps when add-on is deactivated
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del addon_keymaps[:]


if __name__ == "__main__":
    register()
        
        





