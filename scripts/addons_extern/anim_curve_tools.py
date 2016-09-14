# ***** BEGIN GPL LICENSE BLOCK *****
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# ***** END GPL LICENCE BLOCK *****
#
# (c) 2011 Phil Cote (cotejrp1)

bl_info = {
    'name': 'F-Curve Tools',
    'author': 'cotejrp1',
    'version': (0, 1),
    "blender": (2, 6, 4),
    'location': 'Graph Editor -> Properties -> F-Curve Tools',
    'description': 'Manipulates animation f-curves',
    'warning': '',
    'category': 'Animation'}

import bpy
from bpy.props import IntProperty, BoolProperty, EnumProperty


# quick handy little list functions.
def first(lst):
    return lst[0]


def last(lst):
    return lst[-1]


def chunks(lst, n):
    """
    Taken from stack overflow so to easily split off keypoints into pairs.
    Credit due here...
    http://stackoverflow.com/questions/
    312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def swap_pair(pair):

    def swap_ys(p1, p2):
        p1.co.y, p2.co.y = p2.co.y, p1.co.y

    def get_handle_diff(pt):
        left_diff = pt.handle_left.y - pt.co.y
        right_diff = pt.handle_right.y - pt.co.y
        return left_diff, right_diff

    # get the handle relative diff in advance before swapping
    left_diff_0, right_diff_0 = get_handle_diff(pair[0])
    left_diff_1, right_diff_1 = get_handle_diff(pair[1])

    # do the coordinate swap
    y1, y2 = pair[0].co.y, pair[1].co.y
    pair[0].co.y, pair[1].co.y = y2, y1

    # update the handles
    pair[0].handle_left.y = pair[0].co.y + left_diff_0
    pair[0].handle_right.y = pair[0].co.y + right_diff_0

    pair[1].handle_left.y = pair[1].co.y + left_diff_1
    pair[1].handle_right.y = pair[1].co.y + right_diff_1


def get_key_points(context):
    ob = context.object
    fcurves = ob.animation_data.action.fcurves
    fcurve = [x for x in fcurves if x.select][-1]
    kps = fcurve.keyframe_points
    return kps


def op_rules(context):
    """
    Poll rules for all curve operators.
    """
    # there has to be a selected object
    ob = context.active_object
    if ob is None:
        return False

    if context.area.spaces.active.mode == "DRIVERS":
        return False

    # there has to be one and only one curve selected
    sel_curves = [x for x in ob.animation_data.action.fcurves
                  if x.select]
    if len(sel_curves) != 1:
        return False

    # curve in question cannot be locked.
    if sel_curves[0].lock:
        return False

    return True


class KeyCurveSwitchOp(bpy.types.Operator):
    """Switches heights for selected keyframes.
    NOTE: Only works when just one curve is selected"""
    bl_idname = "anim.keycurve_switcher"
    bl_label = "Flip Keyframe Points"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return op_rules(context)

    def execute(self, context):
        kps = get_key_points(context)
        kps = [kp for kp in kps if kp.select_control_point]
        kps_pairs = list(chunks(kps, 2))
        kps_pairs = filter(lambda l: len(l) > 1, kps_pairs)

        for pair in kps_pairs:
            swap_pair(pair)

        return {'FINISHED'}


class KeySelectionOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "animation.key_selection_op"
    bl_label = "Key Selection Operator"

    nth = IntProperty(name="Nth vert", min=1, max=10)

    @classmethod
    def poll(cls, context):
        return op_rules(context)

    def execute(self, context):
        ob = context.object
        nth = ob.everyNth
        left_offset = ob.left_offset
        right_offset = -ob.right_offset if ob.right_offset != 0 else None

        kps = get_key_points(context)

        def set_cp(cp, sel):
            cp.select_control_point = sel
            cp.select_left_handle = ob.checkLeftHandle and sel
            cp.select_right_handle = ob.checkRightHandle and sel

        # deselecting ensures that offsets are taken into account.
        for cp in kps:
            set_cp(cp, False)

        # do the selections
        for i, x in enumerate(kps[left_offset:right_offset]):
            sel_pt = i % nth == 0
            set_cp(x, sel_pt)

        return {'FINISHED'}


class AlignKeyframeOperator(bpy.types.Operator):
    bl_idname = "anim.align_keys"
    bl_label = "Align Selected Key Points"

    @classmethod
    def poll(cls, context):
        other_rules_passed = op_rules(context)
        if not other_rules_passed:
            return False

        # selected curve has to have 2 or more selected points
        kps = get_key_points(context)
        pts = [x for x in kps if x.select_control_point]
        return len(pts) >= 2

    def execute(self, context):
        ob = context.object
        kps = get_key_points(context)
        kps = [x for x in kps if x.select_control_point]

        f = max if ob.top_or_bottom.startswith("high") else min
        max_y_val = f([x.co.y for x in kps])

        for kp in kps:
            left_diff_y = kp.co.y - kp.handle_left.y
            right_diff_y = kp.co.y - kp.handle_right.y
            kp.co.y = max_y_val
            kp.handle_left.y = max_y_val + left_diff_y
            kp.handle_right.y = max_y_val + right_diff_y

        return {'FINISHED'}


class EvenOutHandlesOperator(bpy.types.Operator):
    bl_idname = "anim.evenout_handles"
    bl_label = "Even Out Handles"

    @classmethod
    def poll(cls, context):
        return op_rules(context)

    def execute(self, context):
        handle_choice = context.object.handle_choice

        kps = get_key_points(context)
        kps = [x for x in kps if x.select_control_point]

        if handle_choice == "left":
            for kp in kps:
                diff_y = kp.co.y - kp.handle_left.y
                diff_x = kp.co.x - kp.handle_left.x
                kp.handle_right.x = kp.co.x + diff_x
                kp.handle_right.y = kp.co.y + diff_y
        else:
            for kp in kps:
                diff_y = kp.co.y - kp.handle_right.y
                diff_x = kp.co.x - kp.handle_right.x
                kp.handle_left.x = kp.co.x + diff_x
                kp.handle_left.y = kp.co.y + diff_y

        return {'FINISHED'}


class FCurvePanel(bpy.types.Panel):
    """Creates a Panel in the F-Curve properties region."""
    bl_label = "F-Curve Tools"
    bl_idname = "OBJECT_PT_fcurves"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.label(text="Keypoint Selector")
        row = layout.row()
        row.prop(obj, "checkLeftHandle")
        row.prop(obj, "checkRightHandle")
        row = layout.row()
        row.prop(obj, "everyNth")
        row = layout.row()
        row.label(text="Left/Right Offsets")
        row = layout.row()
        row.prop(obj, "left_offset")
        row.prop(obj, "right_offset")
        row = layout.row()
        row.operator(KeySelectionOperator.bl_idname, text="Select Keys")

        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Keypoint Aligner")
        row = layout.row()
        row.prop(obj, "top_or_bottom")
        row = layout.row()
        row.operator(AlignKeyframeOperator.bl_idname)

        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Keypoint Flipper")
        row = layout.row()
        row.operator(KeyCurveSwitchOp.bl_idname)
        row = layout.row()
        row.separator()
        row = layout.row()
        row.label(text="Even out handles")
        row = layout.row()
        row.prop(obj, "handle_choice")
        row.operator(EvenOutHandlesOperator.bl_idname)


def register():
    ob_type = bpy.types.Object
    ob_type.right_offset = IntProperty(name="Right Offset",
                                       min=0, max=10, default=0,
                                       description="Put Right Offset")

    ob_type.left_offset = IntProperty(name="Left Offset",
                                      min=0, max=10, default=0,
                                      description="Offset val for every nth")
    ob_type.everyNth = IntProperty(name="Every Nth Key",
                                   min=1, max=10, default=2)

    ob_type.checkLeftHandle = BoolProperty(name="Left Handle", default=True)
    ob_type.checkRightHandle = BoolProperty(name="Right Handle", default=True)

    choice_vals = [("highest", "highest", "highest"),
                   ("lowest", "lowest", "lowest"), ]
    ob_type.top_or_bottom = EnumProperty(name="Align Keyframe Points To",
                                         items=choice_vals,
                                         default="highest",
                                         description="Align keyframe points")

    ob_type.handle_choice = EnumProperty(name="Handle to Match",
                                         items=[("left", "left", "left"),
                                                ("right", "right", "right")],
                                         default="left",
                                         description="Which curve handle length to match up with.")

    bpy.utils.register_class(EvenOutHandlesOperator)
    bpy.utils.register_class(KeyCurveSwitchOp)
    bpy.utils.register_class(KeySelectionOperator)
    bpy.utils.register_class(AlignKeyframeOperator)
    bpy.utils.register_class(FCurvePanel)


def unregister():
    bpy.utils.unregister_class(FCurvePanel)
    bpy.utils.unregister_class(AlignKeyframeOperator)
    bpy.utils.unregister_class(EvenOutHandlesOperator)
    bpy.utils.unregister_class(KeyCurveSwitchOp)
    bpy.utils.unregister_class(KeySelectionOperator)

if __name__ == "__main__":
    register()
