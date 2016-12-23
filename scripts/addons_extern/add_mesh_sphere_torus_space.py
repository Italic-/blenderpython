bl_info = {
    "name": "Math Surface Shape",
    "author": "batFINGER",
    "version": (1, 0),
    "blender": (2, 78, 0), # and most prior
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import (FloatVectorProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       StringProperty,
                       )
from bpy.utils import register_class
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from math import * #TODO (quick fix for mapping)

class TorusCoordsPoint:
    @property
    def xyz(self):
        theta = self.theta
        zi = self.zi
        R = self.R
        r = self.r
        a = (R + r * cos(theta))
        x = a * cos(zi)
        y = a * sin(zi)
        z = r * sin(theta)
        return Vector((x,y,z))
    
    def __init__(self, R, r, theta, zi):
        self.theta = theta
        self.zi = zi
        self.R = R
        self.r = r
        #self.xyz = self.point(theta, zi)
        
    def __repr__(self):
        return "TorusCoord(%.4f, %.4f)" % (self.theta, self.zi)     
    
        
class TorusCoords:
    item = ('TOROIDAL', "Toroidal", "Use Torus Space")

    def draw(self, layout, context):
        #print(self, layout, context)
        layout.label("TORUS")
        layout.prop(self, "R")
        layout.prop(self, "r")
        layout.prop(self, "minor_segments")
        layout.prop(self, "major_segments")    

    @property
    def space(self):
        return TorusCoords(self.R, self.r, self.major_segments, self.minor_segments)
                
    props = {"R":FloatProperty(name="Major Radius", default=1.0, min=0.0),
             "r":FloatProperty(name="Minor Radius", default=0.25, min=0.1),
             "major_segments":IntProperty(name="Major Segments", default=48, min=3),
             "minor_segments":IntProperty(name="Minor Segments", default=12, min=3),
             "draw": draw,
             "space": space}

    def point(self, theta, zi):
        return TorusCoordsPoint(self.R, self.r, theta, zi)
    
    def points_rings(self):
        rings = []
        zi_range = radians(360) # TODO
        theta_range = radians(360)
        
        for r in range(self.major_segments + 1):
            zi = r * zi_range / self.major_segments
            ring = [self.point(i * theta_range / self.minor_segments, zi) for i in range(self.minor_segments)]
            #ring.append(ring[0])
            rings.append(ring)
        return rings        
        
    def __init__(self, R, r, major_segments, minor_segments):
        self.R = R
        self.r = r
        self.minor_segments = minor_segments
        self.major_segments = major_segments
   
class SphericalCoordsPoint:
    @property
    def xyz(self):
        theta = self.theta
        zi = self.zi
        x = cos(theta) * sin(zi)
        y = sin(theta) * sin(zi)
        z = cos(zi)
        R = self.R
        return R * Vector((x,y,z))
    
    def __init__(self, R, theta, zi):
        self.R = R
        self.theta = theta
        self.zi = zi
        #self.xyz = self.point(theta, zi)
        
    def __repr__(self):
        return "SphericalCoord(%.4f, %.4f)" % (degrees(self.theta),
                                               degrees(self.zi))            
class SphericalCoords:
    def draw(self, layout, context):
        #print(self, layout, context)
        layout.label("Spherical")
        layout.prop(self, "R")
        layout.prop(self, "rings")
        layout.prop(self, "segments")

    @property
    def space(self):
        return SphericalCoords(self.R, self.rings, self.segments)
       
    def point(self, theta, zi):
        return SphericalCoordsPoint(self.R, theta, zi)
    
    def points_rings(self):
        rings = []
        zi_range = radians(180) # TODO
        theta_range = radians(360)
        
        for r in range(self.rings + 1):
            zi = r * zi_range / self.rings
            ring = [self.point(i * theta_range / self.segments, zi) for i in range(self.segments)]
            #ring.append(ring[0])
            rings.append(ring)
        return rings
       
        
    item = ('SPHERICAL', "Spherical", "Add Spherical Space")
    props = {"R":FloatProperty(name="Radius", default=1.0, min=0.1),
             "segments":IntProperty(name="Segments", default=32, min=3),
             "rings":IntProperty(name="Rings", default=16, min=3),
             "draw":draw,
             "space":space}

    def __init__(self, R, rings, segments):
        self.R = R
        self.rings = rings
        self.segments = segments
        

class OBJECT_OT_add_object_using_space():
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object_from_space"
    bl_label = "Space Mapping"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add Object using Spherical / Toroidal space"
    fx = StringProperty(default="x")
    fy = StringProperty(default="y")
    fz = StringProperty(default="z")
    
    def draw(self, context):
        layout = self.layout
        layout.label("SPACE")
        layout.prop(self, "space")
        space = getattr(self, self.space.lower(), None)
        print(space)
        space.draw(layout, context)
        layout.label("MAPPING")
        layout.prop(self, "fx")
        layout.prop(self, "fy")
        layout.prop(self, "fz")
        col = layout.column()
        col.prop(self, "scale")
        col.prop(self, "location")
        col.prop(self, "view_align")
        rcol = layout.column()
        rcol.enabled = not self.view_align
        rcol.prop(self, "rotation")
        #space.draw()
        
    def add_object(self, context, name):
        print(self, vars(self), self.bl_rna)
        scale_x = self.scale.x
        scale_y = self.scale.y
        bm = bmesh.new()
        # TODO come up with a nicer way to do this.
        space = getattr(self, self.space.lower(), None)
        if not space:
            print("Something horrible happened")
            return {'CANCELLED'}
        rings = space.space.points_rings()

        def map(p):
            x, y, z = p.xyz
            _x = self.scale.x * eval(self.fx)
            _y = self.scale.y * eval(self.fy)
            _z = self.scale.z * eval(self.fz)
            return Vector((_x, _y, _z))
        
        verts0 = [bm.verts.new(map(p)) for p in rings[0]]
        verts0.append(verts0[0])
        for ring in range(1, len(rings)):
                
            verts1 = [bm.verts.new(map(p)) for p in rings[ring]]
            verts1.append(verts1[0]) # make a ring

            faces = [
                bm.faces.new((
                    verts0[i], verts1[i],
                    verts1[i+1], verts0[i+1]
                ))
                for i in range(len(verts0) - 1)
            ]
            verts0 = verts1
            
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        object_data_add(context, mesh, operator=self)
        bm.free()

    def __init__(self): # TODO
        print("INIT")
    
    def execute(self, context):
        self.add_object(context, self.space)

        return {'FINISHED'}

def make_op(spaces):
    items = []
    propdic = {}
    
    for space in spaces:
        enum, name, desc = space.item 
        items.append(space.item)
        # make a pointer from the enum.lower()
        gp = type("%sGroup" % enum, (PropertyGroup,), space.props)
        register_class(gp)
        propdic[enum.lower()] = PointerProperty(type=gp)

    propdic["space"] = EnumProperty(
            items=items,
            name="space",
            default='SPHERICAL',
            description="Use space",
            )
    propdic["scale"] = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )    
    return type("OBJECT_OT_add_object_using_space", (OBJECT_OT_add_object_using_space, Operator, AddObjectHelper,), propdic)

# Registration

def add_object_button(self, context):
    self.layout.operator(
        "mesh.add_object_from_space",
        text="Maths / Space Equations",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping

object_space_op = None
def register():
    object_space_op = make_op([SphericalCoords, TorusCoords])
    register_class(object_space_op)
    #bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)


def unregister():
    if object_space_op:
        bpy.utils.unregister_class(object_space_op)
    #bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()