bl_info = {
    "name": "TP Scene",
    "author": "Addon Authors (see URL), MKB",
    "version": (0, 1, 3),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf [T] or Property Shelf [N] ",
    "description": "Scene Build Panel",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "ToolPlus"}




#line for the panels
from toolplus_scene.grp_editor_ui import (VIEW3D_TP_Groups_Panel_TOOLS)
from toolplus_scene.grp_editor_ui import (VIEW3D_TP_Groups_Panel_UI)

from toolplus_scene.grp_layers_ui import (VIEW3D_TP_Layers_Panel_TOOLS)
from toolplus_scene.grp_layers_ui import (VIEW3D_TP_Layers_Panel_UI)

from toolplus_scene.grp_rename_ui import (VIEW3D_TP_Rename_Panel_TOOLS)
from toolplus_scene.grp_rename_ui import (VIEW3D_TP_Rename_Panel_UI)


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_scene'))

if "bpy" in locals():
    import imp
    imp.reload(grp_action)
    imp.reload(grp_editor)
    imp.reload(grp_layers)
    imp.reload(grp_rename)
    imp.reload(grp_silhouette)
    imp.reload(grp_smartjoin)
else:
    from . import grp_action
    from . import grp_editor
    from . import grp_layers
    from . import grp_rename
    from . import grp_silhouette
    from . import grp_smartjoin



import bpy
from bpy import*

import bpy.utils.previews
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import* #(StringProperty, BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, IntProperty)

def update_panel_position_group(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Groups_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Groups_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Groups_Panel_UI)

    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_group == 'tools':

        VIEW3D_TP_Groups_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_group
        bpy.utils.register_class(VIEW3D_TP_Groups_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_group == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Groups_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_group == 'off':
        pass


def update_panel_position_layer(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Layers_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Layers_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Layers_Panel_UI)
    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_layer == 'tools':

        VIEW3D_TP_Layers_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_layer
        bpy.utils.register_class(VIEW3D_TP_Layers_Panel_TOOLS)
    
    if context.user_preferences.addons[__name__].preferences.tab_location_layer == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Layers_Panel_UI)

    if context.user_preferences.addons[__name__].preferences.tab_location_layer == 'off':
        pass


def update_panel_position_rename(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Rename_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Rename_Panel_TOOLS)
    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Rename_Panel_UI)

    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location_rename == 'tools':

        VIEW3D_TP_Rename_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category_rename
        bpy.utils.register_class(VIEW3D_TP_Rename_Panel_TOOLS)
    
    elif context.user_preferences.addons[__name__].preferences.tab_location_rename == 'ui':
        bpy.utils.register_class(VIEW3D_TP_Rename_Panel_UI)
  
    elif context.user_preferences.addons[__name__].preferences.tab_location_rename == 'off':
        pass


def update_display_tools(self, context):

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'on':
        return True

    if context.user_preferences.addons[__name__].preferences.tab_display_tools == 'off':
        pass 



