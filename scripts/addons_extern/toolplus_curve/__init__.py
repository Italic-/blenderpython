# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# Contributed to by
# testscreenings, Alejandro Omar Chocano Vasquez, Jimmy Hazevoet, Adam Newgas, meta-androcto, 
# MarvinkBreuer (MKB)

bl_info = {
    "name": "TP Add Curve Objects",
    "author": "Multiple Authors / Enhanced Addon Factory",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "View3D > Add > Curve",
    "description": "Add extra curve object types",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/Curve/Curve_Objects",
    "category": "ToolPlus"}


from .object_tube_and_pipe import __init__
from .object_tube_and_pipe import Makemesh
from .object_tube_and_pipe import Pipe
from .object_tube_and_pipe import Tube


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'toolplus_curve'))


if "bpy" in locals():
    
    import importlib    

    importlib.reload(sapling)
    importlib.reload(add_curve_aceous_galore)
    importlib.reload(add_curve_beveled)
    importlib.reload(add_curve_spirals)
    importlib.reload(add_curve_taper)
    importlib.reload(add_curve_torus_knots)
    importlib.reload(add_curve_braid)
    importlib.reload(add_curve_curly)
    importlib.reload(add_curve_celtic_links)
    importlib.reload(add_curve_formulacurves)
    importlib.reload(add_curve_tubetool)
    importlib.reload(add_curve_wires)
    importlib.reload(add_curve_ivygen)
    importlib.reload(curve_action)
    importlib.reload(curve_beveltaper)
    importlib.reload(curve_extend)
    importlib.reload(curve_outline)
    importlib.reload(curve_simplify)
    importlib.reload(curve_split)
    importlib.reload(curve_trim)
    importlib.reload(add_surface_plane_cone)
    importlib.reload(DialScale)
    importlib.reload(add_iterative_tree)
    importlib.reload(add_simple_curve)    
    
    print("Reloaded multifiles")

else:

    from . import sapling
    from . import add_curve_aceous_galore
    from . import add_curve_beveled
    from . import add_curve_spirals
    from . import add_curve_taper
    from . import add_curve_torus_knots
    from . import add_curve_braid
    from . import add_curve_curly
    from . import add_curve_celtic_links
    from . import add_curve_formulacurves
    from . import add_curve_tubetool
    from . import add_curve_wires
    from . import add_curve_ivygen
    from . import curve_action
    from . import curve_beveltaper
    from . import curve_extend
    from . import curve_outline
    from . import curve_simplify
    from . import curve_split
    from . import curve_trim
    from . import add_surface_plane_cone
    from . import DialScale
    from . import add_iterative_tree
    from . import add_simple_curve


    print("Imported multifiles")



import add_simple_curve
import add_curve_beveled
import curve_action

import bpy
from bpy import*
from bpy.props import* 
from bpy.types import AddonPreferences, PropertyGroup



# Panel Position #####################################

def update_panel_position(self, context):
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Add_Curve_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Info_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Edit_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Bevel_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Tools_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Utility_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Set_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Taper_Curve_Panel_UI)
        
        bpy.utils.unregister_class(VIEW3D_TP_Add_Curve_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Info_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Edit_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Bevel_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Tools_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Utility_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Set_Panel_TOOLS)
        bpy.utils.unregister_class(VIEW3D_TP_Taper_Curve_Panel_TOOLS)

    except:
        pass
    
    try:
        bpy.utils.unregister_class(VIEW3D_TP_Add_Curve_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Info_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Edit_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Bevel_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Tools_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Utility_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Curve_Set_Panel_UI)
        bpy.utils.unregister_class(VIEW3D_TP_Taper_Curve_Panel_UI)

    except:
        pass
    
    if context.user_preferences.addons[__name__].preferences.tab_location == 'tools':

        VIEW3D_TP_Add_Curve_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Info_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Edit_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Bevel_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Tools_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Utility_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Curve_Set_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category
        VIEW3D_TP_Taper_Curve_Panel_TOOLS.bl_category = context.user_preferences.addons[__name__].preferences.tools_category

        bpy.utils.register_class(VIEW3D_TP_Add_Curve_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Info_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Edit_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Bevel_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Tools_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Utility_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Curve_Set_Panel_TOOLS)
        bpy.utils.register_class(VIEW3D_TP_Taper_Curve_Panel_TOOLS)
    
    else:
        bpy.utils.register_class(VIEW3D_TP_Add_Curve_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Info_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Edit_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Bevel_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Tools_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Utility_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Curve_Set_Panel_UI)
        bpy.utils.register_class(VIEW3D_TP_Taper_Curve_Panel_UI)




# AddonPreferences #####################################

