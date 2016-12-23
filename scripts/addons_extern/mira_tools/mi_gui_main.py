# BEGIN GPL LICENSE BLOCK #####
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
# END GPL LICENSE BLOCK #####

import bpy, os
from bpy import*
from bpy.props import  *




def draw_ModifyPanel_layout(self, context, layout):
        lt = context.window_manager.mirawindow
                
        icons = icon_collections["main"]
        #mi_settings = context.scene.mi_settings
        #extrude_settings = context.scene.mi_extrude_settings
        #cur_surfs_settings = context.scene.mi_cur_surfs_settings

        box = layout.box().column(1)         

        row = box.row(1)
        row.label("New Mesh Drawing")
            
        box.separator() 

        row = box.row(1)                             
        row.operator("mira.draw_extrude", text="Draw Extrude", icon="VPAINT_HLT")

        row = box.row(1)                 
        if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
            row.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='Step')
        else:
            row.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='Step')
       
        box.separator()

        row = box.row(1)          
        row.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='Step') 
            
        box.separator()

        row = box.row(1)
        if lt.display_help:            
            my_button_one = icons.get("my_image1")
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id).url = "https://lh3.googleusercontent.com/-tIDzK8yFnjU/VbhVbn2cfSI/AAAAAAAAIPo/mYRzdjqOki0/w530-h749-p/%25231_Draw_Extrude.png"           

        if context.scene.mi_settings.surface_snap is False:
            row.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

            if context.scene.mi_extrude_settings.do_symmetry:
                row.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='Axys')

        box.separator()

        box = layout.box().column(1)

        row = box.row(1)
        row.label("New Mesh Creation")
            
        box.separator()
        
        row = box.row(1) 
        if lt.display_help:           
            my_button_one = icons.get("my_image1")             
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id).url = "https://lh3.googleusercontent.com/-0fzOvLD4EM8/Vb5CdYy5qKI/AAAAAAAAIVk/EkiLDYzwtVk/w780-h840-no/%25233_Poly_Loop.png"                  
        row.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")
            
        box.separator()

        row = box.row(1)
        if lt.display_help:             
            my_button_one = icons.get("my_image1")           
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id).url = "https://lh5.googleusercontent.com/-o3W-ypmbxI8/Vb5gyXLJ4tI/AAAAAAAAIXc/ZsNqJR5WiWw/w746-h840-no/%25234_Curve_Surface.png"              
        row.operator("mira.curve_surfaces", text="CurveSurfaces", icon="SURFACE_NCURVE")
        
        box.separator()
        
        row = box.row(1)
        row.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='Points')  

        box.separator()


class MI_ModifyPanel_TOOLS(bpy.types.Panel):
    bl_idname = "MI_ModifyPanel_TOOLS"
    bl_label = "Modify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)        
        return (context.object is not None and isModelingMode)


    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        
        mi_settings = context.scene.mi_settings
        extrude_settings = context.scene.mi_extrude_settings
        cur_surfs_settings = context.scene.mi_cur_surfs_settings

        draw_ModifyPanel_layout(self, context, layout)   


class MI_ModifyPanel_UI(bpy.types.Panel):
    bl_idname = "MI_ModifyPanel_UI"
    bl_label = "Modify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)        
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        mi_settings = context.scene.mi_settings
        extrude_settings = context.scene.mi_extrude_settings
        cur_surfs_settings = context.scene.mi_cur_surfs_settings
        
        draw_ModifyPanel_layout(self, context, layout)   






