import bpy, bmesh, copy
from bpy.props import IntProperty, StringProperty

select_verts = []
active_vert = -1
active_vert_prev = -3
prevs = False



bl_info = {
    "name": "GridFill Manager",
    "author": "Alexander Nedovizin (script), Paul Kotelevets (idea)",
    "version": (0, 1, 5),
    "blender": (2, 6, 8),
    "description": "GridFill Manager",
    "category": "Mesh"
}


def check_context(obj):
    global select_verts, active_vert
    if len(select_verts)==0:
        res=False
        return

    res = True
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    sv = find_index_of_selected_vertex(obj)
    for v in sv:
        if not(v in select_verts) and v<obj.mnogo_v:
            res = False

    return res


def update_shape(self,context):
    global select_verts, active_vert

    ch_c = check_context(context.object)

    if not ch_c:
        main(context, context.object.myRad, mode = True)
    else:

        selecting_verts(context.object.data,select_verts)
        main(context, context.object.myRad, mode = True)



bpy.types.Object.myRad = IntProperty(
    name="Radius",
	min = 0,
    default = 1,
    update = update_shape)

bpy.types.Object.mnogo_v= IntProperty(
    name="Vertices",
    default = -1)


def bm_vert_active_get(ob, D=0):
    global active_vert, active_vert_prev

    bm = bmesh.from_edit_mesh(ob.data)
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
            act_v = elem.index
        if D==1 and active_vert >= 0:
                avs = get_prev_active_vert(ob.data, active_vert)
                if avs==None:
                    return -2

                act_v = avs
                active_vert_prev = active_vert

        if D==2 and active_vert >= 0:
                avs = get_next_active_vert(ob.data, active_vert)
                if avs==None:
                    return -2

                act_v = avs
                active_vert_prev = active_vert

        return act_v
    return -2


def find_index_of_selected_vertex(obj):
    selected_verts = [i.index for i in obj.data.vertices if i.select]
    verts_selected = len(selected_verts)
    if verts_selected <1:
        return None
    else:
        return selected_verts


def find_connected_verts(me, found_index, not_list):
    global select_verts
    edges = me.edges
    connecting_edges = [i for i in edges if found_index in i.vertices[:]]
    if len(connecting_edges) == 0:
        return []
    else:
        connected_verts = []
        for edge in connecting_edges:
            cvert = set(edge.vertices[:])
            cvert.remove(found_index)
            vert = cvert.pop()
            if not (vert in not_list) and me.vertices[vert].select and (vert in select_verts):
                connected_verts.append(vert)

        if len(connected_verts)>2:
            print_error('Error: loop is not selected')
            return None
        return connected_verts


def get_prev_active_vert(me, found_index):
    global active_vert_prev, active_vert, prevs

    verts = find_connected_verts(me, found_index, [])
    if verts[0] == active_vert_prev:
        if not prevs:
            prevs = True
            return verts[0]
        else:
            return verts[1]
    else:
        if not prevs:
            prevs = True
            return verts[1]
        else:
            return verts[0]



def get_next_active_vert(me, found_index):
    global active_vert_prev, active_vert, prevs

    verts = find_connected_verts(me, found_index, [])
    if verts[0] == active_vert_prev:
        if not prevs:
            return verts[1]
        else:
            prevs = False
            return verts[0]
    else:
        if not prevs:
            return verts[0]
        else:
            prevs = False
            return verts[1]


def get_loop(me, active_v, v_set, not_list=[], step=0):
    vlist = [active_v]
    ln = len(v_set)
    not_list.append(active_v)

    step +=1
    list_v_1 = find_connected_verts(me, active_v, not_list)
    if list_v_1==None:
        return None

    if step==ln:
        return vlist

    if len(list_v_1)>0:
        list_v_2 = get_loop(me, list_v_1[0], v_set, not_list, step)
        if list_v_2==None:
            return None

        vlist += list_v_2

    return vlist


def get_opposite(me,vert_index, v_set):
    loop = []
    loop = get_loop(me, vert_index, v_set, [])
    if loop==None:
        return None

    ps = len(loop)//2
    ff = loop.index(vert_index)

    if ff>=ps:
        df = ff-ps
    else:
        df = ff+ps

    return loop[df]



def find_all_connected_verts(R, me, active_v, not_list=[], step=0):
    vlist = [active_v]
    not_list.append(active_v)
    step+=1
    list_v_1 = find_connected_verts(me, active_v, not_list)
    if list_v_1==None:
        return None

    if step==R+2:
        return vlist

    for v in list_v_1:
        list_v_2 = find_all_connected_verts(R, me, v, not_list, step)
        if list_v_2==None:
            return None

        vlist += list_v_2

    return vlist