class TP_Panels_Preferences(AddonPreferences):
    bl_idname = __name__
    
    prefs_tabs = EnumProperty(
        items=(('info',       "Info",       "Info"),
               ('include',    "Include",    "Include"),
               ('location',   "Location",   "Location"),
               ('url',        "URLs",       "URLs")),
               default='info')

    #Tab Location           
    tab_location = EnumProperty(
        name = 'Panel Location',
        description = 'save user settings and restart blender after switching the panel location',
        items=(('tools', 'Tool Shelf [T]', 'place panel in the 3d view tool shelf [T]'),
               ('ui', 'Property Shelf [N]', 'place panel in the  3d view property shelf [N]')),
               default='tools', update = update_panel_position)

    tools_category = StringProperty(name = "TAB Category", description = "add name for a new category tab", default = 'Curves', update = update_panel_position)


    def draw(self, context):
        layout = self.layout
        
        #Info
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)        

        if self.prefs_tabs == 'info':

            layout.label(text="Welcome to enhanced Addon Curve Factory")
            layout.label(text="Add Curve and Surface Objects")
            layout.label(text="Merges most Curve Object Addons into One")

        #Include
        if self.prefs_tabs == 'include':

            layout.label(text="Simple Curves: simple 2d curve shapes")
            layout.label(text="Add Plants: Sapling & Ivy Gen, Add Iterative Tree(panel)")
            layout.label(text="Add Knots: Celtic, TorusKnot+ & Braid")
            layout.label(text="Curves_Galore: 2d curve shapes")
            layout.label(text="Spirals: Create Spiral curve type")
            layout.label(text="Curly Curve: Florishes & Curls")
            layout.label(text="Formular Curve: Math based curve")
            layout.label(text="Curve Wires: String a wire between 2 objects")
            layout.label(text="Dial Scale: Clock Face or Scale")
            layout.label(text="Curve Simplify: Simplify Curves")
            layout.label(text="Tubes & Pipes: Create Solid Tubes & Pipes(panel)")
            layout.label(text="TubeTool: add Curve-Tube beetween two selected faces")
            layout.label(text="Bevel Taper Curve: Add Taper to Curves for Bevel")
            layout.label(text="Bevel Curve: Add Curves with Bevel")


        #Location
        if self.prefs_tabs == 'location':
            
            row = layout.row()
            row.separator()
            
            row = layout.row()
            row.label("Location: ")
            
            row= layout.row(align=True)
            row.prop(self, 'tab_location', expand=True)

            row = layout.row()            
            if self.tab_location == 'tools':
                row.prop(self, "tools_category")

            row = layout.row()
            row.label(text="please reboot blender after changing the panel location")


        #Weblinks
        if self.prefs_tabs == 'url':
            
            row = layout.column_flow(2)             
            row.operator('wm.url_open', text = 'Curve Objects', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Curve_Objects"
            row.operator('wm.url_open', text = 'Curves Galore', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Curves_Galore"
            row.operator('wm.url_open', text = 'Curve Simplify', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Curve_Simplify"
            row.operator('wm.url_open', text = 'Simple Curves', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Simple_curves"
            row.operator('wm.url_open', text = 'Curly Curves', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Curly_Curves"
            row.operator('wm.url_open', text = 'Torus Knot', icon = 'HELP').url = "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Torus_Knot"
            row.operator('wm.url_open', text = 'Sampling Tree', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Sapling_Tree"
            row.operator('wm.url_open', text = 'Taper Curve', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Bevel_-Taper_Curve"
            row.operator('wm.url_open', text = 'Ivy', icon = 'HELP').url = "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Ivy_Gen"
            row.operator('wm.url_open', text = 'Curve Tools', icon = 'HELP').url = "https://blenderartists.org/forum/showthread.php?221213-Tools-for-curves"




# Panels ###############################################            
  

def draw_add_curve_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)

        if context.mode == "OBJECT":

            """ Add Curve """
            box = layout.box().column(1)       
           
            row = box.row(1) 
            row.label(text="Curve / Nurbs:")
   
            row = box.row(1) 
            row.operator("curve.primitive_bezier_curve_add",icon='CURVE_BEZCURVE',text="")
            row.operator("curve.primitive_bezier_circle_add",icon='CURVE_BEZCIRCLE',text="")
            row.operator("curve.primitive_nurbs_curve_add",icon='CURVE_NCURVE',text="")
            row.operator("curve.primitive_nurbs_circle_add",icon='CURVE_NCIRCLE',text="")
            row.operator("curve.primitive_nurbs_path_add",icon='CURVE_PATH',text="")
            row.operator("curve.draw", icon='LINE_DATA',text="")
            
            box.separator()


            """ Add Surface """
            
            box = layout.box().column(1)       
            
            row = box.row(1) 
            row.label(text="Surface:")    
      
            row = box.row(1) 
            row.operator("surface.primitive_nurbs_surface_circle_add",icon='SURFACE_NCIRCLE',text="")
            row.operator("surface.primitive_nurbs_surface_surface_add",icon='SURFACE_NSURFACE',text="")
            row.operator("surface.primitive_nurbs_surface_cylinder_add",icon='SURFACE_NCYLINDER',text="")
            row.operator("surface.primitive_nurbs_surface_sphere_add",icon='SURFACE_NSPHERE',text="")
            row.operator("surface.primitive_nurbs_surface_torus_add",icon='SURFACE_NTORUS',text="")

            box.separator()


            box = layout.box().column(1)                         

            row = box.row(1)
            row.label("2d Curves")
                    
            row = box.row(1)
            row.operator("curve.simple", text="Point", icon_value=my_button_one.icon_id).Simple_Type="Point"
            row.operator("curve.simple", text="Line", icon_value=my_button_one.icon_id).Simple_Type="Line"
            
            row = box.row(1)
            row.operator("curve.simple", text="Distance", icon_value=my_button_one.icon_id).Simple_Type="Distance"        
            row.operator("curve.simple", text="Angle", icon_value=my_button_one.icon_id).Simple_Type="Angle"        

            row = box.row(1)        
            row.operator("curve.simple", text="Circle", icon_value=my_button_one.icon_id).Simple_Type="Circle"        
            row.operator("curve.simple", text="Ellipse", icon_value=my_button_one.icon_id).Simple_Type="Ellipse"

            row = box.row(1)
            row.operator("curve.simple", text="Arc", icon_value=my_button_one.icon_id).Simple_Type="Arc"       
            row.operator("curve.simple", text="Sector", icon_value=my_button_one.icon_id).Simple_Type="Sector"

            row = box.row(1)
            row.operator("curve.simple", text="Segment", icon_value=my_button_one.icon_id).Simple_Type="Segment"        
            row.operator("curve.simple", text="Rectangle", icon_value=my_button_one.icon_id).Simple_Type="Rectangle"

            row = box.row(1)
            row.operator("curve.simple", text="Rhomb", icon_value=my_button_one.icon_id).Simple_Type="Rhomb"
            row.operator("curve.simple", text="Polygon", icon_value=my_button_one.icon_id).Simple_Type="Polygon"

            row = box.row(1)
            row.operator("curve.simple", text="Polygon_ab", icon_value=my_button_one.icon_id).Simple_Type="Polygon_ab"
            row.operator("curve.simple", text="Trapezoid", icon_value=my_button_one.icon_id).Simple_Type="Trapezoid"
            
            box.separator() 

            box = layout.box().column(1)                         

            row = box.row(1)
            row.label("Plants Curves")
                    
            row = box.column(1)
            row.operator("curve.tree_add", text="Sapling Tree", icon_value=my_button_one.icon_id)       
            row.operator("curve.ivy_gen", text="Add Ivy to Mesh", icon_value=my_button_one.icon_id).updateIvy = True

            box.separator() 

            box = layout.box().column(1)                         

            row = box.row(1)
            row.label("Knot Curves")
                    
            row = box.column(1)
            row.operator("curve.torus_knot_plus", text="Torus Plus", icon_value=my_button_one.icon_id)
            row.operator("curve.celtic_links", text="Celtic Links", icon_value=my_button_one.icon_id)
            row.operator("mesh.add_braid", text="Braid Knot", icon_value=my_button_one.icon_id)

            box.separator() 

            box = layout.box().column(1)                         

            row = box.row(1)
            row.label("Extra Curves")
                    
            row = box.row(1)
            row.operator("mesh.curveaceous_galore", text="Galore", icon_value=my_button_one.icon_id)
            row.operator("curve.spirals", text="Spirals", icon_value=my_button_one.icon_id)

            row = box.row(1)
            row.operator("curve.curlycurve", text="Curly", icon_value=my_button_one.icon_id)
            row.operator("curve.formulacurves", text="Formula", icon_value=my_button_one.icon_id)

            row = box.row(1)
            row.operator("curve.wires", text="Wires", icon_value=my_button_one.icon_id)
            
            box.separator() 

            box = layout.box().column(1)                         

            row = box.row(1)      
            row.label(text="Curve Utils")

            row = box.column(1)        
            row.operator("curve.simplify", text="Simplify", icon_value=my_button_one.icon_id)
            row.operator("curve.dial_scale", text="Dial / Scale", icon_value=my_button_one.icon_id)

            box.separator() 

            box = layout.box().column(1)                         

            row = box.row(1)      
            row.label(text="Surface Factory")

            row = box.row(1)        
            row.operator("object.add_surface_wedge", text="Wedge", icon_value=my_button_one.icon_id)
            row.operator("object.add_surface_cone", text="Cone", icon_value=my_button_one.icon_id)

            row = box.row(1)             
            row.operator("object.add_surface_star", text="Star", icon_value=my_button_one.icon_id)
            row.operator("object.add_surface_plane", text="Plane", icon_value=my_button_one.icon_id)
            
            row = box.row(1)             
            row.operator("curve.smooth_x_times", text="Special Smooth", icon_value=my_button_one.icon_id)

            box.separator() 


        if context.mode == "EDIT_MESH":

            box = layout.box().column(1)                         

            row = box.row(1)      
            row.label(text="TubeTool")

            row = box.column(1)        
            row.operator("mesh.add_curvebased_tube", text="Add to Faces", icon_value=my_button_one.icon_id)

            box.separator()             



        if context.mode =='EDIT_CURVE':

            box = layout.box() 
            row = box.row(1)         
            row.alignment = 'CENTER'               

            sub = row.row(1)
            sub.scale_x = 1.2      
            sub.operator("curve.primitive_bezier_curve_add",icon='CURVE_BEZCURVE',text="")
            sub.operator("curve.primitive_bezier_circle_add",icon='CURVE_BEZCIRCLE',text="")
            sub.operator("curve.primitive_nurbs_curve_add",icon='CURVE_NCURVE',text="")
            sub.operator("curve.primitive_nurbs_circle_add",icon='CURVE_NCIRCLE',text="")
            sub.operator("curve.primitive_nurbs_path_add",icon='CURVE_PATH',text="")  
            sub.operator("curve.draw", icon='LINE_DATA')

        if context.mode == 'EDIT_SURFACE':
             
            box = layout.box()
            row = box.row(1) 
            row.alignment = 'CENTER'               
            sub = row.row(1)
            sub.scale_x = 1.2   

            sub.operator("surface.primitive_nurbs_surface_curve_add",icon='SURFACE_NCURVE',text="") 
            sub.operator("surface.primitive_nurbs_surface_circle_add",icon='SURFACE_NCIRCLE',text="")
            sub.operator("surface.primitive_nurbs_surface_surface_add",icon='SURFACE_NSURFACE',text="")
            sub.operator("surface.primitive_nurbs_surface_cylinder_add",icon='SURFACE_NCYLINDER',text="")
            sub.operator("surface.primitive_nurbs_surface_sphere_add",icon='SURFACE_NSPHERE',text="")
            sub.operator("surface.primitive_nurbs_surface_torus_add",icon='SURFACE_NTORUS',text="")   



class VIEW3D_TP_Add_Curve_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Add_Curve_Panel_TOOLS"
    bl_label = "Add"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_add_curve_panel_layout(self, context, layout) 



class VIEW3D_TP_Add_Curve_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Add_Curve_Panel_UI"
    bl_label = "Add"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_add_curve_panel_layout(self, context, layout) 



def draw_add_taper_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        my_button_one = icons.get("my_image1")

        if context.mode == "OBJECT":

            box = layout.box().column(1)                         

            row = box.row(1)      
            row.label(text="Taper Bevel")

            row = box.row(1) 
            row.operator("curve.new_beveled_curve", icon_value=my_button_one.icon_id)
            
            row = box.row(1) 
            row.label(text="Edit Bevel:")

            row = box.row(1) 
            row.operator("curve.edit_bevel_curve", text="Edit")
            row.operator("curve.hide_bevel_objects", text="Hide")
            row.operator("curve.add_bevel_to_curve", text="Reset")

            row = box.row(1) 
            row.label(text="Convert to Mesh:")
           
            row = box.row(1)             
            row.operator("curve.convert_beveled_curve_to_meshes", text="Mesh(es)")
            row.operator("curve.convert_beveled_curve_to_separated_meshes", text="Merged")

            row = box.row(1)   
            row.operator("curve.convert_beveled_curve_to_merged_mesh", text="Separated")
            row.operator("curve.convert_beveled_curve_to_union_mesh", text="Union")

            box.separator()


        if context.mode =='EDIT_CURVE':
            
            box = layout.box().column(1)                         

            row = box.row(1)      
            row.label(text="Taper Bevel")

            row = box.row(1) 
            row.operator("curve.finish_edit_bevel")
            row.operator("tp_ops.wire_all", text="", icon='WIRE')
           
            box.separator()



class VIEW3D_TP_Taper_Curve_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Taper_Curve_Panel_TOOLS"
    bl_label = "Taper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_add_taper_panel_layout(self, context, layout) 



class VIEW3D_TP_Taper_Curve_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Taper_Curve_Panel_UI"
    bl_label = "Taper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column_flow(1)  
        layout.operator_context = 'INVOKE_REGION_WIN'

        draw_add_taper_panel_layout(self, context, layout) 





def draw_curve_info_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)          
        box = layout.box().column(1)         
            
        box.separator()         
         
        row = box.row(1)
        row.prop(context.active_object, "name", text="")        
        
        box.separator()  
               
        row = box.row(1)
        sub = row.row(1)
        sub.scale_x = 0.25           
        sub.prop(context.object.data, "dimensions", expand=True)
    
        box.separator() 

        if context.mode == 'EDIT_CURVE':
                             
            row = box.row(1)
            row.operator("curvetools2.operatorcurveinfo", text = "Curve")                        
            row.operator("curvetools2.operatorsplinesinfo", text = "Splines")
            row.operator("curvetools2.operatorsegmentsinfo", text = "Segments")
             
        row = box.row(1) 
        row.operator("curvetools2.operatorselectioninfo", text = "Selection Info:")
        row.prop(context.scene.curvetools, "NrSelectedObjects", text = "")   


        if context.mode == 'EDIT_CURVE':

            row = box.row(1) 
            row.operator("curvetools2.operatorcurvelength", text = "Calc Length")
            row.prop(context.scene.curvetools, "CurveLength", text = "")    

        ###
        box.separator() 



class VIEW3D_TP_Curve_Info_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Info_Panel_TOOLS"
    bl_label = "Info"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'
         
         draw_curve_info_panel_layout(self, context, layout)


         
class VIEW3D_TP_Curve_Info_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Curve_Info_Panel_UI"
    bl_label = "Info"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_info_panel_layout(self, context, layout)                                     






def draw_curve_edit_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)          
        
        if context.mode == 'EDIT_CURVE':
            
             box = layout.box().column(1) 

             row = box.column(1)
             #row.alignment = 'CENTER'  
             row.label("Set Spline Type", icon="IPO_BEZIER") 
             
             box.separator()
                       
             row = box.row(1)  
             row.operator("curve.spline_type_set", "Poly").type = 'POLY'   
             row.operator("curve.spline_type_set", "Bezier").type = 'BEZIER'   
             row.operator("curve.spline_type_set", "Nurbs").type = 'NURBS'   

             box.separator()   

             box = layout.box().column(1)
     
             row = box.row(1)
             #row.alignment = 'CENTER'  
             row.label("Curve Handle Type", icon='IPO_BEZIER') 

             box.separator() 
                     
             row = box.row(1)   
             row.operator("curve.handle_type_set", text="Auto", icon='BLANK1').type = 'AUTOMATIC'
             row.operator("curve.handle_type_set", text="Vector", icon='BLANK1').type = 'VECTOR'
             
             row = box.row(1)   
             row.operator("curve.handle_type_set", text="Align", icon='BLANK1').type = 'ALIGNED'
             row.operator("curve.handle_type_set", text="Free", icon='BLANK1').type = 'FREE_ALIGN'

             box.separator()  
                  
             box = layout.box().column(1) 

             row = box.column(1)                                 
             row.operator("curve.switch_direction", text="Switch Direction", icon = "ARROW_LEFTRIGHT")                   
             row.operator("curve.cyclic_toggle","Open / Close Curve", icon="MOD_CURVE")  

             row = box.row(1)
             row.operator("tp_ops.wire_all", text="", icon='WIRE') 
             row.prop(context.object.data, "resolution_u", text="Set Resolution")

             box.separator()      
                                 
             row = box.row(1)  
             row.operator("curve.normals_make_consistent", "make normals consistent", icon='SNAP_NORMAL')

             box.separator()  

             box = layout.box().column(1)

             row = box.row(1)
             row.alignment = 'CENTER' 
             row.label("Subdivide")   
             
             row = box.row(1) 
             row.operator("curve.subdivide", text="1").number_cuts=1        
             row.operator("curve.subdivide", text="2").number_cuts=2
             row.operator("curve.subdivide", text="3").number_cuts=3
             row.operator("curve.subdivide", text="4").number_cuts=4
             row.operator("curve.subdivide", text="5").number_cuts=5        
             row.operator("curve.subdivide", text="6").number_cuts=6  

             box.separator() 
            
             box = layout.box().column(1)

             row = box.row(1)  
             row.operator("curve.extrude_move", text="Extrude")
             row.operator("curve.make_segment",  text="Weld") 
            
             row = box.row(1)             
             row.operator("curve.split",  text="Split")          
             row.operator("curve.bezier_spline_divide", text='Divide') 
                      
             row = box.row(1)             
             row.operator("curve.separate",  text="Separate")         
             row.operator("transform.vertex_random") 

             row = box.row(1) 
             row.operator("transform.tilt", text="Tilt")                                     
             row.operator("curve.radius_set", "Radius")                 

             box.separator()  

             row = box.row(1) 
             row.operator("curve.smooth", icon ="SMOOTHCURVE")  

             box.separator() 

             row = box.column(1)                                        
             row.operator("tp_ops.quader_curve","Create Quarter from Circle")   
             row.operator("tp_ops.half_curve","Create Half-Circle from Circle")  

             box.separator()                             

             box = layout.box().column(1)  
           
             row = box.row(1)         
             row.operator("view3d.ruler", text="Ruler")   
             
             row.operator("ed.undo_history", text="History")
             row.operator("ed.undo", text="", icon="LOOP_BACK")
             row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
             ###
             box.separator()                  


        else:
            
             box = layout.box().column(1)   

             row = box.row(1)
             sub = row.row(1)
             sub.scale_x = 7
             sub.operator("view3d.pivot_bounding_box", "", icon="ROTATE")
             sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
             sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
             sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")
             sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")  
             row.operator("purge.unused_curve_data", "", icon = "PANEL_CLOSE") 

             box = layout.box().column(1) 

             row = box.column(1) 
             row.label("Curve Type", icon="MOD_CURVE") 
             
             box.separator()
             
             row = box.row(1)
             row.operator("curve.to_poly","Poly")
             row.operator("curve.to_bezier","Bezièr")
             row.operator("curve.to_nurbs","Nurbs")

             box.separator() 
             
             box = layout.box().column(1) 

             row = box.column(1)
             row.label("Handle Type", icon="IPO_BEZIER") 
             
             box.separator()
             row = box.row(1)                            
             row.operator("curve.handle_to_free","Free")                         
             row.operator("curve.handle_to_automatic","Auto")
             
             row = box.row(1)                                                   
             row.operator("curve.handle_to_vector","Vector") 
             row.operator("curve.handle_to_aligned","Aligned")

             box.separator() 

             box = layout.box().column(1)   
             
             row = box.column(1)
             row.operator("tp_ops.origin_start_point","Origin to Start Point", icon = "LAYER_ACTIVE") 
             row.operator("curve.open_circle", text = "Open / Close", icon = "MOD_CURVE")                                                                              
             row.operator("curve.smoothspline", "Smooth Curve", icon ="SMOOTHCURVE")                
             
             row = box.row(1)
             row.operator("tp_ops.wire_all", text="", icon='WIRE') 
             row.prop(context.object.data, "resolution_u", text="Set Resolution")
            
             box.separator()            

             box = layout.box().column(1)  
             row = box.row(1)
             row.operator("object.convert",text="Convert > Mesh ", icon = "OUTLINER_DATA_MESH").target="MESH"  

             box.separator() 

             box = layout.box().column(1)  
           
             row = box.row(1)        
             row.operator("view3d.ruler", text="Ruler")   
             
             row.operator("ed.undo_history", text="History")
             row.operator("ed.undo", text="", icon="LOOP_BACK")
             row.operator("ed.redo", text="", icon="LOOP_FORWARDS") 
           
             ###
             box.separator()     




class VIEW3D_TP_Curve_Edit_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Edit_Panel_TOOLS"
    bl_label = "Edit"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_edit_panel_layout(self, context, layout)         


class VIEW3D_TP_Curve_Edit_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Curve_Edit_Panel_UI"
    bl_label = "Edit"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_edit_panel_layout(self, context, layout) 




def draw_curve_bevel_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)          
        
        if context.mode == 'EDIT_CURVE':

             box = layout.box().column(1)

             row = box.row(1)
             row.alignment = 'CENTER' 
             row.label("Bevel Curve") 
             
             row = box.row(1)        
             row.prop(context.object.data, "fill_mode", text="")           
             show = bpy.context.object.data.dimensions
             if show == '3D':
                 
                 active_bevel = bpy.context.object.data.bevel_depth            
                 if active_bevel == 0.0:              
                    row.operator("tp_ops.enable_bevel", text="Bevel on", icon='MOD_WARP')
                 else:   
                    row.operator("tp_ops.enable_bevel", text="Bevel off", icon='MOD_WARP')  
                 
             row = box.row(1)               
             row.prop(context.object.data, "use_fill_deform")

             box = layout.box().column(1)
             
             row = box.row(1)
             active_wire = bpy.context.object.show_wire 
             if active_wire == True:
                row.operator("tp_ops.wire_off", "", icon = 'MESH_PLANE')              
             else:                       
                 row.operator("tp_ops.wire_on", "", icon = 'MESH_GRID')   
                             
             row.prop(context.object.data, "bevel_depth", text="Bevel Radius")
             
             row = box.row(1)
             row.prop(context.object.data, "resolution_u", text="Rings")          
             row.prop(context.object.data, "bevel_resolution", text="Loops")

             row = box.row(1)
             row.prop(context.object.data, "offset")
             row.prop(context.object.data, "extrude","Height") 
            
             box.separator()  
                                   
             row = box.column_flow(2)
             row.label("Value Rings", icon = "MOD_CURVE")  
             row.label("1 = 4",) 
             row.label("2 = 8") 
             row.label("4 = 16") 
             row.label("8 = 32")
             row.label("(+4) Ring")          

             row.label("Value Loops", icon = "MOD_CURVE")  
             row.label("0 = 4",) 
             row.label("6 = 16") 
             row.label("10 = 24") 
             row.label("14 = 32")           
             row.label("(+2) Loop")    
                            
             box = layout.box().column(1)
             
             row = box.row(1) 
             row.label(text="Bevel Factor:")
         
             row.active = (context.object.data.bevel_depth > 0 or context.object.data.bevel_object is not None)

             row = box.row(1) 
             row.prop(context.object.data, "bevel_factor_start", text="Start") 
             row.prop(context.object.data, "bevel_factor_end", text="End")  

             row = box.row(1) 
             row.prop(context.object.data, "bevel_factor_mapping_start", text="")
             row.prop(context.object.data, "bevel_factor_mapping_end", text="")
                      
             row = box.row(1)                      
             sub = row.row()
             sub.active = context.object.data.taper_object is not None
             sub.prop(context.object.data, "use_map_taper")

             sub = row.row()
             sub.active = context.object.data.bevel_object is not None
             sub.prop(context.object.data, "use_fill_caps")

             box = layout.box().column(1)
             
             row = box.row(1)  
             row.label(text="Taper Object:")
             row.prop(context.object.data, "taper_object", text="")
             
             row = box.row(1) 
             row.label(text="Bevel Object:")
             row.prop(context.object.data, "bevel_object", text="")

             box = layout.box().column(1)

             row = box.row(1) 
             row.alignment = 'CENTER' 
             row.label(text="Path / Curve-Deform")

             row = box.row(1)
             row.prop(context.object.data, "use_radius")
             row.prop(context.object.data, "use_stretch")
             row.prop(context.object.data, "use_deform_bounds")
             
             row = box.row(1)
             row.alignment = 'CENTER' 
             row.label(text="Twisting")

             row = box.row(1) 
             row.active = (context.object.data.dimensions == '2D' or (context.object.data.bevel_object is None and context.object.data.dimensions == '3D'))
             row.prop(context.object.data,"twist_mode", text="")
             row.prop(context.object.data, "twist_smooth", text="Smooth")

             ###
             box.separator()   

        else:  
                      
             box = layout.box().column(1)   
         
             row = box.row(1)        
             row.prop(context.object.data, "fill_mode", text="")           
            
             show = bpy.context.object.data.dimensions
             if show == '3D':
                 
                 active_bevel = bpy.context.object.data.bevel_depth            
                 if active_bevel == 0.0:              
                    row.operator("tp_ops.enable_bevel", text="Bevel on", icon='MOD_WARP')
                 else:   
                    row.operator("tp_ops.enable_bevel", text="Bevel off", icon='MOD_WARP')                 
                          
             row = box.row(1)                          
             row.prop(context.object.data, "use_fill_deform")

             box = layout.box().column(1)   
             
             row = box.row(1) 
             row = box.row(1)
             active_wire = bpy.context.object.show_wire 
             if active_wire == True:
                row.operator("tp_ops.wire_off", "", icon = 'MESH_PLANE')              
             else:                       
                 row.operator("tp_ops.wire_on", "", icon = 'MESH_GRID') 
                                                        
             row.prop(context.object.data, "bevel_depth", text="Bevel Radius")
            
             row = box.row(1)
             row.prop(context.object.data, "resolution_u", text="Rings")          
             row.prop(context.object.data, "bevel_resolution", text="Loops")

             row = box.row(1)
             row.prop(context.object.data, "offset")
             row.prop(context.object.data, "extrude","Height")
            
             box.separator()  
                                   
             row = box.column_flow(2)
             row.label("Value Rings", icon = "MOD_CURVE")  
             row.label("1 = 4",) 
             row.label("2 = 8") 
             row.label("4 = 16") 
             row.label("8 = 32")
             row.label("(+4) Ring")          

             row.label("Value Loops", icon = "MOD_CURVE")  
             row.label("0 = 4",) 
             row.label("6 = 16") 
             row.label("10 = 24") 
             row.label("14 = 32")           
             row.label("(+2) Loop")                                 

             box.separator() 

             box = layout.box().column(1)

             row = box.row(1)              
             row.alignment = 'CENTER'
             row.label("Bevel & Taper", icon = "MOD_CURVE")    
            
             box.separator()
              
             row = box.row(1)
             row.operator("curve.bevelcurve", "C-Bevel", icon = "CURVE_BEZCIRCLE") 
             row.prop(context.object.data, "bevel_object", text = "")
             
             row = box.row(1)
             row.operator("curve.tapercurve", "C-Taper", icon = "CURVE_BEZCURVE") 
             row.prop(context.object.data, "taper_object", text = "")
     
             box.separator() 

             box = layout.box().column(1)

             row = box.row(1)              
             row.alignment = 'CENTER'
             row.label("Bevel Factor", icon = "MOD_CURVE")    
            
             box.separator()
            
             row = box.row(1) 
             row.prop(context.object.data, "bevel_factor_start", text="Start") 
             row.prop(context.object.data, "bevel_factor_end", text="End")  

             row = box.row(1) 
             row.prop(context.object.data, "bevel_factor_mapping_start", text="")
             row.prop(context.object.data, "bevel_factor_mapping_end", text="")    

             box.separator() 

             box = layout.box().column(1)  

             row = box.row(1) 
             row.alignment = 'CENTER'
             row.label(text="Path / Deform / Twist:")

             box.separator() 

             row = box.row(1)
             row.prop(context.object.data, "use_radius")
             row.prop(context.object.data, "use_stretch")
             row = box.row(1)
             row.prop(context.object.data, "use_deform_bounds")   
            
             row = box.row(1)                        
             row.prop(context.object.data,"twist_mode", text="")
             row.prop(context.object.data, "twist_smooth", text="Smooth")    
            
             ###
             box.separator()                                    
     




class VIEW3D_TP_Curve_Bevel_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Bevel_Panel_TOOLS"
    bl_label = "Bevel"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_bevel_panel_layout(self, context, layout)



class VIEW3D_TP_Curve_Bevel_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Curve_Bevel_Panel_UI"
    bl_label = "Bevel"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'
         
         draw_curve_bevel_panel_layout(self, context, layout)




def draw_curve_tools_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)          
        
        if context.mode == 'EDIT_CURVE':
         
             box = layout.box().column(1)

             row = box.row(1) 
             row.operator("object._curve_outline",  text="Outline")             
             row.operator("curve.bezier_points_fillet", text='Fillet') 

             row = box.row(1)                         
             row.operator("curve.trim_tool", text="Trim")
             row.operator("curve.extend_tool", text="Extend")

             ###
             box.separator()  
        
        else:

             box = layout.box().column(1)  
            
             row = box.row(1)
             active_wire = bpy.context.object.show_wire 
             if active_wire == True:
                row.operator("tp_ops.wire_off", "", icon = 'MESH_PLANE')              
             else:                       
                 row.operator("tp_ops.wire_on", "", icon = 'MESH_GRID') 
             row.prop(context.object.data, "resolution_u", text="Odd Resolution")                         

             box = layout.box().column(1)  
              
             row = box.row(1) 
             row.scale_y = 1.5                  
             row.operator("curvetools2.operatorloftcurves", text = "Loft")
             row.operator("curvetools2.operatorsweepcurves", text = "Sweep")  
             row.operator("curvetools2.operatorbirail", text = "Birail")  

             box = layout.box().column(1)  

             row = box.row(1)
             row.operator("curvetools2.operatorintersectcurves", text = "Intersect Curves")
             row = box.row(1)
             row.prop(context.scene.curvetools, "LimitDistance", text = "LimitDistance")
                     
             box = layout.box().column(1) 
            
             row = box.row(align=0)
             row.prop(context.scene.curvetools, "IntersectCurvesAlgorithm", text = "Algorithm")

             row = box.row(align=0.1)
             row.prop(context.scene.curvetools, "IntersectCurvesMode", text = "Mode")

             row = box.row(align=0.1)
             row.prop(context.scene.curvetools, "IntersectCurvesAffect", text = "Affect")

             ###
             box.separator()               



class VIEW3D_TP_Curve_Tools_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Tools_Panel_TOOLS"
    bl_label = "Tools"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_tools_panel_layout(self, context, layout)


class VIEW3D_TP_Curve_Tools_Panel_UI(bpy.types.Panel):
    bl_idname = "VIEW3D_TP_Curve_Tools_Panel_UI"
    bl_label = "Tools"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'         

         draw_curve_tools_panel_layout(self, context, layout)




def draw_curve_utility_panel_layout(self, context, layout):

        icons = icon_collections["main"]

        #my_button_one = icons.get("my_image1")
        #row.label(text="Icon", icon_value=my_button_one.icon_id)          
        
        if context.mode == 'EDIT_CURVE':

             box = layout.box().column(1)  

             row = box.row(1)
             row.alignment = "CENTER" 
             row.label("Optimize Tools for BezièrCurve", icon="LAMP")

             row = box.row(1) 
             row.operator("curvetools2.operatorsplinesjoinneighbouring", text = "Join neighbouring splines", icon ="AUTOMERGE_ON")

             row = box.row(1)
             row.prop(context.scene.curvetools, "SplineJoinDistance", text = "Threshold join")
            
             box = layout.box().column(1) 

             row = box.row(1) 
             row.prop(context.scene.curvetools, "SplineJoinStartEnd", text = "Only at start & end")

             row = box.row(align=0.5) 
             row.prop(context.scene.curvetools, "SplineJoinMode", text = "Join")

             box = layout.box().column(1) 

             row = box.row(1)             
             row.operator("curvetools2.operatorsplinesremovezerosegment", text = "del 0-segments", icon ="DISCLOSURE_TRI_DOWN")
             row.operator("curvetools2.operatorsplinesremoveshort", text = "del short splines", icon ="DISCLOSURE_TRI_DOWN")

             row = box.row(1)
             row.prop(context.scene.curvetools, "SplineRemoveLength", text = "Threshold remove")

             ###
             box.separator()                             
         

        else:
            
            
             box = layout.box().column(1)  

             row = box.row(1)
             row.alignment = "CENTER" 
             row.label("Optimize Tools for BezièrCurve", icon="LAMP")
             
             row = box.row(1) 
             row.operator("curvetools2.operatorsplinesjoinneighbouring", text = "Join neighbouring splines")

             row = box.row(1)
             row.prop(context.scene.curvetools, "SplineJoinDistance", text = "Threshold join")

             box = layout.box().column(1) 

             row = box.row(1) 
             row.prop(context.scene.curvetools, "SplineJoinStartEnd", text = "Only at start & end")

             row = box.row(align=0.5) 
             row.prop(context.scene.curvetools, "SplineJoinMode", text = "Join")

             box = layout.box().column(1) 

             row = box.row(1)             
             row.operator("curvetools2.operatorsplinesremovezerosegment", text = "del 0-segments")
             row.operator("curvetools2.operatorsplinesremoveshort", text = "del short splines")

             row = box.row(1)
             row.prop(context.scene.curvetools, "SplineRemoveLength", text = "Threshold remove")

             ###
             box.separator()   
                




class VIEW3D_TP_Curve_Utility_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Utility_Panel_TOOLS"
    bl_label = "Utility"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_utility_panel_layout(self, context, layout)



class VIEW3D_TP_Curve_Utility_Panel_UI(bpy.types.Panel):
    bl_category = "Curve"
    bl_idname = "VIEW3D_TP_Curve_Utility_Panel_UI"
    bl_label = "Utility"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)

    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'

         draw_curve_utility_panel_layout(self, context, layout)         




def draw_curve_set_panel_layout(self, context, layout):

         icons = icon_collections["main"]

         #my_button_one = icons.get("my_image1")
         #row.label(text="Icon", icon_value=my_button_one.icon_id)          

         box = layout.box().column(1)   
         
         row = box.column(1)
                        
         if context.object.data.splines.active.type == 'POLY':
             row.prop(context.object.data.splines.active, "use_cyclic_u", text="U Cyclic")                        
             row.prop(context.object.data.splines.active, "use_smooth")
         else:
             if context.object.data.splines.active.type == 'NURBS':
                 row.prop(context.object.data.splines.active, "use_cyclic_u", text="U Cyclic")

             if context.object.data.splines.active.type == 'NURBS':
                 row.prop(context.object.data.splines.active, "use_bezier_u", text="U Bezier")
                 row.prop(context.object.data.splines.active, "use_endpoint_u", text="U Endpoint")
                 row.prop(context.object.data.splines.active, "order_u", text="U Order")
 
             if context.object.data.splines.active.type == 'SURFACE':
                 row.prop(context.object.data.splines.active, "use_cyclic_v", text="V Cyclic")
                 row.prop(context.object.data.splines.active, "use_bezier_v", text="V Bezier")
                 row.prop(context.object.data.splines.active, "use_endpoint_v", text="V Endpoint")
                 row.prop(context.object.data.splines.active, "order_v", text="V Order")

             if context.object.data.splines.active.type == 'BEZIER':

                 row.label(text="Interpolation:")
                 row.active = (context.object.data.dimensions == '3D')
                 row.prop(context.object.data.splines.active, "tilt_interpolation", text="Tilt")
                 row.prop(context.object.data.splines.active, "radius_interpolation", text="Radius")
             
             row.prop(context.object.data.splines.active, "use_smooth")

         box.separator() 

         box = layout.box().column(1)   
         
         row = box.row(1)        
         row.prop(context.object.data, "use_path", text="Path Animation")

         row = box.column()
         row.prop(context.object.data, "path_duration", text="Frames")
         row.prop(context.object.data, "eval_time")

         # these are for paths only
         row = box.row()
         row.prop(context.object.data, "use_path_follow")

         ###
         box.separator() 

        


class VIEW3D_TP_Curve_Set_Panel_TOOLS(bpy.types.Panel):
    bl_category = "Curve"
    bl_context = "objectmode"
    bl_idname = "VIEW3D_TP_Curve_Set_Panel_TOOLS"
    bl_label = "Setting"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)


    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'
         
         draw_curve_set_panel_layout(self, context, layout)



