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


bl_info = {
    'name': 'Emulate Numpad',
    'author': 'chromoly',
    'version': (0, 1, 2),
    'blender': (2, 78, 0),
    'location': 'Screen > MiddleMouse',
    # 英語で書けるかよw
    'description': 'マウス中ボタンと特定キーの組み合わせで、'
                   'テンキーに割り当てられたオペレーターを実行する',
    'warning': 'EVT_TWEAK_Mが割り当てられたオペレータは全て無視されるようになる',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'User Interface',
}

"""
単独動作不可。listvalidkeysに依存する。
"""


import importlib
import traceback
import ctypes as ct

import bpy
from mathutils import Vector

try:
    importlib.reload(listvalidkeys)
    importlib.reload(addongroup)
    importlib.reload(registerinfo)
    importlib.reload(structures)
except NameError:
    from .. import listvalidkeys
    from ..utils import addongroup
    from ..utils import registerinfo
    from ..utils import structures


OPERATOR_PRIORITY = [
    'view2d.scroller_activate',
    'text.scroll_bar'
]


keypad = [
    ('kp0', 'V', 'NUMPAD_0', '0'),
    ('kp1', 'Z', 'NUMPAD_1', '1'),
    ('kp2', 'X', 'NUMPAD_2', '2'),
    ('kp3', 'C', 'NUMPAD_3', '3'),
    ('kp4', 'A', 'NUMPAD_4', '4'),
    ('kp5', 'S', 'NUMPAD_5', '5'),
    ('kp6', 'D', 'NUMPAD_6', '6'),
    ('kp7', 'Q', 'NUMPAD_7', '7'),
    ('kp8', 'W', 'NUMPAD_8', '8'),
    ('kp9', 'E', 'NUMPAD_9', '9'),
    ('kpdl', 'B', 'NUMPAD_PERIOD', '.'),
    ('kpad', 'F', 'NUMPAD_PLUS', '+'),
    ('kpsu', 'R', 'NUMPAD_MINUS', '-'),
    ('kpmu', 'G', 'NUMPAD_ASTERIX', '*'),
    ('kpdv', 'T', 'NUMPAD_SLASH', '/'),
    ('kpen', 'SPACE', 'NUMPAD_ENTER', 'Enter'),
]

keypad_alt = [
    ('kp0', 'Z', 'NUMPAD_0', '0'),
    ('kp1', 'A', 'NUMPAD_1', '1'),
    ('kp2', 'S', 'NUMPAD_2', '2'),
    ('kp3', 'D', 'NUMPAD_3', '3'),
    ('kp4', 'Q', 'NUMPAD_4', '4'),
    ('kp5', 'W', 'NUMPAD_5', '5'),
    ('kp6', 'E', 'NUMPAD_6', '6'),
    ('kp7', 'ONE', 'NUMPAD_7', '7'),
    ('kp8', 'TWO', 'NUMPAD_8', '8'),
    ('kp9', 'THREE', 'NUMPAD_9', '9'),
    ('kpdl', 'C', 'NUMPAD_PERIOD', '.'),
    ('kpad', 'V', 'NUMPAD_PLUS', '+'),
    ('kpsu', 'F', 'NUMPAD_MINUS', '-'),
    ('kpmu', 'R', 'NUMPAD_ASTERIX', '*'),
    ('kpdv', 'FOUR', 'NUMPAD_SLASH', '/'),
    ('kpen', 'SPACE', 'NUMPAD_ENTER', 'Enter'),
]


name_space = \
    {attr: bpy.props.StringProperty(
        name=name, description=type_, default=default)
     for attr, default, type_, name in keypad}


def keymap_update(self, context):
    keymap = keypad if self.keymap == 'TYPE1' else keypad_alt
    for attr, rcv, snd, name in keymap:
        setattr(self, attr, rcv)


name_space['keymap'] = bpy.props.EnumProperty(
    name='KeyMap',
    items=(('TYPE1', 'Type1', ''),
           ('TYPE2', 'Type2', '')),
    update=keymap_update,
)
KeyPad = type('KeyPad', (), name_space)