def selecting_verts(me, mas):
    bpy.ops.object.mode_set(mode='OBJECT')

    for idx in mas:
        me.vertices[idx].select = True

    bpy.ops.object.mode_set(mode='EDIT')


def deselecting_verts(me, mas):
    bpy.ops.object.mode_set(mode='OBJECT')

    for idx in mas:
        me.vertices[idx].select = False

    bpy.ops.object.mode_set(mode='EDIT')



def cls_mnogo(obj):
    obj.mnogo_v = -1
    active_vert = -1
    select_verts = []
    active_vert_prev = -3
    prevs = False
    return


def main(context, Rad=1, Dist=0, mode=False):
    global select_verts, active_vert, mnogo_v, active_vert_prev

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

    ob = bpy.context.object
    ch_c = check_context(ob)

    if active_vert >= 0 and ob.mnogo_v>0 and mode:
        if ch_c:
            bpy.ops.ed.undo()
            if Dist>0:
                active_vert = bm_vert_active_get(ob,Dist)
        else:
            cls_mnogo(ob)
            main(context,Rad,mode=False)
            return





    if mode:
        av = -1
        if ch_c:
            av = active_vert
    else:
        av = bm_vert_active_get(ob,Dist)
        if ch_c:
            active_vert = -1

    if (active_vert < 0 or active_vert != av) and not mode:
        active_vert = bm_vert_active_get(ob,Dist)
        select_verts=[]

    if active_vert==-2 and not mode:
        print_error('Active vert is not defined')
        return{'Error: 003'}

    if select_verts==[]:
        select_verts = find_index_of_selected_vertex(ob)

    sv_len = len(select_verts)

    if sv_len<8:
        print_error('Error: need for equ or more then 8 verts')
        return{'Error: 001'}

    if (sv_len//8)<Rad:
        Rad = sv_len//8

    if (sv_len%2)>0 and not mode:
        print_error('Error: must be an even number of vertices')
        return{'Error: 002'}

    mesh = ob.data
    opposit_vert = get_opposite(mesh,active_vert, select_verts)
    if opposit_vert==None:
        return {'FINISHED'}

    nl = []
    new_sel_v_1 = find_all_connected_verts(Rad, mesh, active_vert, nl)
    if new_sel_v_1==None:
        return {'FINISHED'}
    new_sel_v_2 = find_all_connected_verts(Rad, mesh, opposit_vert, nl)
    if new_sel_v_2==None:
        return {'FINISHED'}

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for idx in nl:
        mesh.vertices[idx].select = True

    bpy.ops.object.mode_set(mode='EDIT')
    ob.mnogo_v = len(mesh.vertices)
    bpy.ops.mesh.fill_grid()

    return {'FINISHED'}


class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    message = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)

    def draw(self, context):
        self.layout.label(self.message, icon='BLENDER')


def print_error(message):
    bpy.ops.error.message('INVOKE_DEFAULT',
        type = "Message",
        message = message)


class GFManagerOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.gfmanager_operator"
    bl_label = "GridFill Manager Operator"
    bl_options = {'REGISTER', 'UNDO'}
    rad = bpy.props.IntProperty(options={'HIDDEN'})
    typing = bpy.props.IntProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.typing>0:
            main(context, context.object.myRad, Dist=self.typing, mode=True)
        else:
            main(context, context.object.myRad, Dist=0, mode = False)
        return {'FINISHED'}



class GFManagerPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Grid Fill Manager"
    bl_idname = "OBJECT_PT_GFManagerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == 'EDIT_MESH'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")
        layout.prop(obj, 'myRad')

        row = layout.row()
        row.operator("mesh.gfmanager_operator", text='', icon='TRIA_LEFT').typing=1
        row.operator("mesh.gfmanager_operator", text='', icon='TRIA_RIGHT').typing=2
        row.operator("mesh.gfmanager_operator", text='Ok').typing=0


def register():
    bpy.utils.register_class(GFManagerPanel)
    bpy.utils.register_class(GFManagerOperator)
    bpy.utils.register_class(MessageOperator)


def unregister():
    bpy.utils.unregister_class(GFManagerPanel)
    bpy.utils.unregister_class(GFManagerOperator)
    bpy.utils.unregister_class(MessageOperator)


if __name__ == "__main__":
    register()
