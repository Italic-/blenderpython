bl_info = {
    "name": "JARCH Vis",
    "author": "Jacob Morris",
    "version": (0, 8, 2),
    "blender": (2, 76, 0),
    "location": "View 3D > Toolbar > JARCH Vis",
    "description": "Adds Architectural Objects Like Flooring, Siding, Stairs, and Roofing",
    "category": "Add Mesh"
}

if "bpy" in locals():
    import imp
    imp.reload(jarch_siding)
    imp.reload(jarch_flooring)
    imp.reload(jarch_stairs)
    imp.reload(jarch_roofing)
else:
    from . import jarch_siding
    from . import jarch_flooring
    from . import jarch_stairs
    from . import jarch_roofing

import bpy
from bpy.props import (CollectionProperty, 
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        IntProperty,
        FloatVectorProperty,
        )
from bpy_extras import view3d_utils
from bpy.types import (
        PropertyGroup,
        )

class FaceGroup(bpy.types.PropertyGroup):
    data = StringProperty()
    num_faces = IntProperty()
    face_slope = FloatProperty()
    rot = FloatProperty(unit="ROTATION")

class SidingPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_jarch_siding"
    bl_label = "JARCH Vis"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        SIDINGDROP = scene.UTSidingDrop
        FLOORDROP = scene.UTFloorDrop
        STAIRDROP = scene.UTStairDrop
        ROOFDROP = scene.UTRoofDrop
        view = context.space_data
        toolsettings = context.tool_settings