class VIEW3D_TP_Curve_Set_Panel_UI(bpy.types.Panel):
    bl_context = "objectmode"
    bl_idname = "VIEW3D_TP_Curve_Set_Panel_UI"
    bl_label = "Setting"
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
        if len(context.selected_objects) > 0:
            return (context.active_object.type == "CURVE" and isModelingMode)


    def draw(self, context):
         layout = self.layout.column_flow(1)  
         layout.operator_context = 'INVOKE_REGION_WIN'
         
         draw_curve_set_panel_layout(self, context, layout)





# Menus ################################################

# Define the "Extras" menu
class INFO_MT_curve_plants_add(bpy.types.Menu):
    bl_idname = "curve_plants_add"
    bl_label = "Plants"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        col = layout.column()
        self.layout.separator()
        
        layout.operator("curve.tree_add", text="Sapling 3")
       
        self.layout.operator("curve.ivy_gen", text="Add Ivy to Mesh").updateIvy = True



# Define the "Extras" menu
class INFO_MT_curve_knots_add(bpy.types.Menu):
    bl_idname = "curve_knots_add"
    bl_label = "Plants"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        col = layout.column()
        self.layout.separator()
        
        layout.operator("curve.torus_knot_plus", text="Torus Knot Plus")
        layout.operator("curve.celtic_links", text="Celtic Links")
        layout.operator("mesh.add_braid", text="Braid Knot")



