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

__bpydoc__ = """\
This script is an implementation of the concept of sliding vertices around on edges. 
It is used to finetune/redraw edges/edgeloops through the process of sliding vertices. 
It can be used to slide anything anywhere.
To my knowledge this is a new concept in 3D modelling. Try it and you will see how it can impact your modelling habits. 
You are able to tune vertices by sliding by freehand-redrawing them on the edges they are part of.


This is version 2 of the script, implementing a new graphical user interface and having gone to a complete rewrite of the code,
lifting almost all shortcomings of the old code.


Documentation
The script will work on any vertice/edge/face-selection. 
Make a selection, invoke script.  The selection will be visualized in yellow.
Press and hold left-mouse button and draw freely across the in red visualized, so called "slide-edges".
The respective selected vertices will change position on the slide-edge to the new position you choose
by moving over it with the left mouse-button pressed.
Press ENTER/RETURN to finalize the operation.
Just press the right-mouse-button to cancel the script operation.

HINT: EdgeTune is also vertex-slide.

Version 2 now works in both orthogonal and perspective mode.

Version 2 now doesn't mess with the undo list anymore, plus the script operation can be
undone by pressing standard Ctrl-Z.

Do BEWARE still: EdgeTune, like every other script that changes the mesh, will decompose all FGons in the mesh!
"""