# siding
        layout = self.layout
        ob = context.object
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTSidingDrop", icon="TRIA_DOWN")
        if SIDINGDROP:
            if bpy.context.mode == "EDIT_MESH":
                layout.label("JARCH Vis Doesn't Work In Edit Mode", icon="ERROR")
            else:
                o = context.object
                if o != None:
                    if o.type == "MESH":
                        if o.f_object_add == "none" and o.s_object_add == "none" and o.ro_object_add == "none":
                            if o.object_add in ("convert", "add"):
                                layout.label("Material:")
                                layout.prop(o, "mat", icon="MATERIAL")
                                layout.label("Type(s):")
                                if o.mat == "1":
                                    layout.prop(o, "if_wood", icon="OBJECT_DATA")
                                elif o.mat == "2":
                                    layout.prop(o, "if_vinyl", icon="OBJECT_DATA")
                                elif o.mat == "3":
                                    layout.prop(o, "if_tin", icon="OBJECT_DATA")
                                elif o.mat == "4":
                                    layout.label("Horizontal: Lap", icon="OBJECT_DATA")
                                elif o.mat == "5":
                                    layout.label("Bricks", icon="OBJECT_DATA")
                                elif o.mat == "6":
                                    layout.label("Stone", icon="OBJECT_DATA")
                                layout.separator()
                                # measurements
                                if o.object_add == "add":
                                    layout.prop(o, "over_width")
                                    layout.prop(o, "over_height")
                                    layout.separator()
                                if o.mat not in ("3", "5", "6"):
                                    layout.prop(o, "board_width")
                                elif o.mat == "3":
                                    layout.label("Sheet Lays: 36 (in)", icon="ARROW_LEFTRIGHT")
                                    layout.prop(o, "is_screws", icon="PLUS")
                                if o.mat not in ("5", "6"):  # if not bricks or stone
                                    if o.mat == "1" and o.if_wood == "1":
                                        layout.prop(o, "board_space")
                                        layout.separator()
                                    if o.mat in ("1", "2"):
                                        if (o.if_vinyl == "1" and o.mat == "2") or (o.if_wood == "3" and o.mat == "1"):
                                            layout.prop(o, "batten_width")
                                            if o.batten_width / 2 > (o.board_width / 2) - (0.125 / 39.3701):
                                                layout.label("Max Width: " + str(round(2 * ((o.board_width / 2) - (0.125 / 39.3701)), 3)) + " in", icon="ERROR")
                                elif o.mat == "5":  # bricks
                                    layout.prop(o, "b_width")
                                    layout.prop(o, "b_height")
                                    layout.separator()
                                    if o.object_add == "add":
                                        layout.prop(o, "is_corner", icon="VIEW3D")
                                    if o.is_corner == False:
                                        layout.separator()
                                        layout.prop(o, "b_ran_offset", icon="NLA")
                                        if o.b_ran_offset == False:
                                            layout.prop(o, "b_offset")
                                        else:
                                            layout.prop(o, "b_vary")
                                    else:
                                        layout.separator()
                                        layout.prop(o, "is_left", icon="TRIA_LEFT")
                                        layout.prop(o, "is_right", icon="TRIA_RIGHT")
                                        layout.prop(o, "is_invert", icon="FILE_REFRESH")
                                        layout.separator()
                                    layout.prop(o, "b_gap")
                                    layout.separator()
                                    layout.prop(o, "m_depth")
                                    layout.separator()
                                if o.object_add == "convert":
                                    layout.prop(o, "x_offset")
                                    layout.separator()
                                if o.mat in ("5", "6") or (o.mat == "1" and o.if_wood == "1"):
                                    layout.prop(o, "is_bevel", icon="MOD_BEVEL")
                                    if o.is_bevel == True and o.mat != "1":
                                        layout.prop(o, "res", icon="OUTLINER_DATA_CURVE")
                                        layout.separator()
                                    elif o.mat == "1" and o.is_bevel == True:
                                        layout.prop(o, "bevel_width")
                                if o.mat == "6":  # stone
                                    layout.prop(o, "av_width")
                                    layout.prop(o, "av_height")
                                    layout.separator()
                                    layout.prop(o, "s_random")
                                    layout.prop(o, "b_random")
                                    layout.separator()
                                    layout.prop(o, "b_gap")
                                    layout.prop(o, "s_mortar")
                                layout.separator()
                                if o.object_add == "add":
                                    layout.prop(o, "is_slope", icon="TRIA_UP")
                                    if o.is_slope == True:
                                        layout.label("Pitch x/12", icon="LINCURVE")
                                        layout.prop(o, "slope")
                                        units = " m"
                                        if o.is_corner == False:
                                            ht = round(o.over_height - ((o.slope * (o.over_width / 2)) / 12), 2)
                                            if ht <= 0:
                                                slope = round(((24 * o.over_height) / o.over_width) - 0.01, 2)
                                                ht = round(o.over_height - ((slope * (o.over_width / 2)) / 12), 2)
                                                layout.label("Max Slope: " + str(slope), icon="ERROR")
                                        else:
                                            ht = round(o.over_height - ((o.slope * ((o.over_width + (2 * o.b_width)) / 2)) / 12), 2)
                                            if ht <= 0:
                                                slope = round(((24 * o.over_height) / o.over_width + (2 * o.b_width)) - 0.01, 2)
                                                ht = round(o.over_height - ((slope * ((o.over_width + (2 * o.b_width)) / 2)) / 12), 2)
                                                layout.label("Max Slope: " + str(slope), icon="ERROR")
                                        if context.scene.unit_settings.system == "IMPERIAL":
                                            ht = round(3.28084 * ht, 2)
                                            units = " ft"
                                        layout.label("Height At Edges: " + str(ht) + units, icon="TEXT")
                                if o.mat not in ("5", "6"):
                                    if o.mat == "1":
                                        if o.if_wood == "1":
                                            layout.prop(o, "is_width_vary", icon="UV_ISLANDSEL")
                                            if o.is_width_vary == True:
                                                layout.prop(o, "width_vary")
                                    if o.mat != "3":
                                        layout.prop(o, "is_length_vary", icon="NLA")
                                    if o.is_length_vary == True:
                                        layout.prop(o, "length_vary")
                                        layout.prop(o, "max_boards")
                                    if o.mat == "2":
                                        layout.separator()
                                        layout.prop(o, "res", icon="OUTLINER_DATA_CURVE")
                                        layout.separator()
                                if o.object_add == "add":
                                    layout.prop(o, "is_cutout", icon="MOD_BOOLEAN")
                                    units = " m"
                                    if context.scene.unit_settings.system == "IMPERIAL":
                                        units = " ft"
                                    if o.is_cutout == True:
                                        if o.mat == "5":
                                            layout.separator()
                                            layout.prop(o, "is_soldier", icon="DOTSUP")
                                            layout.separator()
                                        layout.prop(o, "num_cutouts")
                                        layout.separator()
                                        layout.label("X, Z, Height, Width in" + units)
                                        for i in range(1, o.num_cutouts + 1):
                                            layout.label("Cutout " + str(i) + ":", icon="MOD_BOOLEAN")
                                            layout.prop(o, "nc" + str(i))
                                layout.separator()
                                layout.prop(o, "unwrap", icon="GROUP_UVS")
                                if o.unwrap == True:
                                    layout.prop(o, "random_uv", icon="RNDCURVE")
                                layout.separator()
                                # materials
                                if context.scene.render.engine == "CYCLES":
                                    layout.prop(o, "is_material", icon="MATERIAL")
                                else:
                                    layout.label("Materials Only Supported With Cycles", icon="POTATO")
                                layout.separator()
                                if o.is_material == True and context.scene.render.engine == "CYCLES":
                                    if o.mat == "6":
                                        layout.prop(o, "s_mat")
                                        layout.separator()
                                    if o.mat in ("2", "3", "4"):
                                        layout.prop(o, "mat_color", icon="COLOR")  # vinyl and tin
                                    elif o.mat == "1" or (o.mat == "6" and o.s_mat == "1"):  # wood and fiber cement
                                        layout.prop(o, "col_image", icon="COLOR")
                                        layout.prop(o, "is_bump", icon="SMOOTHCURVE")
                                        if o.is_bump == True:
                                            layout.prop(o, "norm_image", icon="TEXTURE")
                                            layout.prop(o, "bump_amo")
                                        layout.prop(o, "im_scale", icon="MAN_SCALE")
                                        layout.prop(o, "is_rotate", icon="MAN_ROT")
                                    elif o.mat == "5" or (o.mat == "6" and s_mat == "2"):  # bricks
                                        layout.prop(o, "color_style", icon="COLOR")
                                        layout.prop(o, "mat_color", icon="COLOR")
                                        if o.color_style != "constant":
                                            layout.prop(o, "mat_color2", icon="COLOR")
                                        if o.color_style == "extreme":
                                            layout.prop(o, "mat_color3", icon="COLOR")
                                        layout.prop(o, "color_sharp")
                                        layout.prop(o, "color_scale")
                                        layout.separator()
                                        layout.prop(o, "mortar_color", icon="COLOR")
                                        layout.prop(o, "mortar_bump")
                                        layout.prop(o, "bump_type", icon="SMOOTHCURVE")
                                        if o.bump_type != "4":
                                            layout.prop(o, "brick_bump")
                                            layout.prop(o, "bump_scale")
                                    if o.mat == "6":
                                        layout.separator()
                                        layout.prop(o, "mortar_color", icon="COLOR")
                                        layout.prop(o, "mortar_bump")
                                        layout.prop(o, "bump_scale")
                                    layout.separator()
                                    layout.operator("mesh.jarch_siding_materials", icon="MATERIAL")
                                    layout.separator()
                                    layout.prop(o, "is_preview", icon="SCENE")
                                layout.separator()
                                layout.separator()
                                layout.operator("mesh.jarch_siding_update", icon="FILE_REFRESH")
                                layout.operator("mesh.jarch_siding_mesh", icon="OUTLINER_OB_MESH")
                                layout.operator("mesh.jarch_siding_delete", icon="CANCEL")
                            else:
                                if o.f_object_add == "none" and o.s_object_add == "none" and o.ro_object_add == "none" and o.object_add != "mesh":
                                    layout.operator("mesh.jarch_siding_convert")
                                elif o.object_add == "mesh":
                                    layout.label("This Is A Mesh JARCH Vis Object", icon="INFO")
                        else:
                            layout.label("This Is Already A JARCH Vis Object", icon="POTATO")
                    else:
                        layout.label("Only Mesh Objects Can Be Used", icon="ERROR")
                else:
                    layout.operator("mesh.jarch_siding_add", text="Add Siding", icon="UV_ISLANDSEL")