# Define the "Extras" menu
class INFO_MT_curve_extras_add(bpy.types.Menu):    
    bl_idname = "curve_extra_objects_add"
    bl_label = "Extra Objects"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        col = layout.column()
        self.layout.separator()
        
        layout.operator("mesh.curveaceous_galore", text="Curves Galore!")
        layout.operator("curve.spirals", text="Spirals")
        layout.operator("curve.curlycurve", text="Curly Curve")
        layout.operator("curve.formulacurves", text="Formula Curve")
        layout.operator("curve.wires", text="Curve Wires")
        
        layout.separator()
        
        layout.label(text="Curve Utils")
        
        layout.operator("curve.simplify", text="Simplify Curves")
        layout.operator("curve.dial_scale", text="Dial/Scale")



# Define "Extras" menu
def menu(self, context):
    layout = self.layout
    
    col = layout.column()
    self.layout.separator()
    
    layout.label(text="AF: Curve Objects", icon="OUTLINER_OB_CURVE")
    
    self.layout.menu("curve_plants_add", text="Plants", icon="CURVE_DATA")
    self.layout.menu("curve_knots_add", text="Knots", icon='CURVE_DATA')
    self.layout.operator("mesh.curveaceous_galore", text="Curves Galore!", icon="CURVE_DATA")
    self.layout.operator("curve.spirals", text="Spirals", icon="CURVE_DATA")
    self.layout.operator("curve.curlycurve", text="Curly Curve", icon="CURVE_DATA")
    self.layout.operator("curve.formulacurves", text="Formula Curve", icon="CURVE_DATA")
    self.layout.operator("curve.wires", text="Curve Wires", icon="CURVE_DATA")
    self.layout.operator("curve.dial_scale", text="Dial/Scale", icon="CURVE_DATA")
    
    self.layout.separator()
    
    layout.label(text="Curve Utils")
    self.layout.operator("curve.simplify", text="Curve Simplify", icon="CURVE_DATA")



