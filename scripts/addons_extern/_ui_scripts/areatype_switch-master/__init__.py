
bl_info = {
        "name": "Areatype Toggle Switch (Node/Timeline)",
        "description":"This example adds a button which toggles between the timeline and the node editor.",
        "author":"dustractor@gmail.com",
        "version":(0,1),
        "blender":(2,65,0),
        "location":"First button on the header.",
        "warning":"",
        "wiki_url":"",
        "category": "System"
        }

import bpy

class AREATYPE_OT_switch(bpy.types.Operator):
    bl_idname = "areatype.switch"
    bl_label = "areatype.switch"
    switchto = bpy.props.StringProperty()
    def execute(self,context):
        context.area.type = self.switchto
        return {"FINISHED"}

def timedraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="NODETREE").switchto = "NODE_EDITOR"

def nodedraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="TIME").switchto = "TIMELINE"

def prefsdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="TEXT").switchto = "TEXT_EDITOR"

def textdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="PREFERENCES").switchto = "USER_PREFERENCES"

def register():
    bpy.types.TIME_HT_header.prepend(timedraw)
    bpy.types.NODE_HT_header.prepend(nodedraw)
    bpy.types.USERPREF_HT_header.prepend(prefsdraw)
    bpy.types.TEXT_HT_header.prepend(textdraw)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.TIME_HT_header.remove(timedraw)
    bpy.types.NODE_HT_header.remove(nodedraw)
    bpy.utils.unregister_module(__name__)
    