# flooring
        layout = self.layout
        ob = context.object
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTFloorDrop", icon="TRIA_DOWN")
        if FLOORDROP:
            if bpy.context.mode == "EDIT_MESH":
                layout.label("JARCH Vis Doesn't Work In Edit Mode", icon="ERROR")
            else:
                o = context.object
                if o != None:
                    if o.type == "MESH":
                        if o.object_add == "none" and o.s_object_add == "none" and o.ro_object_add == "none":
                            if o.f_object_add in ("convert", "add"):
                                layout.label("Material:")
                                layout.prop(o, "f_mat", icon="MATERIAL")
                                layout.label("Types:")
                                if o.f_mat == "1":
                                    layout.prop(o, "f_if_wood", icon="OBJECT_DATA")
                                elif o.f_mat == "2":
                                    layout.prop(o, "f_if_tile", icon="OBJECT_DATA")
                                layout.separator()
                                if o.f_object_add == "add":
                                    layout.prop(o, "f_over_width")
                                    layout.prop(o, "f_over_length")
                                    layout.separator()
                                #width and lengths
                                layout.prop(o, "f_thickness")
                                layout.separator()

                                if o.f_mat == "1":
                                    layout.prop(o, "f_b_width")

                                    if o.f_if_wood == "1":
                                        layout.prop(o, "f_b_length")
                                    layout.separator()

                                    if o.f_if_wood == "1":
                                        layout.prop(o, "f_is_length_vary", icon="NLA")
                                        if o.f_is_length_vary == True:
                                            layout.prop(o, "f_length_vary")
                                            layout.prop(o, "f_max_boards")
                                            layout.separator()
                                        layout.prop(o, "f_is_width_vary", icon="UV_ISLANDSEL")
                                        if o.f_is_width_vary == True:
                                            layout.prop(o, "f_width_vary")
                                            layout.separator()
                                        layout.prop(o, "f_is_ran_height", icon="RNDCURVE")
                                        if o.f_is_ran_height == True:
                                            layout.prop(o, "f_ran_height")
                                        layout.separator()
                                        layout.prop(o, "f_space_w")
                                        layout.prop(o, "f_space_l")
                                        layout.separator()

                                    elif o.f_if_wood in ("3", "4"):
                                        layout.prop(o, "f_b_length2")
                                        layout.prop(o, "f_hb_direction")
                                        layout.separator()

                                    if o.f_if_wood != "1":
                                        layout.prop(o, "f_spacing")
                                        layout.separator()
                                    if o.f_if_wood == "2":
                                        layout.prop(o, "f_num_boards")
                                        layout.separator()

                                    # bevel
                                    layout.prop(o, "f_is_bevel", icon="MOD_BEVEL")
                                    if o.f_is_bevel == True:
                                        layout.prop(o, "f_res", icon="OUTLINER_DATA_CURVE")
                                        layout.prop(o, "f_bevel_amo")
                                        layout.separator()

                                elif o.f_mat == "2":
                                    if o.f_if_tile != "4":
                                        layout.prop(o, "f_t_width")
                                        layout.prop(o, "f_t_length")
                                        layout.separator()
                                    else:
                                        layout.prop(o, "f_t_width2")
                                        layout.separator()
                                    if o.f_if_tile == "1":
                                        layout.prop(o, "f_is_offset", icon="OOPS")
                                        if o.f_is_offset == True:
                                            layout.prop(o, "f_is_random_offset", icon="NLA")
                                            if o.f_is_random_offset == False:
                                                layout.prop(o, "f_offset")
                                            else:
                                                layout.prop(o, "f_offset_vary")
                                        layout.separator()
                                    layout.prop(o, "f_grout_depth")
                                    layout.prop(o, "f_spacing")
                                    layout.separator()
                                layout.prop(o, "f_unwrap", icon="GROUP_UVS")

                                if o.f_unwrap == True:
                                    layout.prop(o, "f_random_uv", icon="RNDCURVE")
                                layout.separator()

                                if context.scene.render.engine == "CYCLES":
                                    layout.prop(o, "f_is_material", icon="MATERIAL")
                                else:
                                    layout.label("Materials Only Supported With Cycles", icon="POTATO")

                                if o.f_is_material == True and context.scene.render.engine == "CYCLES":
                                    layout.separator()
                                    layout.prop(o, "f_col_image", icon="COLOR")
                                    layout.prop(o, "f_is_bump", icon="SMOOTHCURVE")
                                    if o.f_is_bump == True:
                                        layout.prop(o, "f_norm_image", icon="TEXTURE")
                                        layout.prop(o, "f_bump_amo")
                                    layout.prop(o, "f_im_scale", icon="MAN_SCALE")
                                    layout.prop(o, "f_is_rotate", icon="MAN_ROT")
                                    if o.f_mat == "2":
                                        layout.separator()
                                        layout.prop(o, "f_mortar_color", icon="COLOR")
                                        layout.prop(o, "f_mortar_bump")
                                    layout.separator()
                                    layout.operator("mesh.jarch_flooring_materials", icon="MATERIAL")
                                    layout.separator()
                                    layout.prop(o, "f_is_preview", icon="SCENE")
                                layout.separator()
                                layout.operator("mesh.jarch_flooring_update", icon="FILE_REFRESH")
                                layout.operator("mesh.jarch_flooring_mesh", icon="OUTLINER_OB_MESH")
                                layout.operator("mesh.jarch_flooring_delete", icon="CANCEL")
                            else:
                                if o.f_object_add == "none" and o.s_object_add == "none" and o.ro_object_add == "none" and o.f_object_add != "mesh":
                                    layout.operator("mesh.jarch_flooring_convert")
                                elif o.f_object_add == "mesh":
                                    layout.label("This Is A Mesh JARCH Vis Object", icon="INFO")
                        else:
                            layout.label("This Is Already A JARCH Vis Object", icon="POTATO")
                    else:
                        layout.label("Only Mesh Objects Can Be Used", icon="ERROR")
                else:
                    layout.operator("mesh.jarch_flooring_add", text="Add Flooring", icon="MESH_GRID")