def draw_DeformPanel_layout(self, context, layout):
        lt = context.window_manager.mirawindow
                
        icons = icon_collections["main"]        
        #cur_stretch_settings = context.scene.mi_cur_stretch_settings
        #lin_def_settings = context.scene.mi_ldeformer_settings
        #curguide_settings = context.scene.mi_curguide_settings

        box = layout.box().column(1)  

        row = box.row(1)
        row.label("Mesh Transformation")
            
        box.separator() 
        
        row = box.row(1) 
        row.operator("screen.redo_last", text = "", icon="SETTINGS") 
        row.operator("mira.deformer", text="Deformer")
        row.operator("mira.noise", text="NoiseDeform", icon="RNDCURVE")
       
        box.separator() 
 
        row = box.row(1) 
        row.operator("mira.linear_deformer", text="LinearDeformer", icon="OUTLINER_OB_MESH")
        
        row = box.row(1)
        if lt.display_help:              
            my_button_one = icons.get("my_image1")           
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id ).url = "https://lh4.googleusercontent.com/-GTuGp92YHvc/VbruOKWUTTI/AAAAAAAAIUk/LbjhscUtqHI/w611-h840-no/%25232_Deform_Mesh.png"           
        row.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

        box.separator() 

        box = layout.box().column(1) 

        row = box.row(1)
        row.label("Loop Manipulation")
            
        box.separator()        
        
        row = box.row(1)        
        row.operator("mira.curve_stretch", text="CurveStretch", icon="STYLUS_PRESSURE")
        
        row = box.row(1)
        if lt.display_help:              
            my_button_one = icons.get("my_image1")
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id).url = "https://lh3.googleusercontent.com/-pFQ0XaKlZY4/VcDyem3HKaI/AAAAAAAAIZI/oELrYw398oM/w530-h597-p/%25235_Curve_Stretch.png"         
        row.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')       
        
        box.separator()
        
        row = box.row(1)     
        row.operator("mira.curve_guide", text="CurveGuide", icon="RNA")

        row = box.row(1)
        if lt.display_help:              
            my_button_one = icons.get("my_image1")
            row.operator("wm.url_open", text="", icon_value=my_button_one.icon_id).url = "https://lh3.googleusercontent.com/WBih_PAVzmvuBWVuAv-iO6_ZAy1L9PdSaIm1C-AmkJkCeM8kl3te7DESf98kn3SAWVZWSLNAIg=w1920-h1080-no"        
        row.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')

        box.separator() 
        
        row = box.row(1)
        row.prop(context.scene.mi_curguide_settings, "deform_type", text='Type')      

        box.separator() 



class MI_DeformPanel_TOOLS(bpy.types.Panel):
    bl_idname = "MI_DeformPanel_TOOLS"
    bl_label = "Deform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        cur_stretch_settings = context.scene.mi_cur_stretch_settings
        lin_def_settings = context.scene.mi_ldeformer_settings
        curguide_settings = context.scene.mi_curguide_settings

        draw_DeformPanel_layout(self, context, layout)   


class MI_DeformPanel_UI(bpy.types.Panel):
    bl_idname = "MI_DeformPanel_UI"
    bl_label = "Deform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)        
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        cur_stretch_settings = context.scene.mi_cur_stretch_settings
        lin_def_settings = context.scene.mi_ldeformer_settings
        curguide_settings = context.scene.mi_curguide_settings

        draw_DeformPanel_layout(self, context, layout)   







def draw_SettingsPanel_layout(self, context, layout):
     
        lt = context.window_manager.mirawindow
                
        icons = icon_collections["main"]

        #mi_settings = context.scene.mi_settings

        box = layout.box().column(1)

        row = box.column(1)
        row.prop(context.scene.mi_settings, "surface_snap", text='Surface Snapping', icon ="SNAP_SURFACE")
        row.prop(context.scene.mi_settings, "convert_instances", text='Convert Instances')

        box.separator() 

        row = box.column(1)
        row.prop(context.scene.mi_settings, "snap_objects", text='Snap')

        box.separator() 

        box = layout.box().column(1)

        row = box.column(1)
        row.prop(context.scene.mi_settings, "spread_mode", text='Spread')

        box.separator() 

        row = box.column(1)
        row.prop(context.scene.mi_settings, "curve_resolution", text='Resolution')

        box.separator() 

        row = box.row(1)
        row.operator("mira.curve_test", text="Curve Test")
        row.prop(context.scene.mi_settings, "draw_handlers", text='Handlers')

        box.separator() 
        
        box = layout.box().column(1)

        row = box.column(1)
        row.operator('wm.url_open', text = 'Wiki', icon='HELP').url = "https://github.com/mifth/mifthtools/wiki/Mira-Tools"

        row = box.row(1)
        my_button_one = icons.get("my_image1")            
        row.prop(lt, "display_help", text=" Help-URL-Buttons", icon_value=my_button_one.icon_id)




        
    
class MI_SettingsPanel_TOOLS(bpy.types.Panel):
    bl_idname = "MI_SettingsPanel_TOOLS"
    bl_label = "Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)        
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        mi_settings = context.scene.mi_settings

        draw_SettingsPanel_layout(self, context, layout) 


    
class MI_SettingsPanel_UI(bpy.types.Panel):
    bl_idname = "MI_SettingsPanel_UI"
    bl_label = "Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        #context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)        
        return (context.object is not None and isModelingMode)

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        mi_settings = context.scene.mi_settings

        draw_SettingsPanel_layout(self, context, layout)   
          



#register

icon_collections = {}

def register_icons():
    import bpy.utils.previews
    
    mira_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mira_icons.load("my_image1", os.path.join(icons_dir, "icon_image1.png"), 'IMAGE')

    icon_collections['main'] = mira_icons
    

def unregister_icons():
    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear() 


def register():
    
    bpy.utils.register_module(__name__)

def unregister():

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
    