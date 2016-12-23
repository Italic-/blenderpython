import bpy
import bmesh
from math import radians
from math import degrees
import mathutils
from mathutils.geometry import normal

bl_info = {
    "name": "Trim Tools",
    "description": "Trim mesh with Knife Trim and Trim from selection",
    "author": "Bartosz Styperek",
    "version": (0, 0, 1),
    "blender": (2, 75, 0),
    "location": "View3D",
    "warning": "This is an unstable version",
    "wiki_url": "",
    "category": "Mesh" }

bpy.types.Scene.trim_type = bpy.props.EnumProperty(name = "Trim type", default = "DISSOLVE",
                                    items = (("DISSOLVE","Dissolve",""),
                                            ("KDTREE", "KDTree Search", "")))


class TrimView(bpy.types.Panel):
    bl_idname = "trim_view"
    bl_label = "Trim View"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_context = "mesh_edit"

    def draw(self, context):
        trim = context.scene
        layout = self.layout
        layout.operator("mesh.bisect_w_knife_macro")
        layout.operator("mesh.trim_by_selection")
        layout.prop(trim, 'trim_type', text = "Trim Type")


class BisectKnife(bpy.types.Macro):
    """Overall macro declaration - knife then delete"""
    bl_idname = "mesh.bisect_w_knife_macro"
    bl_label = "Knife Trim"
    bl_options = {'REGISTER',"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'


class selectModeSwitchToEdge(bpy.types.Operator):
    bl_idname = "mesh.mode_switch_edge"
    bl_label = "selectModeSwitchToEdge"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        return {"FINISHED"}

class KnifeTrimCleanup(bpy.types.Operator): #calculate shorter region distance to loop  and selects is.
    bl_idname = "mesh.select_smaller"
    bl_label = "DeleteSmaller"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    @staticmethod
    def reselectMainLoop(MainLoop):
        bpy.ops.mesh.select_all(action='DESELECT') #reselect loop
        for edge in MainLoop:
            edge.select = True

    @staticmethod
    def find_indices_close_vertices(perspectiveMatrixLocalSpace,mainLoopVertList,depth):
        kd = mathutils.kdtree.KDTree(len(mainLoopVertList))
        vertsPerspective = []
        vertPairsList = []
        for i, v in enumerate(mainLoopVertList):

            # translate coordinates to view-space
            tempVert = perspectiveMatrixLocalSpace * mathutils.Vector((v.co[0], v.co[1], v.co[2], 1.0))
            perVertLoc4D = [tempVert.x/tempVert.w, tempVert.y/tempVert.w, 0.0]
            vertsPerspective.append(perVertLoc4D)
            kd.insert( perVertLoc4D,i)
        kd.balance()
        for i,vertPersp in enumerate(vertsPerspective):
            for (co, index, dist) in kd.find_n(vertPersp,depth):
            # print('Distance from i= ',i, ' to index ',index,' is ',dist)
                if dist<0.0001 and index!=i:
                    #print("found pair of verts ", index, " and ", i)
                    vertPairsList.append((index,i))
        return vertPairsList

    def execute(self, context):

        mesh = bpy.context.active_object.data
        bm = bmesh.from_edit_mesh(mesh)
        vectMainLoopCenterLoc = mathutils.Vector((0.0, 0.0, 0.0))
        sumDistanceBiggerRegion = 0.0
        sumDistanceSmallerRegion = 0.0
        biggerCount = 0
        smallerCount = 0
        mainLoopVertCount = 0
        mainLoopVertList = []
        mainLoopEdges = []

        rv3d = context.region_data
        viewPerspectiveMatrix = rv3d.perspective_matrix #.inverted().translation #   view_matrix
        localObjMatrix = context.object.matrix_world #.inverted() #to fix obj local transfomation problem (without it verts get calculated from obj position 0,0,0
        perspectiveMatrixLocalSpace = viewPerspectiveMatrix*localObjMatrix
        depth = 6  # how many verts will be searched in depth for kd-tree - has big influence on speed of script.

        for vert in (vert for vert in bm.verts if vert.select):  #count loop verts
            mainLoopVertCount+=1
            vectMainLoopCenterLoc+=vert.co
            mainLoopVertList.append(vert)

        for edge in (edge for edge in bm.edges if edge.select):  #store original loop made by knife
            mainLoopEdges.append(edge)

        boundaryEdgesList = []
        isBoundary = False
        for loopEdge in mainLoopEdges:
            if loopEdge.is_boundary:
                boundaryEdgesList.append(loopEdge)
                isBoundary = True
            else:
                loopEdge.select = False
        if isBoundary:
            try:
                bmesh.ops.bridge_loops(bm, edges=boundaryEdgesList)
            except:
                self.reselectMainLoop(mainLoopEdges)
                bpy.ops.mesh.loop_to_region(select_bigger=False)
                bpy.ops.mesh.delete(type='FACE')
                self.reselectMainLoop(mainLoopEdges)
                newboundaryEdgesList = []
                for loopEdge in mainLoopEdges:
                    if not loopEdge.is_boundary:
                        loopEdge.select = False
                    else:
                        newboundaryEdgesList.append(loopEdge)
                bpy.ops.mesh.bridge_edge_loops()
                # bmesh.ops.bridge_loops(bm, edges=newboundaryEdgesList)
            bmesh.update_edit_mesh(mesh, tessface=True, destructive=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            return {'FINISHED'}

        self.reselectMainLoop(mainLoopEdges)
        bpy.ops.mesh.loop_to_region(select_bigger=True)
        for vert in (vert for vert in bm.verts if not vert.select):
            smallerCount+=1
            sumDistanceSmallerRegion=sumDistanceSmallerRegion+(vectMainLoopCenterLoc - vert.co).length_squared

        if smallerCount == 0:     # not verts in smaller region of loop so select smaller region (eg when making vedge type of cut on edge)
            self.reselectMainLoop(mainLoopEdges)
            bpy.ops.mesh.loop_to_region(select_bigger=False)

        else:                      # else calculate distance the old way.
            self.reselectMainLoop(mainLoopEdges)
            bpy.ops.mesh.loop_to_region(select_bigger=False)
            for vert in (vert for vert in bm.verts if not vert.select):
                biggerCount+=1
                sumDistanceBiggerRegion=sumDistanceBiggerRegion+(vectMainLoopCenterLoc - vert.co).length_squared

            # print('Smaller count = ', smallerCount,' Bigger count = ', biggerCount, 'Smaller distance= ', sumDistanceSmallerRegion, ' Bigger distance= ', sumDistanceBiggerRegion)
            self.reselectMainLoop(mainLoopEdges)
            if sumDistanceBiggerRegion < sumDistanceSmallerRegion:  # compare distance from bigger and smaller region selection
                bpy.ops.mesh.loop_to_region(select_bigger=True) #bigger part is close to middle loop so mark it for deletion
            else:
                bpy.ops.mesh.loop_to_region(select_bigger=False)

        if not(biggerCount==0 and smallerCount==0):
            try:
                bpy.ops.mesh.delete(type='FACE')
                self.reselectMainLoop(mainLoopEdges)
                fillResult = bmesh.ops.triangle_fill(bm,use_beauty=False,use_dissolve=True, edges=mainLoopEdges) #works best
                # __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
                generatedFaces = []
                for geo in fillResult:
                    if type(geo) is bmesh.types.BMFace:
                        generatedFaces.append(geo)
                bmesh.ops.recalc_face_normals(bm, faces=generatedFaces)
                # bmesh.ops.dissolve_verts(bm, mainLoopVertList, use_face_split=True, use_boundary_tear=False)
                # bpy.ops.mesh.dissolve_faces()
            except:
                self.report({'ERROR'}, message="Failed to dissolve face. It is possible trim was not started/finished outside mesh.. Cancelling")
                return {'CANCELLED'}
        else: #eg when knife over edge this may happen
            self.reselectMainLoop(mainLoopEdges)  #last try to dissolve
            bpy.context.tool_settings.mesh_select_mode = [True, False, False]
            try:
                bpy.ops.mesh.dissolve_faces()
            except:
                self.report({'ERROR'}, message="Failed to dissolve face. It is possible trim was not started/finished outside mesh.. Cancelling")
                return {'CANCELLED'}

        trim = context.scene.trim_type
        if trim =='KDTREE':
            for face in (face for face in bm.faces if face.select):
                faceVertsCopy = face.verts[:]  #because face will change after conecting_verts so store it
                for x,y in self.find_indices_close_vertices(perspectiveMatrixLocalSpace,face.verts[:],depth):  # x,y - indexes of faces to connect
                    # print('********** conntcing verts   ', faceVertsCopy[x].index, ' with   ', faceVertsCopy[y].index)
                    edges = bmesh.ops.connect_verts(bm, verts=[faceVertsCopy[x],faceVertsCopy[y]])
                    # for edge in edges['edges']:
                    #     print('created edge: ', edge.index)

        elif trim=='DISSOLVE':
            activeFace =[]    #for spliting big ngon into planar faces with connect_verts_nonplanar()
            for faces in bm.faces:
                if faces.select:
                    activeFace.append(faces)
            bmesh.ops.connect_verts_nonplanar(bm, angle_limit =0.001, faces =activeFace)


        # bm.select_flush_mode()
        bmesh.update_edit_mesh(mesh, tessface=True, destructive=True)
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bm.free()
        return {"FINISHED"}

class ThreePointTrim(bpy.types.Operator):
    bl_idname = "mesh.trim_by_selection"
    bl_label = "Trim by selection"
    bl_description = "Trims mesh based on selected vertices. Works only in vertex mode."
    bl_options = {"REGISTER","UNDO"}

    clearOut = bpy.props.BoolProperty(default=True,name="Trim direction flip")
    Depth = bpy.props.FloatProperty(default=0.0,name="Depth")
    TrimRoll = bpy.props.FloatProperty(default=0.0,name="Yaw")
    TripPitch = bpy.props.FloatProperty(default=0.0,name="Pitch")

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.select_history.validate()
        vertCount = 0
        selectedVerts = []
        for vert in (vert for vert in bm.verts if vert.select):  #count loop verts
            vertCount+=1
            if len(selectedVerts)<3:
                selectedVerts.append(vert)

        if vertCount < 1:
            self.report({'INFO'}, 'Select at least one vertex')
            return {'CANCELLED'}


        vertsMedianLoc = mathutils.Vector((0.0 ,0.0 ,0.0))
        vertsMedianNorm = mathutils.Vector((0.0 ,0.0 ,0.0))
        vertsCoordList = []
        vectOffset = mathutils.Vector((0.0, 0.0, self.Depth))
        offsetMatrix = mathutils.Matrix.Translation(vectOffset)
        yawMatrix = mathutils.Matrix.Rotation(radians(self.TrimRoll), 4, 'X')
        pitchMatrix = mathutils.Matrix.Rotation(radians(self.TripPitch), 4, 'Y')

        for vert in selectedVerts:
            vertsMedianLoc+=vert.co
            vertsCoordList.append(vert.co)
            vertsMedianNorm+=vert.normal
        vertsMedianLoc /= len(selectedVerts)
        if vertCount>2:
            trisNorm=normal(vertsCoordList)
            if degrees(vertsMedianNorm.angle(trisNorm))>90:
                vertsMedianNorm= trisNorm*(-1)
            else:
                vertsMedianNorm = trisNorm
        if vertCount==2:  #fixes normal for 2 verts
            vectorV1_V2=selectedVerts[0].co-selectedVerts[1].co
            perpendicular= vectorV1_V2.cross(vertsMedianNorm)
            vertsMedianNorm = perpendicular.cross(vectorV1_V2)


        normToRotation = vertsMedianNorm.to_track_quat('Z', 'X').to_euler()
        selectionLocalMatrix = mathutils.Matrix.Translation(vertsMedianLoc)
        selectionLocalMatrix *= selectionLocalMatrix.Rotation(normToRotation[2], 4, 'Z')
        selectionLocalMatrix *= selectionLocalMatrix.Rotation(normToRotation[1], 4, 'Y')
        selectionLocalMatrix *= selectionLocalMatrix.Rotation(normToRotation[0], 4, 'X')

        spaceMatrixTransform = context.object.matrix_world*selectionLocalMatrix*offsetMatrix*yawMatrix*pitchMatrix

        loc = spaceMatrixTransform.to_translation()
        norm = spaceMatrixTransform.to_3x3()*mathutils.Vector((0.0, 0.0, 1.0))
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=loc, plane_no=norm, use_fill=True, clear_inner= not self.clearOut, clear_outer=self.clearOut)
        bpy.ops.mesh.select_all(action='DESELECT')
        bmesh.update_edit_mesh(me, True)
        return {"FINISHED"}

    
    
def register():
    bpy.utils.register_module(__name__)
    deselect = BisectKnife.define("MESH_OT_select_all")
    deselect.properties.action = 'DESELECT'
    BisectKnife.define("MESH_OT_mode_switch_edge")
    op = BisectKnife.define("MESH_OT_knife_tool")
    op.properties.use_occlude_geometry = False
    op.properties.only_selected = False
    BisectKnife.define("MESH_OT_select_smaller")
    # sel=BisectKnife.define("MESH_OT_select_all")
    # sel.action = 'DESELECT'

def unregister():
    bpy.utils.unregister_module(__name__)