# Stairs
        layout = self.layout
        ob = context.object
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTStairDrop", icon="TRIA_DOWN")
        if STAIRDROP:
            o = context.object
            if bpy.context.mode == "EDIT_MESH":
                layout.label("JARCH Vis Doesn't Work In Edit Mode", icon="ERROR")
            else:
                if o != None:
                    if o.object_add == "none" and o.f_object_add == "none" and o.ro_object_add == "none":
                        if o.s_object_add != "mesh":
                            if o.s_object_add == "add":
                                layout.label("Style:", icon="OBJECT_DATA")
                                layout.prop(o, "s_style")
                                layout.separator()
                                layout.prop(o, "s_width")
                                layout.separator()

                                if o.s_style != "3":
                                    layout.prop(o, "s_num_steps")
                                else:
                                    layout.prop(o, "s_num_steps2")

                                # if not spiral stairs
                                if o.s_style != "3":
                                    layout.prop(o, "s_tread_width")

                                layout.prop(o, "s_riser_height")

                                # show height
                                h = round((o.s_num_steps * o.s_riser_height) + (1 / 39.3701), 2)
                                if context.scene.unit_settings.system == "IMPERIAL":
                                    layout.label("Height: " + str(round(((h * 39.3701) / 12), 2)) + " ft", icon="INFO")
                                    layout.separator()
                                else:
                                    layout.label("Height: " + str(round(h, 2)) + " m", icon="INFO")
                                    layout.separator()

                                if o.s_style == "1":
                                    layout.prop(o, "s_is_set_in", icon="OOPS")

                                    # ask if you want custom treads
                                    if o.s_is_set_in == False:
                                        layout.separator()
                                        layout.prop(o, "s_is_custom_tread", icon="OBJECT_DATAMODE")
                                        if o.s_is_custom_tread == True:
                                            layout.prop_search(o, "s_custom_tread", context.scene, "objects")
                                        layout.separator()

                                    if o.s_is_set_in == False:
                                        layout.prop(o, "s_is_close", icon="AUTOMERGE_ON")
                                        layout.prop(o, "s_is_light", icon="OUTLINER_OB_LAMP")
                                if o.s_is_set_in == False and o.s_style != "3":
                                    layout.separator()
                                    if o.s_style == "1":
                                        layout.label("Overhang Style:", icon="OUTLINER_OB_SURFACE")
                                        layout.prop(o, "s_overhang")
                                    layout.prop(o, "s_over_front")
                                    if o.s_overhang != "1":
                                        layout.prop(o, "s_over_sides")
                                    if o.s_style == "1":
                                        layout.separator()
                                        layout.prop(o, "s_is_riser", icon="TRIA_UP")
                                    layout.separator()
                                else:
                                    layout.prop(o, "s_over_front")
                                    layout.separator()

                                # normal stairs
                                if o.s_style == "1":  # normal stairs
                                    layout.separator()
                                    layout.prop(o, "s_num_land")
                                    if o.s_num_land > 0:
                                        layout.prop(o, "s_is_landing", icon="FULLSCREEN")

                                    # for each landing
                                    for i in range(int(o.s_num_land)):
                                        layout.separator()
                                        layout.separator()
                                        box = layout.box()
                                        box.label("Stair Set " + str(i + 2) + ":", icon="MOD_ARRAY")
                                        box.separator()
                                        box.prop(o, "s_num_steps" + str(i))

                                        if o.s_is_custom_tread == True:
                                            box.prop(o, "s_tread_width" + str(i))
                                            box.prop(o, "s_riser_height" + str(i))

                                        # display height
                                        if i == 0:
                                            h2 = h + round((o.s_riser_height0 * o.s_num_steps0) + o.s_riser_height + (1 / 39.3701), 2)
                                            if context.scene.unit_settings.system == "IMPERIAL":
                                                box.label("Height: " + str(round(((h2 * 39.3701) / 12), 2)) + " ft", icon="INFO")
                                            else:
                                                box.label("Height: " + str(round(h2, 2)) + " m", icon="INFO")
                                        else:
                                            h2 = h + round((o.s_riser_height0 * o.s_num_steps0) + (o.s_riser_height0 * o.s_num_steps0) + (2 / 39.3701) + o.s_riser_height + o.s_riser_height0, 2)
                                            if context.scene.unit_settings.system == "IMPERIAL":
                                                box.label("Height: " + str(round(((h2 * 39.3701) / 12), 2)) + " ft", icon="INFO")
                                            else:
                                                box.label("Height: " + str(round(h2, 2)) + " m", icon="INFO")

                                        box.separator()
                                        box.label("Landing " + str(i + 1) + " Rotation:")
                                        box.prop(o, "s_landing_rot" + str(i))

                                        if (i == 0 and o.s_landing_rot0 != "1") or (i == 1 and o.s_landing_rot1 != "1"):
                                            box.prop(o, "s_is_back" + str(i), icon="LOOP_BACK")
                                        box.prop(o, "s_landing_depth" + str(i))

                                        # if steps are not set in then allow adjustment of overhang and stuff
                                        if o.s_is_set_in == False:
                                            box.separator()
                                            box.label("Overhang Style:", icon="OUTLINER_OB_SURFACE")
                                            box.prop(o, "s_overhang" + str(i))
                                            box.prop(o, "s_over_front" + str(i))
                                            if (i == 0 and o.s_overhang0 != "1") or (i == 1 and o.s_overhang1 != "1"):
                                                box.prop(o, "s_over_sides" + str(i))

                                elif o.s_style == "2":  # winding stairs
                                    layout.prop(o, "s_num_rot")
                                    row = self.layout.row()
                                    row.label("Rotation: ")
                                    row.prop(o, "s_w_rot")
                                elif o.s_style == "3":  # spiral stairs
                                    layout.prop(o, "s_rot", icon="MAN_ROT")
                                    layout.prop(o, "s_tread_res")
                                    layout.separator()
                                    layout.prop(o, "s_pole_dia")
                                    layout.prop(o, "s_pole_res")
                                # materials
                                layout.separator()
                                layout.prop(o, "s_unwrap", icon="GROUP_UVS")
                                if o.s_unwrap == True:
                                    layout.prop(o, "s_random_uv", icon="RNDCURVE")
                                layout.separator()
                                if context.scene.render.engine == "CYCLES":
                                    layout.prop(o, "s_is_material", icon="MATERIAL")
                                else:
                                    layout.label("Materials Only Supported With Cycles", icon="POTATO")
                                layout.separator()
                                if o.s_is_material == True and context.scene.render.engine == "CYCLES":
                                    # steps
                                    box = layout.box()
                                    box.label("Stairs:")
                                    box.prop(o, "s_col_image", icon="COLOR")
                                    box.prop(o, "s_is_bump", icon="SMOOTHCURVE")
                                    box.separator()
                                    if o.s_is_bump == True:
                                        box.prop(o, "s_norm_image", icon="TEXTURE")
                                        box.prop(o, "s_bump_amo")
                                    box.prop(o, "s_im_scale", icon="MAN_SCALE")
                                    box.prop(o, "s_is_rotate", icon="MAN_ROT")
                                    # pole/jacks
                                    layout.separator()
                                    if o.s_style in ("1", "3"):
                                        box = layout.box()
                                        if o.s_style == "1":
                                            box.label("Jacks:")
                                        else:
                                            box.label("Pole:")
                                        box.prop(o, "s_col_image2", icon="COLOR")
                                        box.prop(o, "s_is_bump2", icon="SMOOTHCURVE")
                                        box.separator()
                                        if o.s_is_bump2 == True:
                                            box.prop(o, "s_norm_image2", icon="TEXTURE")
                                            box.prop(o, "s_bump_amo2")
                                        box.prop(o, "s_im_scale2", icon="MAN_SCALE")
                                        box.prop(o, "s_is_rotate2", icon="MAN_ROT")
                                    layout.separator()
                                    layout.operator("mesh.jarch_stairs_materials", icon="MATERIAL")
                                # operators
                                layout.separator()
                                layout.separator()
                                layout.operator("mesh.jarch_stairs_update", icon="FILE_REFRESH")
                                layout.operator("mesh.jarch_stairs_mesh", icon="OUTLINER_OB_MESH")
                                layout.operator("mesh.jarch_stairs_delete", icon="CANCEL")
                            else:
                                layout.operator("mesh.jarch_stairs_add", icon="MOD_ARRAY")
                        else:
                            layout.label("This Is A Mesh JARCH Vis Object", icon="INFO")
                    else:
                        layout.label("This Is Already A JARCH Vis Object", icon="POTATO")
                else:
                    layout.operator("mesh.jarch_stairs_add", icon="MOD_ARRAY")