bl_info = {
	"name": "EdgeTune",
	"author": "Gert De Roost",
	"version": (3, 0, 5),
	"blender": (2, 6, 3),
	"location": "View3D > Tools > Deform",
	"description": "Tuning edgeloops by redrawing them manually, sliding verts.",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Mesh"}

if "bpy" in locals():
    import imp
#else:
 #   from . import ETmain
  #  from . import ETdraw


import bpy
from bpy_extras import *
from bgl import *
import math
from mathutils import *
import bmesh


scn = bpy.context.scene
bpy.types.Scene.AutoAdapt = bpy.props.BoolProperty(
name = "Auto Occlusion", 
description = "Occlusion behaviour setting")
scn['AutoAdapt'] = True

#class ToolPropsPanel(bpy.types.Panel):
#	bl_label = "EdgeTune"
#	bl_space_type = "VIEW_3D"
#	bl_region_type = "TOOL_PROPS"

class EdgeTune(bpy.types.Operator):
	bl_idname = "mesh.edgetune"
	bl_label = "Tune Edge"
	bl_description = "Tuning edgeloops by redrawing them manually, sliding verts"
	bl_options = {"REGISTER", "UNDO"}
	
	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return (obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH')

#	def draw(self, context):
#		layout = self.layout
#		layout.operator("mesh.edgetune")
	#	layout.prop(scn, 'AutoAdapt')
#
	def invoke(self, context, event):
		self.save_global_undo = bpy.context.user_preferences.edit.use_global_undo
		bpy.context.user_preferences.edit.use_global_undo = False
		
		do_edgetune(self)
		
		context.window_manager.modal_handler_add(self)
		self._handle2 = context.region.callback_add(adapt, (), 'PRE_VIEW')
		self._handle = context.region.callback_add(redraw, (), 'POST_PIXEL')
		
		return {'RUNNING_MODAL'}

#	def execute(self, context):
#		self.action(context)
#		return {'FINISHED'}

	def modal(self, context, event):
		global matrix, viewwidth, viewheight
		global seledges, selverts, selcoords, vertd, singles, boxes, sverts
		global slideedges, slideverts, slidecoords
		global bm, mesh
		global mbns, inter, viewchange, mouseover, highoff, bx1, bx2, by1, by2, mx, my, vertd
		global space, selobj
		global matrix, rotmat, mat_rotX, mat_rotY, mat_rotZ
		
		inter = 0
		if event.type == "LEFTMOUSE":
			if event.value == "PRESS":
				mbns = 1
			if event.value == "RELEASE":
				mbns = 0
		if event.type == "RIGHTMOUSE":
			context.region.callback_remove(self._handle)
			bpy.context.user_preferences.edit.use_global_undo = self.save_global_undo
			bm.free()
			bpy.ops.object.editmode_toggle()
			bmundo.to_mesh(mesh)
			bpy.ops.object.editmode_toggle()
			return {'CANCELLED'}
		elif event.type in ["MIDDLEMOUSE"]:
			inter = 1
			return {"PASS_THROUGH"}
		elif event.type in ["WHEELDOWNMOUSE", "WHEELUPMOUSE"]:
			inter = 1		
			return {"PASS_THROUGH"}
		
		elif event.type == "RET":
			# Break from while loop if ENTER pressed.
			# Free the bmesh.
			bm.free()
			context.region.callback_remove(self._handle)
			bpy.context.user_preferences.edit.use_global_undo = self.save_global_undo
			return {'FINISHED'}
		elif event.type == "MOUSEMOVE":
#			print (inter)
#			adapt()

			mx = event.mouse_region_x
			my = event.mouse_region_y
			hoveredge = None
	
			# First check mouse is in bounding box edge of which edges.
			testscrl = []
			for edge in slideedges:
				x1, y1, dummy = getscreencoords(edge.verts[0].co[:])
				x2, y2, dummy = getscreencoords(edge.verts[1].co[:])
				if x1 < x2:
					lwpx = x1 - 5
					uppx = x2 + 5
				else:
					lwpx = x2 - 5
					uppx = x1 + 5
				if y1 < y2:
					lwpy = y1 - 5
					uppy = y2 + 5
				else:
					lwpy = y2 - 5
					uppy = y1 + 5		
				if (((x1 < mx < x2) or (x2 < mx < x1)) and (lwpy < my < uppy)) or (((y1 < my < y2) or (y2 < my < y1)) and (lwpx < mx < uppx)):
					testscrl.append(edge)
	
			# Then check these edges to see if mouse is on one of them.
			allhoveredges = []
			hovering = 0
			zmin = 1e10
			if testscrl != []:
				for edge in testscrl:
					x1, y1, z1 = getscreencoords(edge.verts[0].co[:])
					x2, y2, z2 = getscreencoords(edge.verts[1].co[:])
	
					if x1 == x2 and y1 == y2:
						dist = math.sqrt((mx - x1)**2 + (my - y1)**2)
					else:
						dist = ((mx - x1)*(y2 - y1) - (my - y1)*(x2 - x1)) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	
					if -5 < dist < 5:
						allhoveredges.append(edge)
						if hoveredge != None and ((z1 + z2) / 2) > zmin:
							pass
						else:
							hovering = 1
							hoveredge = edge
							zmin = (z1 + z2) / 2
							mouseover = 1
							x1, y1, dummy = bx1, by1, dummy = getscreencoords(hoveredge.verts[0].co[:])
							x2, y2, dummy = bx2, by2, dummy = getscreencoords(hoveredge.verts[1].co[:])
							region.tag_redraw()
			if hovering == 0:
				if mouseover == 1:
					highoff = 1
					region.tag_redraw()
				mouseover = 0
				bx1, bx2, by1, by2 = -1, -1, -1, -1
			
	
	
			if hoveredge != None and mbns == 1:
				# Find projection mouse perpend on edge.
				if x1 == x2:	x1 += 1e-6
				if y1 == y2:	y1 += 1e-6
				a = (x2 - x1) / (y2 - y1)
				x = ((x1 / a) + (mx * a) + my - y1) / ((1 / a) + a)
				y = ((mx - x) * a) + my
				# Calculate relative position on edge and adapt screencoords accoringly.
				div = (x - x1) / (x2 - x1)
				if hoveredge.verts[0] in sverts:
					vert = hoveredge.verts[0]
					vert2 = hoveredge.verts[1]
				else:
					vert = hoveredge.verts[1]
					vert2 = hoveredge.verts[0]
				hx1, hy1, dummy = getscreencoords(hoveredge.verts[0].co[:])
				hx2, hy2, dummy = getscreencoords(hoveredge.verts[1].co[:])
				coords = [((hx2 - hx1) * div ) + hx1, ((hy2 - hy1) * div ) + hy1]
				for verts in selverts:
					if vert == verts[0]:
						selcoords[selverts.index(verts)][0] = coords
					elif vert == verts[1]:	
						selcoords[selverts.index(verts)][1] = coords
				if vert in singles:
					boxes[singles.index(vert)] = coords
				# Calculate and remember new vert 3D coordinates.  Set in physical mesh at end of program.		
				vx1, vy1, vz1 = hoveredge.verts[0].co[:]
				vx2, vy2, vz2 = hoveredge.verts[1].co[:]
				vertd[vert] = [((vx2 - vx1) * div ) + vx1, ((vy2 - vy1) * div ) + vy1, ((vz2 - vz1) * div ) + vz1]
				vert = bm.verts[vert.index]
				vert.co[0] = ((vx2 - vx1) * div ) + vx1
				vert.co[1] = ((vy2 - vy1) * div ) + vy1
				vert.co[2] = ((vz2 - vz1) * div ) + vz1
				mesh.update()
				
		return {'RUNNING_MODAL'}


def panel_func(self, context):
	self.layout.label(text="Deform:")
	self.layout.operator("mesh.edgetune", text="EdgeTune")
	self.layout.prop(scn, 'AutoAdapt')


def register():
	bpy.utils.register_module(__name__)
#	bpy.utils.register_class(EdgeTune)
	bpy.types.VIEW3D_PT_tools_meshedit.append(panel_func)


def unregister():
	bpy.utils.unregister_class(EdgeTune)
	bpy.types.VIEW3D_PT_tools_meshedit.remove(panel_func)


if __name__ == "__main__":
	register()







def adapt():
	
	global matrix, mat_rotX, mat_rotY, mat_rotZ, rotmat, viewwidth, viewheight
	global seledges, selverts, selcoords, vertd, singles, boxes, sverts
	global slideedges, slideverts, slidecoords, keepverts
	global bm, mesh, bmundo
	global mbns, viewchange, mouseover, highoff, bx1, bx2, by1, by2, mx, my, vertd
	global space, selobj, area, region
	global inter
	
	if not(inter):
		return
	# Rotating / panning / zooming 3D view is handled here.
	# Transform lists of coords to draw.
	if selobj.rotation_mode == "AXIS_ANGLE":
		return
		# How to find the axis WXYZ values ?
		ang =  selobj.rotation_axis_angle
		mat_rotX = Matrix.Rotation(ang, 4, ang)
		mat_rotY = Matrix.Rotation(ang, 4, ang)
		mat_rotZ = Matrix.Rotation(ang, 4, ang)
	elif selobj.rotation_mode == "QUATERNION":
		w, x, y, z = selobj.rotation_quaternion
		x = -x
		y = -y
		z = -z
		quat = Quaternion([w, x, y, z])
		matrix = quat.to_matrix()
		matrix.resize_4x4()
	else:
		ax, ay, az = selobj.rotation_euler
		mat_rotX = Matrix.Rotation(-ax, 4, 'X')
		mat_rotY = Matrix.Rotation(-ay, 4, 'Y')
		mat_rotZ = Matrix.Rotation(-az, 4, 'Z')
	if selobj.rotation_mode == "XYZ":
		matrix = mat_rotX * mat_rotY * mat_rotZ
	elif selobj.rotation_mode == "XZY":
		matrix = mat_rotX * mat_rotZ * mat_rotY
	elif selobj.rotation_mode == "YXZ":
		matrix = mat_rotY * mat_rotX * mat_rotZ
	elif selobj.rotation_mode == "YZX":
		matrix = mat_rotY * mat_rotZ * mat_rotX
	elif selobj.rotation_mode == "ZXY":
		matrix = mat_rotZ * mat_rotX * mat_rotY
	elif selobj.rotation_mode == "ZYX":
		matrix = mat_rotZ * mat_rotY * mat_rotX

	sx, sy, sz = selobj.scale
	mat_scX = Matrix.Scale(sx, 4, Vector([1, 0, 0]))
	mat_scY = Matrix.Scale(sy, 4, Vector([0, 1, 0]))
	mat_scZ = Matrix.Scale(sz, 4, Vector([0, 0, 1]))
	matrix = mat_scX * mat_scY * mat_scZ * matrix

	for posn in range(len(selverts)):
		selcoords[posn] = [getscreencoords(vertd[selverts[posn][0]][:])[:2], getscreencoords(vertd[selverts[posn][1]][:])[:2]]
	for posn in range(len(slideverts)):
		slidecoords[posn] = [getscreencoords(slideverts[posn][0].co[:])[:2],  getscreencoords(slideverts[posn][1].co[:])[:2]]
	for posn in range(len(singles)):
		boxes[posn] = getscreencoords(vertd[singles[posn]][:])[:2]

	if bpy.context.scene['AutoAdapt']:
		getlayout()



	





def getscreencoords(vector):
	region = bpy.context.region
	rv3d = bpy.context.space_data.region_3d	
	vector = Vector([vector[0], vector[1], vector[2]])
	pvector = vector * matrix
	pvector = pvector + selobj.location
	
	pvector[0] = pvector[0]
	pvector[1] = pvector[1]
	pvector[2] = pvector[2]
	svector = view3d_utils.location_3d_to_region_2d(region, rv3d, pvector)
	if svector == None:
		return [0, 0 ,0]
	else:
		return [svector[0], svector[1], pvector[2]]

def mul(a, b):
	# a is vector, b is matrix
	r = [0, 0, 0]
	r[0] = a[0]*b[0][0]+a[1]*b[1][0]+a[2]*b[2][0]+b[3][0]
	r[1] = a[0]*b[0][1]+a[1]*b[1][1]+a[2]*b[2][1]+b[3][1]
	r[2] = a[0]*b[0][2]+a[1]*b[1][2]+a[2]*b[2][2]+b[3][2]
	return r
	








def do_edgetune(self):

	global matrix, mat_rotX, mat_rotY, mat_rotZ, rotmat, viewwidth, viewheight
	global seledges, selverts, selcoords, vertd, singles, boxes, sverts
	global slideedges, slideverts, slidecoords, keepverts, keepedges
	global bm, mesh, bmundo
	global mbns, viewchange, mouseover, highoff, bx1, bx2, by1, by2, mx, my, vertd
	global space, selobj, area, region
	global inter

	# Do this to refresh mesh if just subdivided.
	bpy.ops.object.editmode_toggle()
	bpy.ops.object.editmode_toggle()

	context = bpy.context
	region = context.region  
	selobj = bpy.context.active_object
	mesh = selobj.data
	bm = bmesh.from_edit_mesh(mesh)
	bmundo = bm.copy()

	area = bpy.context.area

	# Calculate viewport, get transformation matrix.
	for sp in area.spaces:
		if sp.type == "VIEW_3D":
			space = sp
	viewwidth = area.width
	viewheight = area.height
	if selobj.rotation_mode == "AXIS_ANGLE":
		return
		# How to find the axis WXYZ values ?
		ang =  selobj.rotation_axis_angle
		mat_rotX = Matrix.Rotation(ang, 4, ang)
		mat_rotY = Matrix.Rotation(ang, 4, ang)
		mat_rotZ = Matrix.Rotation(ang, 4, ang)
	elif selobj.rotation_mode == "QUATERNION":
		print ("QUAT")
		w, x, y, z = selobj.rotation_quaternion
		x = -x
		y = -y
		z = -z
		quat = Quaternion([w, x, y, z])
		matrix = quat.to_matrix()
		matrix.resize_4x4()
	else:
		ax, ay, az = selobj.rotation_euler
		mat_rotX = Matrix.Rotation(-ax, 4, 'X')
		mat_rotY = Matrix.Rotation(-ay, 4, 'Y')
		mat_rotZ = Matrix.Rotation(-az, 4, 'Z')
	if selobj.rotation_mode == "XYZ":
		matrix = mat_rotX * mat_rotY * mat_rotZ
	elif selobj.rotation_mode == "XZY":
		matrix = mat_rotX * mat_rotZ * mat_rotY
	elif selobj.rotation_mode == "YXZ":
		matrix = mat_rotY * mat_rotX * mat_rotZ
	elif selobj.rotation_mode == "YZX":
		matrix = mat_rotY * mat_rotZ * mat_rotX
	elif selobj.rotation_mode == "ZXY":
		matrix = mat_rotZ * mat_rotX * mat_rotY
	elif selobj.rotation_mode == "ZYX":
		matrix = mat_rotZ * mat_rotY * mat_rotX
		
	sx, sy, sz = selobj.scale
	mat_scX = Matrix.Scale(sx, 4, Vector([1, 0, 0]))
	mat_scY = Matrix.Scale(sy, 4, Vector([0, 1, 0]))
	mat_scZ = Matrix.Scale(sz, 4, Vector([0, 0, 1]))
	matrix = mat_scX * mat_scY * mat_scZ * matrix
	
	
	keepverts = []
	for vert in bm.verts:
		if vert.select:
			keepverts.append(vert)
	keepedges = []
	for edge in bm.edges:
		if edge.select:
			keepedges.append(edge)

	highoff = 0
	mbns = 0
	inter = 0
	viewchange = 0
	mouseover = 0	
	bx1, bx2, by1, by2 = -1, -1, -1, -1
	mx = my = -1
	vertd2 = {}

	getlayout()



def getlayout():
	
	global matrix, mat_rotX, mat_rotY, mat_rotZ, rotmat, viewwidth, viewheight
	global seledges, selverts, selcoords, vertd, singles, boxes, sverts
	global slideedges, slideverts, slidecoords, keepverts, keepedges
	global bm, mesh, bmundo
	global mbns, viewchange, mouseover, highoff, bx1, bx2, by1, by2, mx, my, vertd
	global space, selobj, area, region
	
	# seledges: selected edges list
	# Blender.selverts: selected verts list per edge
	# Blender.selcoords: selected verts coordinate list per edge
	sverts = []
	seledges = []
	selverts = []
	selcoords = []
	for vert in keepverts:
		vert.select = 1
#	bm.select_mode = "VERT"
	bpy.ops.view3d.select_border(gesture_mode=0, xmin=0, xmax=viewwidth - 1, ymin=0, ymax=viewheight - 1, extend=True)
	for vert in keepverts:
		if vert.select:
			vert.select = 0      
		else:
			vert.select = 1
			sverts.append(bmundo.verts[vert.index])
	for edge in keepedges:
		if edge.verts[0].select and edge.verts[1].select:
			edge = bmundo.edges[edge.index]
			seledges.append(edge)
			selverts.append([edge.verts[0], edge.verts[1]])
			x1, y1, dummy = getscreencoords(edge.verts[0].co[:])
			x2, y2, dummy = getscreencoords(edge.verts[1].co[:])
			selcoords.append([[x1, y1],[x2, y2]])
#	return
	# selverts: selected verts list
	# slideedges: slideedges list
	# slideverts: slideverts list per edge
	# slidecoords: slideverts coordinate list per edge
	vertd = {}
	slideverts = []
	slidecoords = []
	slideedges = []
	for vert in sverts:
		vertd[vert] = vert.co[:]
#		for rail in keepedges:
		for edge in vert.link_edges:
#				if vert in edge.verts:
#			if vert == edge.verts[0] or vert == edge.verts[1]:
			if not(edge in seledges):
				slideedges.append(edge)
				slideverts.append([edge.verts[0], edge.verts[1]])
				x1, y1, dummy = getscreencoords(edge.verts[0].co[:])
				x2, y2, dummy = getscreencoords(edge.verts[1].co[:])
				slidecoords.append([[x1, y1], [x2, y2]])
						
	
	# Box out single vertices.
	singles = []
	boxes = []
	for vert in sverts:
		single = 1
		for edge in seledges:
			if vert == edge.verts[0] or vert == edge.verts[1]:
				single = 0
				break
		if single == 1:
			singles.append(vert)
			boxes.append(getscreencoords(vert.co[:])[:2])




def redraw():
	
	global matrix, rotmat, mat_rotX, mat_rotY, mat_rotZ, viewwidth, viewheight
	global seledges, selverts, selcoords, vertd, singles, boxes, sverts, slideedges, slideverts, slidecoords
	global bm, mesh
	global viewchange, mouseover, highoff, bx1, bx2, by1, by2, mx, my, vertd
	global space, selobj, context, area
	

	if slideverts != []:
		# Draw single verts as boxes.
		glColor3f(1.0,1.0,0)
		for vertcoords in boxes:
			glBegin(GL_POLYGON)
			x, y = vertcoords
			glVertex2f(x-2, y-2)
			glVertex2f(x-2, y+2)
			glVertex2f(x+2, y+2)
			glVertex2f(x+2, y-2)
			glEnd()
	
		# Accentuate selected edges.
		glColor3f(1.0,1.0,0)
		for posn in range(len(selcoords)):
			glBegin(GL_LINES)
			x, y = selcoords[posn][0]
			glVertex2f(x, y)
			x, y = selcoords[posn][1]
			glVertex2f(x, y)
			glEnd()
	
		# Draw slide-edges.
		glColor3f(1.0,0,0)
		for posn in range(len(slidecoords)):
			glBegin(GL_LINES)
			x, y = slidecoords[posn][0]
			glVertex2f(x, y)
			x, y = slidecoords[posn][1]
			glVertex2f(x, y)
			glEnd()

	# Draw mouseover highlighting.
	if mouseover:
		glColor3f(0,0,1.0)
		glBegin(GL_LINES)
		x,y = bx1, by1
		glVertex2f(x,y)
		x,y = bx2, by2
		glVertex2f(x,y)
		glEnd()
	if highoff:
		highoff = 0
		glColor3f(1.0,0,0)
		glBegin(GL_LINES)
		x,y = bx1, by1
		glVertex2f(x,y)
		x,y = bx2, by2
		glVertex2f(x,y)
		glEnd()
	
#	restoreOGLsetup()