# Define the "Extras" menu
def menu_surface(self, context):
    layout = self.layout
    
    col = layout.column()
    self.layout.separator()
    
    layout.label(text="Surface Factory")
    
    self.layout.operator("object.add_surface_wedge", text="Wedge", icon="MOD_CURVE")
    self.layout.operator("object.add_surface_cone", text="Cone", icon="MOD_CURVE")
    self.layout.operator("object.add_surface_star", text="Star", icon="MOD_CURVE")
    self.layout.operator("object.add_surface_plane", text="Plane", icon="MOD_CURVE")
    self.layout.operator("curve.smooth_x_times", text="Special Smooth", icon="MOD_CURVE")






# Registry ###############################################              

import traceback

icon_collections = {}

def register():

    import bpy.utils.previews
    mkb_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mkb_icons.load("my_image1", os.path.join(icons_dir, "icon_image1.png"), 'IMAGE')    

    icon_collections['main'] = mkb_icons   

    add_curve_beveled.register()
    add_simple_curve.register()
    curve_action.register()

    
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
        
    update_panel_position(None, bpy.context)

    # Add "Extras" menu to the "Add Primitiv" menu
    bpy.types.INFO_MT_curve_add.append(menu)
    bpy.types.INFO_MT_surface_add.append(menu_surface)
    bpy.types.GRAPH_MT_channel.append(curve_simplify.menu_func)
    bpy.types.DOPESHEET_MT_channel.append(curve_simplify.menu_func)



def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    add_curve_beveled.unregister()
    add_simple_curve.unregister()
    curve_action.unregister()


    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    # Remove "Extras" menu from the "Add Primitiv" menu.
    bpy.types.INFO_MT_curve_add.remove(menu)
    bpy.types.INFO_MT_surface_add.remove(menu_surface)
    bpy.types.GRAPH_MT_channel.remove(curve_simplify.menu_func)
    bpy.types.DOPESHEET_MT_channel.remove(curve_simplify.menu_func)

    del bpy.types.Scene.curvetools

if __name__ == "__main__":
    register()