# Roof
        layout = self.layout
        ob = context.object
        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
#        row.alignment = 'CENTER'
        row.prop(scene, "UTRoofDrop", icon="TRIA_DOWN")
        if ROOFDROP:
            ob = context.object

            # if in edit mode layout UIlist
            if ob != None:
                if ob.object_add == "none" and ob.s_object_add == "none" and ob.f_object_add == "none":
                    if context.mode == "EDIT_MESH" and ob.ro_object_add == "none":
                        layout.template_list("OBJECT_UL_face_groups", "", ob, "face_groups", ob, "group_index")
                        layout.separator()
                        layout.prop(ob, "pl_z_rot")
                        layout.prop(ob, "pl_pitch")
                        layout.separator()
                        layout.operator("mesh.jarch_vis_roofing_update_helper", icon="FILE_TICK")
                        layout.separator()
                        layout.operator("mesh.jarch_vis_add_item", icon="ZOOMIN")
                        layout.operator("mesh.jarch_vis_remove_item", icon="ZOOMOUT")
                        layout.operator("mesh.jarch_vis_update_item", icon="FILE_REFRESH")

                    elif context.mode == "EDIT_MESH" and ob.ro_object_add != "none":
                        layout.label("This Object Is Already A JARCH Vis: Siding Object", icon="INFO")

                    # if in object mode and there are face groups
                    if (context.mode == "OBJECT" and len(ob.face_groups) >= 1 and ob.ro_object_add == "convert") or ob.ro_object_add == "add":
                        if ob.ro_object_add != "convert":
                            layout.prop(ob, "ro_mat", icon="MATERIAL")
                        else:
                            layout.label("Material: Tin", icon="MATERIAL")

                        if ob.ro_mat == "1":
                            layout.prop(ob, "ro_tin")
                        elif ob.ro_mat == "2":
                            layout.prop(ob, "ro_shingles")

                        layout.separator()

                        if ob.ro_object_add != "convert":
                            layout.prop(ob, "ro_length")
                            layout.prop(ob, "ro_width")
                            layout.prop(ob, "ro_slope")
                            layout.separator()
                            layout.prop(ob, "ro_mirror", icon="MOD_MIRROR")

                        layout.separator()

                        if ob.ro_mat == "3":
                            layout.prop(ob, "ro_tile_radius")
                            layout.prop(ob, "ro_res")

                        # uv stuff
                        layout.prop(ob, "ro_unwrap", icon="GROUP_UVS")
                        layout.prop(ob, "ro_random_uv", icon="RNDCURVE")

                        # materials
                        layout.separator()
                        if context.scene.render.engine == "CYCLES":
                            layout.prop(ob, "ro_is_material", icon="MATERIAL")
                        else:
                            layout.label("Materials Only Supported With Cycles", icon="POTATO")

                        if ob.ro_is_material == True and context.scene.render.engine == "CYCLES":
                            layout.separator()
                            if ob.ro_mat == "1":  # tin
                                layout.prop(ob, "ro_color")

                            elif ob.ro_mat in ("2", "3"):  # shingles and terra cotta
                                layout.prop(ob, "ro_col_image", icon="COLOR")
                                layout.prop(ob, "ro_is_bump", icon="SMOOTHCURVE")

                                if ob.ro_is_bump == True:
                                    layout.prop(ob, "ro_norm_image", icon="TEXTURE")
                                    layout.prop(ob, "ro_bump_amo")

                                layout.prop(ob, "ro_im_scale")
                                layout.separator()
                                layout.prop(ob, "ro_is_rotate", icon="MAN_ROT")

                            layout.separator()
                            layout.operator("mesh.jarch_roofing_materials", icon="MATERIAL")
                            layout.separator()
                            layout.prop(ob, "ro_is_preview", icon="SCENE")

                        # operators
                        layout.separator()
                        layout.operator("mesh.jarch_roofing_update", icon="FILE_REFRESH")
                        layout.operator("mesh.jarch_roofing_mesh", icon="OUTLINER_OB_MESH")
                        layout.operator("mesh.jarch_roofing_delete", icon="CANCEL")

                    elif ob.ro_object_add == "none" and context.mode == "OBJECT" and len(ob.face_groups) == 0:
                        layout.label("Enter Edit Mode And Create Face Groups", icon="ERROR")

                    # if object has
                    elif ob.ro_object_add == "none" and context.mode == "OBJECT" and len(ob.face_groups) >= 1:
                        layout.operator("mesh.jarch_roofing_convert")
                elif ob.ro_object_add == "mesh":
                    layout.label("This Is Already A JARCH Vis Object", icon="POTATO")
            else:
                layout.operator("mesh.jarch_roofing_add", icon="LINCURVE")


