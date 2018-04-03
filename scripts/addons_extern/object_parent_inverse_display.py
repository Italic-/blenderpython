"""
Display transforms for an object's parent inverse offset matrix.

Load this script as an add-on through Blender's add-on manager.
This add-on only includes a panel to help visualize and tweak a
child object's parent inverse matrix.

To set the location/rotation/scale fields with python, the properties are at:
Object.parent_inverse_display.location          type: mathutils.Vector      or (float, float, float)
Object.parent_inverse_display.rotation_euler    type: mathutils.Euler
Object.parent_inverse_display.rotation_quat     type: mathutils.Quaternion  or (float, float, float, float)
Object.parent_inverse_display.scale             type: mathutils.Vector      or (float, float, float)

TODO:
Proper matrix scales.
Child-of constraint matrix display.


(c) Jeffrey "italic" Hoover
italic DOT rendezvous AT gmail DOT com

Licensed under the Apache 2.0 license.
This script can be used for non-commercial
and commercial projects free of charge,
although credit would be nice.
For more information, visit:
https://www.apache.org/licenses/LICENSE-2.0
"""


import bpy
from bpy.types import (
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (
    FloatVectorProperty,
    PointerProperty,
)
from mathutils import (
    Matrix,
    Quaternion,
    Euler,
)

bl_info = {
    'name': 'Parent Inverse Display',
    'author': 'italic',
    'description': 'Visualize the parent inverse matrix applied when parenting objects.',
    'category': 'Object',
    'version': (0, 0, 2),
    'blender': (2, 7, 6),
    'location': 'Object Properties Panel -> Parent Inverse Transform',
}


def update_inverse_components(self, context, component):
    ob = context.object
    loc, rot, sca = ob.matrix_parent_inverse.decompose()

    if component == "LOC":
        loc = Matrix.Translation((
            self.location.x,
            self.location.y,
            self.location.z
        ))
    else:
        loc = Matrix.Translation(loc)

    if component == "ROT":
        if ob.rotation_mode == 'QUATERNION':
            rot = Quaternion((
                self.rotation_quat.w,
                self.rotation_quat.x,
                self.rotation_quat.y,
                self.rotation_quat.z
            )).to_matrix().to_4x4()
        elif ob.rotation_mode == "AXIS_ANGLE":
            rot = rot.to_matrix().to_4x4()
        else:
            rot = Euler((
                self.rotation_euler.x,
                self.rotation_euler.y,
                self.rotation_euler.z),
                ob.rotation_mode
            ).to_matrix().to_4x4()
    else:
        rot = rot.to_matrix().to_4x4()

    if component == "SCA":
        scaX = Matrix.Scale(self.scale.x, 4, (1.0, 0.0, 0.0))
        scaY = Matrix.Scale(self.scale.y, 4, (0.0, 1.0, 0.0))
        scaZ = Matrix.Scale(self.scale.z, 4, (0.0, 0.0, 1.0))
        sca = scaX * scaY * scaZ
    else:
        scaX = Matrix.Scale(sca.x, 4, (1.0, 0.0, 0.0))
        scaY = Matrix.Scale(sca.y, 4, (0.0, 1.0, 0.0))
        scaZ = Matrix.Scale(sca.z, 4, (0.0, 0.0, 1.0))
        sca = scaX * scaY * scaZ

    # Produce and update inverse matrix
    ob.matrix_parent_inverse = loc * rot * sca


def update_inverse_loc(self, context):
    update_inverse_components(self, context, "LOC")


def update_inverse_rot(self, context):
    update_inverse_components(self, context, "ROT")


def update_inverse_sca(self, context):
    update_inverse_components(self, context, "SCA")


class OBJECT_OT_inverse_get(Operator):

    """Get object's parent inverse."""

    bl_idname = "object.inverse_get"
    bl_label = "Get parent inverse"

    def execute(self, context):
        ob = context.object
        inv_mat = ob.matrix_parent_inverse
        inv_prop = ob.parent_inverse_display
        loc, rot, sca = inv_mat.decompose()

        inv_prop.location = loc
        if ob.rotation_mode not in ("QUATERNION", "AXIS_ANGLE"):
            inv_prop.rotation_euler = rot.to_euler(ob.rotation_mode)
        inv_prop.rotation_quat = rot
        inv_prop.scale = sca

        return {'FINISHED'}


class OBJECT_OT_inverse_clear(Operator):

    """Clear parent inverse."""

    bl_idname = "object.inverse_clear"
    bl_label = "Clear parent inverse"

    def execute(self, context):
        bpy.ops.object.parent_clear(type='CLEAR_INVERSE')
        bpy.ops.object.inverse_get()

        return {'FINISHED'}


class OBJECT_PT_inverse_display(Panel):

    bl_label = "Parent Inverse Transform"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout
        ob = context.object
        inverse = ob.parent_inverse_display

        col = layout.column()
        col.operator("object.inverse_get", text="Fetch Inverse")
        col.operator("object.inverse_clear", text="Clear Inverse (Reset)")
        row = layout.row()
        row.column().prop(inverse, "location")
        if ob.rotation_mode == "QUATERNION":
            row.column().prop(inverse, "rotation_quat", text="Inverse Rotation")
        elif ob.rotation_mode == "AXIS_ANGLE":
            row.column().label(text="Not for Axis-Angle")
        else:
            row.column().prop(inverse, "rotation_euler", text="Inverse Rotation")

        row.column().prop(inverse, "scale")


class ParentInverseDisplayProps(PropertyGroup):

    location = FloatVectorProperty(
        name="Inverse Location",
        description="Location transform from decomposed parent inverse matrix.",
        options=set(),
        precision=3,
        subtype='TRANSLATION',
        unit='LENGTH',
        size=3,
        update=update_inverse_loc,
    )
    rotation_quat = FloatVectorProperty(
        name="Inverse Quaternion Rotation",
        description="Quaternion rotation transform from decomposed parent inverse matrix.",
        options=set(),
        precision=3,
        subtype='QUATERNION',
        unit='NONE',
        size=4,
        update=update_inverse_rot,
    )
    rotation_euler = FloatVectorProperty(
        name="Inverse Euler Rotation",
        description="Euler rotation transform from decomposed parent inverse matrix.",
        options=set(),
        precision=3,
        subtype='EULER',
        unit='NONE',
        size=3,
        update=update_inverse_rot,
    )
    scale = FloatVectorProperty(
        name="Inverse Scale",
        description="Scale transform from decomposed parent inverse matrix.",
        options=set(),
        precision=3,
        subtype='XYZ',
        unit='NONE',
        size=3,
        update=update_inverse_sca,
    )


classes = (
    ParentInverseDisplayProps,
    OBJECT_PT_inverse_display,
    OBJECT_OT_inverse_get,
    OBJECT_OT_inverse_clear,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.parent_inverse_display = PointerProperty(
        type=ParentInverseDisplayProps,
        name="Parent Inverse Properties",
        description=""
    )


def unregister():
    del bpy.types.Object.parent_inverse_display

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