#Preferences
class TP_Panels_Preferences(AddonPreferences):
    bl_idname = __name__
    
    prefs_tabs = EnumProperty(
        items=(('info',       "Info",       "Info"),
               ('toolsets',   "Tools",      "Tools"),        
               ('location',   "Location",   "Location"),
               ('url',        "URLs",       "URLs")),
               default='info')

    #Tab Location           
    tab_location_group = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'disable panel in the shelf')),
               default='tools', update = update_panel_position_group)

    tab_location_layer = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'disable panel in the shelf')),
               default='tools', update = update_panel_position_layer)

    tab_location_rename = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf', 'place panel in the tool shelf [T]'),
               ('ui', 'Property Shelf', 'place panel in the property shelf [N]'),
               ('off', 'Off', 'disable panel in the shelf')),
               default='tools', update = update_panel_position_rename)

    #SmartLayer

    tab_move = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Move on', 'enable tools in panel'), ('off', 'Move off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_shade = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'Shade on', 'enable tools in panel'), ('off', 'Shade off', 'disable tools in panel')), default='on', update = update_display_tools)

    tab_history = EnumProperty(name = 'Display Tools', description = 'on / off',
                  items=(('on', 'History on', 'enable tools in panel'), ('off', 'History off', 'disable tools in panel')), default='on', update = update_display_tools)


    tools_category_group = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_group)
    tools_category_layer = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_layer)
    tools_category_rename = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'T+', update = update_panel_position_rename)


    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)
       
        if self.prefs_tabs == 'info':
            row = layout.row()
            row.label(text="Welcome to T+ Scene!")

            row = layout.column()
            row.label(text="This custom setup helps to build a scene easier.")
            row.label(text="Includes grouping, layering & renaming tools in separate panels.")
            row.label(text="Have Fun! :) ")


        #Tools
        if self.prefs_tabs == 'toolsets':
          
            box = layout.box().column(1)

            row = box.row()
            row.label("Panel: SmartLayer")            
            
            row = box.row()
            row.prop(self, 'tab_move', expand=True)
            row.prop(self, 'tab_shade', expand=True)

            row = box.row()
            row.label("Panel: ReNamer")            
            
            row = box.row()            
            row.prop(self, 'tab_history', expand=True)
            
            box.separator()       
            
            row = layout.row()
            row.label(text="! save user settings for permant on/off !", icon ="INFO")

            box.separator() 

    
        #Location
        if self.prefs_tabs == 'location':

            box = layout.box().column(1) 
            
            row = box.row(1) 
            row.label("Location GroupEditor: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_group', expand=True)

            if self.tab_location_group == 'tools':
                
                row = box.row()
                row.prop(self, "tools_category_group")               
            
            box.separator()
        
            box = layout.box().column(1) 

            row = box.row(1) 
            row.label("Location Layers: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_layer', expand=True)
            if self.tab_location_layer == 'tools':

                row = box.row()                
                row.prop(self, "tools_category_layer")
                            
            box.separator()
        
            box = layout.box().column(1) 

            row = box.row(1) 
            row.label("Location Rename: ")
            
            box.separator()

            row = box.row(1) 
            row.prop(self, 'tab_location_rename', expand=True)            
            if self.tab_location_rename == 'tools':   

                row = box.row()                
                row.prop(self, "tools_category_rename")
            
            box.separator()
            
            box = layout.box().column(1) 

            row = box.row(1)            
            row.label(text="...please reboot blender after changing the locations...", icon ="INFO")
            
            box.separator()
            

        #Weblinks
        if self.prefs_tabs == 'url':
            row = layout.row(1)

            row = layout.row() 
            row.operator('wm.url_open', text = 'Renaming Objects', icon = 'CLIP').url = "https://www.youtube.com/watch?v=ztnfo6eKtL8"
            row.operator('wm.url_open', text = 'Group Editor', icon = 'HELP').url = "http://blenderaddonlist.blogspot.de/2013/11/addon-group-editor.html"
            row.operator('wm.url_open', text = 'Display Layers', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?388166-Addon-Display-Layers-(unlimited)&highlight="
            row.operator('wm.url_open', text = 'Silhoutte', icon = 'HELP').url = "https://github.com/Antonioya/blender/tree/master/silhoutte"
            row.operator('wm.url_open', text = 'Thread', icon = 'BLENDER').url = "https://blenderartists.org/forum/showthread.php?409425-Addon-T-Scene&highlight="




#Property


# GroupEditor
class GroupList(bpy.types.PropertyGroup):
    pass

class GroupObjectList(bpy.types.PropertyGroup):
    pass



# Layers
def display_toggle_callback(self, context):
    apply_layer_settings(context)

class property_collection_display_layers(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Layer name", default="Layer"),
    display = bpy.props.BoolProperty(name="Display", default=True, update=display_toggle_callback)
    select = bpy.props.BoolProperty(name="Select", default=True, update=display_toggle_callback)
    render = bpy.props.BoolProperty(name="Render", default=True, update=display_toggle_callback)
    wire = bpy.props.BoolProperty(name="Wire", default=False, update=display_toggle_callback)
        
class multilight_properties(bpy.types.PropertyGroup):
    
    bpy.types.Object.display_layer = bpy.props.IntProperty(
        name = "Layer ID",
        description = "",
        default = 0,
        min = 0,
        update = display_toggle_callback
    )
    
    bpy.types.Object.use_display_layer = bpy.props.BoolProperty(
        name = "Use Layer",
        description = "",
        default = 0,
        update = display_toggle_callback
    )
    
    bpy.types.Scene.display_layers_collection_index = bpy.props.IntProperty(
        name = "Layer Scene Index",
        description = "---",
        default = 0,
        min = 0,
    )


def apply_layer_settings(context):

    for obj in context.scene.objects:
        if obj.use_display_layer:

            layer = context.scene.display_layers_collection[obj.display_layer]

            if layer.display:
                obj.hide = False
            else:
                obj.hide = True

            if layer.select:
                obj.hide_select = False
            else:
                obj.hide_select = True

            if layer.render:
                obj.hide_render = False
            else:
                obj.hide_render = True

            if layer.wire:
                obj.show_wire = True
                obj.show_all_edges = True
            else:
                obj.show_wire = False
                obj.show_all_edges = False

#layers
class layers_select_objects(bpy.types.Operator):
    bl_idname = "select_objects.btn"
    bl_label = "Select"
    bl_description = "Select objects"

    @classmethod
    def poll(cls, context):
        return context.object and context.scene.display_layers_collection.items()

    def execute(self, context):
        active_layer_index = context.scene.display_layers_collection_index

        for obj in context.scene.objects:
            if obj.use_display_layer and obj.display_layer == active_layer_index:
                obj.select = True
                obj.select = True

        return{'FINISHED'}



def tp_load_copy_to_meshdata(self,context):
    layout = self.layout
    
    col = layout.row(1)
    col.operator("tp_ops.copy_name_to_meshdata", text= "", icon ="PASTEDOWN")
    col.operator("tp_ops.copy_data_name_to_object", text= "", icon ="COPYDOWN")



# registration
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
        
    #panels
    update_panel_position_group(None, bpy.context)
    update_panel_position_layer(None, bpy.context)
    update_panel_position_rename(None, bpy.context)

    #outliner header
    bpy.types.OUTLINER_HT_header.prepend(tp_load_copy_to_meshdata)    

    #rename
    bpy.types.Scene.rno_list_selection_ordered = bpy.props.EnumProperty(name="selection orderer", items=[])    
    bpy.types.Scene.rno_str_new_name = bpy.props.StringProperty(name="New name", default='')
    bpy.types.Scene.rno_str_old_string = bpy.props.StringProperty(name="Old string", default='')
    bpy.types.Scene.rno_str_new_string = bpy.props.StringProperty(name="New string", default='')
    bpy.types.Scene.rno_str_numFrom = bpy.props.StringProperty(name="from", default='')
    bpy.types.Scene.rno_str_prefix = bpy.props.StringProperty(name="Prefix", default='')
    bpy.types.Scene.rno_str_subfix = bpy.props.StringProperty(name="Subfix", default='')    
    bpy.types.Scene.rno_bool_numbered = bpy.props.BoolProperty(name='numbered', default=True)
    bpy.types.Scene.rno_bool_keepOrder = bpy.props.BoolProperty(name='keep selection order')
    bpy.types.Scene.rno_bool_keepIndex = bpy.props.BoolProperty(name='keep object Index', default=True)


    #group editor
    bpy.types.Scene.hk_group_list = bpy.props.CollectionProperty(type=GroupList)
    bpy.types.Scene.hk_group_list_index = bpy.props.IntProperty()
    bpy.types.Scene.hk_group_name_txt = bpy.props.StringProperty(name="")
    bpy.types.Scene.hk_group_object_list = bpy.props.CollectionProperty(type=GroupObjectList)
    bpy.types.Scene.hk_group_object_list_index = bpy.props.IntProperty() 



    #layer
    bpy.types.Scene.display_layers_collection = bpy.props.CollectionProperty(type=property_collection_display_layers)
    bpy.types.Scene.display_layers_collection_index = bpy.props.IntProperty(name = "Layer Scene Index", description = "---", default = 0, min = 0)


    #smartjoin
    bpy.types.Mesh.is_sjoin = BoolProperty(default=False)
    bpy.types.Mesh.sjoin_link_name = StringProperty()
    bpy.types.Mesh.expanded_obj = StringProperty()
    bpy.types.Object.sjoin_mesh = StringProperty(default = '')

    #silhoutte
    bpy.types.Scene.silhoutte_formula = bpy.props.StringProperty(name="Formula", maxlen=512)


def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    #outliner header
    bpy.types.OUTLINER_HT_header.remove(tp_load_copy_to_meshdata)  
 
    #rename    
    del bpy.types.Scene.rno_str_new_name
    del bpy.types.Scene.rno_str_old_string
    del bpy.types.Scene.rno_str_new_string
    del bpy.types.Scene.rno_bool_keepOrder
    del bpy.types.Scene.rno_bool_numbered
    del bpy.types.Scene.rno_list_selection_ordered
    del bpy.types.Scene.rno_str_prefix
    del bpy.types.Scene.rno_str_subfix
    del bpy.types.Scene.rno_bool_keepIndex 


    #layer    
    del bpy.types.Scene.display_layers_collection
    del bpy.types.Scene.display_layers_collection_index  


    #smartjoin
    del bpy.types.Mesh.is_sjoin
    del bpy.types.Object.sjoin_mesh

    #silhoutte
    del bpy.types.Scene.silhoutte_formula

    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    

if __name__ == "__main__":
    register()
        
        
                   





