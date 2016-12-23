# 3Dビュー > メッシュ編集モード > 「Ctrl+V」キー

import bpy

################
# オペレーター #
################

class CellMenuSeparateEX(bpy.types.Operator):
	bl_idname = "mesh.cell_menu_separate_ex"
	bl_label = "Separation of different objects (extended)"
	bl_description = "Isolate to another object of the call the extended menu"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu(name=SeparateEXMenu.bl_idname)
		return {'FINISHED'}

class SeparateSelectedEX(bpy.types.Operator):
	bl_idname = "mesh.separate_selected_ex"
	bl_label = "Choice of (active isolated-side)"
	bl_description = "After \"in the choice of separation\" enters edit mode for the separation side"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		objs = []
		for obj in context.selectable_objects:
			objs.append(obj.name)
		bpy.ops.mesh.separate(type='SELECTED')
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		for obj in context.selectable_objects:
			if (not obj.name in objs):
				obj.select = True
				context.scene.objects.active = obj
				break
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='SELECT')
		return {'FINISHED'}

class DuplicateNewParts(bpy.types.Operator):
	bl_idname = "mesh.duplicate_new_parts"
	bl_label = "A selection of reproduction and new objects"
	bl_description = "Enters edit mode, replication and selection to the new object from"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		objs = []
		for obj in context.selectable_objects:
			objs.append(obj.name)
		bpy.ops.mesh.duplicate()
		bpy.ops.mesh.separate(type='SELECTED')
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		for obj in context.selectable_objects:
			if (not obj.name in objs):
				obj.select = True
				context.scene.objects.active = obj
				break
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='SELECT')
		return {'FINISHED'}

class QuickShrinkwrap(bpy.types.Operator):
	bl_idname = "mesh.quick_shrinkwrap"
	bl_label = "Quick shrink wrap"
	bl_description = "Another one you mesh the selected vertices pettanko was bonds, who"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		('NEAREST_SURFACEPOINT', "The closest surface point", "", 1),
		('PROJECT', "Projection", "", 2),
		('NEAREST_VERTEX', "Nearest vertex", "", 3),
		]
	wrap_method = bpy.props.EnumProperty(items=items, name="Mode", default='PROJECT')
	offset = bpy.props.FloatProperty(name="Offset", default=0.0, min=-10, max=10, soft_min=-10, soft_max=10, step=1, precision=5)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) != 2):
			return False
		for obj in context.selected_objects:
			if (obj.type != 'MESH'):
				return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		pre_mode = active_obj.mode
		bpy.ops.object.mode_set(mode='OBJECT')
		for obj in context.selected_objects:
			if (active_obj.name != obj.name):
				target_obj = obj
				break
		new_vg = active_obj.vertex_groups.new(name="TempGroup")
		selected_verts = []
		for vert in active_obj.data.vertices:
			if (vert.select):
				selected_verts.append(vert.index)
		if (len(selected_verts) <= 0):
			bpy.ops.object.mode_set(mode=pre_mode)
			self.report(type={'ERROR'}, message="One run, select the vertex more than")
			return {'CANCELLED'}
		new_vg.add(selected_verts, 1.0, 'REPLACE')
		new_mod = active_obj.modifiers.new("temp", 'SHRINKWRAP')
		for i in range(len(active_obj.modifiers)):
			bpy.ops.object.modifier_move_up(modifier=new_mod.name)
		new_mod.target = target_obj
		new_mod.offset = self.offset
		new_mod.vertex_group = new_vg.name
		new_mod.wrap_method = self.wrap_method
		if (self.wrap_method == 'PROJECT'):
			new_mod.use_negative_direction = True
		bpy.ops.object.modifier_apply(modifier=new_mod.name)
		active_obj.vertex_groups.remove(new_vg)
		bpy.ops.object.mode_set(mode=pre_mode)
		return {'FINISHED'}

################
# メニュー追加 #
################

class SeparateEXMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_edit_mesh_separate_ex"
	bl_label = "Separation of different objects (extended)"
	bl_description = "Isolate to another object of the extended menu."
	
	def draw(self, context):
		self.layout.operator("mesh.separate", text="Selection of").type = 'SELECTED'
		self.layout.operator(SeparateSelectedEX.bl_idname, icon="PLUGIN")
		self.layout.operator(DuplicateNewParts.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator("mesh.separate", text="In the material").type = 'MATERIAL'
		self.layout.operator("mesh.separate", text="In the isolated structural parts").type = 'LOOSE'


# Menu
def menu(self, context):

		self.layout.separator()
		self.layout.operator(QuickShrinkwrap.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(CellMenuSeparateEX.bl_idname, icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(DuplicateNewParts.bl_idname, icon="PLUGIN")