class INFO_MT_mesh_jarch_menu_add(bpy.types.Menu):
    bl_idname = "INFO_MT_mesh_jarch_menu_add"
    bl_label = "JARCH Vis"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.jarch_flooring_add", text="Add Flooring", icon="MESH_GRID")
        layout.operator("mesh.jarch_roofing_add", text="Add Roofing", icon="LINCURVE")
        layout.operator("mesh.jarch_siding_add", text="Add Siding", icon="UV_ISLANDSEL")
        layout.operator("mesh.jarch_stairs_add", text="Add Stairs", icon="MOD_ARRAY")


def menu_add(self, context):
    self.layout.menu("INFO_MT_mesh_jarch_menu_add", icon="PLUGIN")

# define scene props
class jarchvis_scene_props(PropertyGroup):


    bpy.types.Scene.UTSidingDrop = bpy.props.BoolProperty(
        name="Siding",
        default=False,
        description="Add Siding")
    bpy.types.Scene.UTFloorDrop = bpy.props.BoolProperty(
        name="Floor",
        default=False,
        description="Add Floor")
    bpy.types.Scene.UTStairDrop = bpy.props.BoolProperty(
        name="Stair",
        default=False,
        description="Add Stair")
    bpy.types.Scene.UTRoofDrop = bpy.props.BoolProperty(
        name="Roof",
        default=False,
        description="Add Roof")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_add)
    bpy.types.Object.face_groups = CollectionProperty(type=FaceGroup)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.face_groups

if __name__ == "__main__":
    register()