class EmulateNumpadPreferences(
        addongroup.AddonGroupPreferences,
        registerinfo.AddonRegisterInfo,
        KeyPad,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    tweak_threshold = bpy.props.IntProperty(
        name='Tweak Threshold',
        default=1,
        min=1,
        max=1024,
        subtype='PIXEL',
    )

    func = bpy.types.Window.bl_rna.functions['cursor_modal_set']
    enum_items = func.parameters['cursor'].enum_items
    cursor_type = bpy.props.EnumProperty(
        name='Cursor',
        items=[(e.identifier, e.name, e.description) for e in enum_items],
        default='SCROLL_XY',
    )

    def draw(self, context):
        layout = self.layout
        split = layout.split(0.3)

        column = split.column()
        col = column.column()
        col.prop(self, 'tweak_threshold')
        col.prop(self, 'cursor_type')
        col.prop(self, 'keymap')

        def draw_column(layout, attrs):
            column = layout.column()
            for attr in attrs:
                prop_row = column.row()
                if attr:
                    s = prop_row.split(0.3)
                    sub_row = s.row()
                    sub_row.label(self.bl_rna.properties[attr].name)
                    sub_row = s.row()
                    sub_row.prop(self, attr, text='')
                else:
                    prop_row.label()

        row = split.row()
        sp = row.split()
        draw_column(sp.column(), [None, 'kp7', 'kp4', 'kp1', 'kp0'])
        draw_column(sp.column(), ['kpdv', 'kp8', 'kp5', 'kp2', None])
        draw_column(sp.column(), ['kpmu', 'kp9', 'kp6', 'kp3', 'kpdl'])
        draw_column(sp.column(), [None, 'kpsu', 'kpad', None, 'kpen'])

        self.layout.separator()
        super().draw(context)


def find_event_keymap_items(context, event_attrs, keymaps, idnames=()):
    keymap_items = []

    event_attrs = {
        'type': 'NONE',
        'value': 'ANY',
        'any': False,
        'shift': False,
        'ctrl': False,
        'alt': False,
        'oskey': False,
        'key_modifier': 'NONE',
        **event_attrs
    }

    idnames = set(idnames)

    for km in keymaps:
        for kmi in km.keymap_items:
            if not kmi.active:
                continue
            if kmi.idname == SCREEN_OT_emulate_numpad.bl_idname:
                continue
            if idnames and kmi.idname not in idnames:
                continue

            select_mouse = context.user_preferences.inputs.select_mouse
            if select_mouse == 'RIGHT':
                action_select = {'ACTIONMOUSE': 'LEFTMOUSE',
                     'SELECTMOUSE': 'RIGHTMOUSE',
                     'EVT_TWEAK_A': 'EVT_TWEAK_L',
                     'EVT_TWEAK_S': 'EVT_TWEAK_R',
                     }
            else:
                action_select = {'ACTIONMOUSE': 'RIGHTMOUSE',
                     'SELECTMOUSE': 'LEFTMOUSE',
                     'EVT_TWEAK_A': 'EVT_TWEAK_R',
                     'EVT_TWEAK_S': 'EVT_TWEAK_L',
                     }
            if (kmi.type == event_attrs['type'] or
                    kmi.type in action_select and
                    action_select[kmi.type] == event_attrs['type']):
                if kmi.value == event_attrs['value'] or kmi.value == 'ANY':
                    if kmi.any:
                        match = True
                    else:
                        mods = ['shift', 'ctrl', 'alt', 'oskey']
                        match = all([getattr(kmi, m) == event_attrs[m]
                                     for m in mods])
                    if kmi.key_modifier != 'NONE':
                        if kmi.key_modifier != event_attrs['key_modifier']:
                            match = False
                    if match:
                        keymap_items.append(kmi)
    return keymap_items


def get_operator_from_keymap_item(kmi):
    kwargs = {}
    try:
        m, f = kmi.idname.split('.')
        type_name = m.upper() + '_OT_' + f
        if not hasattr(bpy.types, type_name):
            return None, kwargs

        op = getattr(getattr(bpy.ops, m), f)
        for attr in kmi.properties.keys():
            if kmi.properties.is_property_set(attr):
                # NOTE: enumの場合、kmi.properties[attr]とすると
                #       intが返ってくる
                kwargs[attr] = getattr(kmi.properties, attr)
        return op, kwargs
    except:
        traceback.print_exc()
        return None, kwargs


def operator_call(context, event_attrs, keymaps, idnames=()):
    called = False
    pass_through = False
    running_modal = False

    for kmi in find_event_keymap_items(context, event_attrs, keymaps,
                                       idnames):
        op, kwargs = get_operator_from_keymap_item(kmi)
        if not op:
            continue

        if op.poll():
            called = True
            try:
                r = op('INVOKE_DEFAULT', **kwargs)
            except:
                traceback.print_exc()
                return called, running_modal, False
            pass_through = 'PASS_THROUGH' in r
            if 'RUNNING_MODAL' in r:
                running_modal = True
            if not pass_through:
                return called, running_modal, pass_through

    return called, running_modal, pass_through


class SCREEN_OT_emulate_numpad(bpy.types.Operator):
    bl_idname = 'screen.emulate_numpad'
    bl_label = 'Emulate Numpad'
    bl_options = {'REGISTER'}

    def __init__(self):
        self.event_type = ''

    def modal(self, context, event):
        prefs = EmulateNumpadPreferences.get_instance()
        ret = {'RUNNING_MODAL'}

        event_attrs = {
            attr: getattr(event, attr)
            for attr in ['type', 'value', 'shift', 'ctrl', 'alt', 'oskey']}
        # event.key_modifierに当たるものはpythonAPIでは提供されていない
        ev = ct.cast(ct.c_void_p(event.as_pointer()),
                     ct.POINTER(structures.wmEvent)).contents
        value = ev.keymodifier
        prop = bpy.types.KeyMapItem.bl_rna.properties['key_modifier']
        for enum_item in prop.enum_items:
            if enum_item.value == value:
                event_attrs['key_modifier'] = enum_item.identifier
                break

        if self.finish:
            ret = {'FINISHED'}

        elif event.type == 'MOUSEMOVE':
            x, y = event.mouse_x, event.mouse_y
            v = Vector((x, y)) - Vector((self.mouse_x, self.mouse_y))
            if v.length >= prefs.tweak_threshold:
                self.cursor_restor(context)
                event_attrs_ = {**event_attrs,
                                'type': 'MIDDLEMOUSE', 'value': 'PRESS'}
                _called, running_modal, _pass_through = operator_call(
                    context, event_attrs_, self.keymaps)
                if running_modal:
                    self.finish = True
                else:
                    # ret = {'FINISHED'}
                    self.cursor_set(context)

        elif event.type == self.event_type and event.value == 'RELEASE':
            ret = {'FINISHED'}

        elif event.type == 'ESC':
            ret = {'FINISHED'}

        else:
            match = False
            if event.value == 'PRESS':
                for attr, _, kmi_type, _ in keypad:
                    if event.type == getattr(prefs, attr):
                        match = True
                        break
            if match:
                self.cursor_restor(context)
                event_attrs_ = {**event_attrs,
                                'type': kmi_type, 'value': 'PRESS'}
                _called, running_modal, _pass_through = operator_call(
                    context, event_attrs_, self.keymaps)
                self.cursor_set(context)
                if running_modal:
                    self.finish = True
                else:
                    # ret = {'FINISHED'}
                    self.cursor_set(context)

        if 'FINISHED' in ret:
            self.cursor_restor(context)
        return ret

    def cursor_set(self, context):
        prefs = EmulateNumpadPreferences.get_instance()
        if prefs.cursor_type != 'NONE':
            context.window.cursor_modal_set(prefs.cursor_type)

    def cursor_restor(self, context):
        context.window.cursor_modal_restore()

    def invoke(self, context, event):
        self.event_type = event.type
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        self.finish = False

        self.keymaps = [km for km in listvalidkeys.context_keymaps(context)
                        if listvalidkeys.keymap_poll(context, km)]

        # numpadを使うオペレータが無いなら終了。
        found = False
        for km in self.keymaps:
            for kmi in km.keymap_items:
                if kmi.active:
                    if kmi.type.startswith('NUMPAD_'):
                        op, kwargs = get_operator_from_keymap_item(kmi)
                        if op and op.poll():
                            found = True
                            break
            if found:
                break
        if not found:
            return {'CANCELLED', 'PASS_THROUGH'}

        # view2d.scroller_activateを中ボタンで呼び出した場合、
        # すぐ反応する必要があるのでここで処理する
        event_attrs = {
            attr: getattr(event, attr)
            for attr in ['type', 'value', 'shift', 'ctrl', 'alt', 'oskey']}
        called, running_modal, pass_through = operator_call(
            context, event_attrs, self.keymaps, OPERATOR_PRIORITY)
        if called and not pass_through:
            return {'FINISHED'}

        self.cursor_set(context)

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}


classes = [
    SCREEN_OT_emulate_numpad,
    EmulateNumpadPreferences,
]


@EmulateNumpadPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = EmulateNumpadPreferences.get_keymap('Screen Editing')
        kmi = km.keymap_items.new(
            'screen.emulate_numpad', 'MIDDLEMOUSE', 'PRESS', head=True)


@EmulateNumpadPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
