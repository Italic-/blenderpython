# 情報 > 「ウィンドウ」メニュー

import bpy

################
# パイメニュー #
################

class PieMenu(bpy.types.Menu):
	bl_idname = "INFO_MT_window_pie"
	bl_label = "Pie menu"
	bl_description = "Is a pie menu window relationship"
	
	def draw(self, context):
		self.layout.operator(AreaTypePieOperator.bl_idname, icon="PLUGIN")

class AreaTypePieOperator(bpy.types.Operator):
	bl_idname = "wm.area_type_pie_operator"
	bl_label = "Editor type"
	bl_description = "Change the editor type pie menu is"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.ops.wm.call_menu_pie(name=AreaTypePie.bl_idname)
		return {'FINISHED'}
class AreaTypePie(bpy.types.Menu): #
	bl_idname = "INFO_MT_window_pie_area_type"
	bl_label = "Editor type"
	bl_description = "Change the editor type pie menu is"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Text editor", icon="TEXT").type = "TEXT_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Out liner", icon="OOPS").type = "OUTLINER"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Property", icon="BUTS").type = "PROPERTIES"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="3D view", icon="MESH_CUBE").type = "VIEW_3D"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="UV / image editor", icon="IMAGE_COL").type = "IMAGE_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Nordeditor", icon="NODETREE").type = "NODE_EDITOR"
		self.layout.menu_pie().operator("wm.call_menu_pie", text="Anime related", icon="ACTION").name = AreaTypePieAnim.bl_idname
		self.layout.menu_pie().operator("wm.call_menu_pie", text="Other", icon="QUESTION").name = AreaTypePieOther.bl_idname
		

class AreaTypePieAnim(bpy.types.Menu):
	bl_idname = "INFO_MT_window_pie_area_type_anim"
	bl_label = "Editor type (animation)"
	bl_description = "Is a pie menu change the editor type (animation related)"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="The NLA Editor", icon="NLA").type = "NLA_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Dope sheet", icon="ACTION").type = "DOPESHEET_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Graph Editor", icon="IPO").type = "GRAPH_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Timeline", icon="TIME").type = "TIMELINE"

class AreaTypePieOther(bpy.types.Menu):
	bl_idname = "INFO_MT_window_pie_area_type_other"
	bl_label = "Editor type (other)"
	bl_description = "Is a pie menu change the editor type (other)"
	
	def draw(self, context):
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Logic Editor", icon="LOGIC").type = "LOGIC_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Video sequence editor", icon="SEQUENCE").type = "SEQUENCE_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Video clip Editor", icon="RENDER_ANIMATION").type = "CLIP_EDITOR"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="File browser", icon="FILESEL").type = "FILE_BROWSER"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Python console", icon="CONSOLE").type = "CONSOLE"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="Information", icon="INFO").type = "INFO"
		self.layout.menu_pie().operator(SetAreaType.bl_idname, text="User settings", icon="PREFERENCES").type = "USER_PREFERENCES"

class SetAreaType(bpy.types.Operator): #
	bl_idname = "wm.set_area_type"
	bl_label = "Change the editor type"
	bl_description = "Change the editor type"
	bl_options = {'REGISTER'}
	
	type = bpy.props.StringProperty(name="Area type")
	
	def execute(self, context):
		context.area.type = self.type
		return {'FINISHED'}

################
# オペレーター #
################

class ToggleJapaneseInterface(bpy.types.Operator):
	bl_idname = "wm.toggle_japanese_interface"
	bl_label = "English UI, Japanese switch"
	bl_description = "Japan language with English interface switch"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		if (not bpy.context.user_preferences.system.use_international_fonts):
			bpy.context.user_preferences.system.use_international_fonts = True
		if (bpy.context.user_preferences.system.language != "ja_JP"):
			bpy.context.user_preferences.system.language = "ja_JP"
		bpy.context.user_preferences.system.use_translate_interface = not bpy.context.user_preferences.system.use_translate_interface
		return {'FINISHED'}


def menu(self, context):

	self.layout.separator()
	self.layout.operator(ToggleJapaneseInterface.bl_idname, icon="FILE_REFRESH")
	self.layout.separator()

