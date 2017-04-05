#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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

# @author: Matej Moderc

import datetime
from math import radians

import bpy
import bpy.path as bpath
from bpy.types import Panel, Operator
from bpy.props import BoolProperty
from mathutils import Matrix, Quaternion, Vector

from .export import write_obj, write_mtl


class ExportException(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return repr(self._msg)


def info(msg):
    print("INFO: %s" % msg)


def warning(msg):
    print("WARNING: %s" % msg)


def error(msg):
    print("ERROR: %s" % msg)

SCALE_FACTORS = {0: 0.001, 1: 0.01, 2: 0.1, 3: 1, 4: 10, 5: 100, 6: 1000,
                 7: 0.0254, 8: 0.3048, 9: 0.9144, 10: 201.168, 11: 1609.344}


def writeTransform(t, fh):
    """Writes first three matrix rows to the file handle"""
    vals = ["%.6f" % v for v in tuple(t[0]) + tuple(t[1]) + tuple(t[2])]
    fh.write(" ".join(vals) + "\n")


def writeDupliObjects(scene, dupli_list, filepath, temp=False):
    """
    Writes the vizualisation object data to .obj/.mtl

    @param scene: Active Blender scene
    @param dupli_list: A list of geometry objects to write
    @param filepath: The path where to save the files
    @param temp: If saving into temporary files with .temp sufix

    @return: A lits of two filenames that have been written
    """
    octane = scene.octane_render
    objFile = filepath + ".obj" if not temp else filepath + ".obj.temp"
    mtlFile = filepath + ".mtl" if not temp else filepath + ".mtl.temp"
    mtl_dict = write_obj(objFile, mtlFile, dupli_list, scene, SCALE_FACTORS[int(octane.unit_size)])
    write_mtl(mtlFile, mtl_dict, scene, False)
    return [objFile, mtlFile]


def exportDuplis(scene, emitter, oct_t):
    """Exports dupli objects for the specified emitter"""
    info("Exporting dupli objects for '%s'" % emitter.name)
    octane = scene.octane_render
    export_path = bpath.abspath(octane.path)

    if octane.instances_write_dupli:
        filepath = "".join([export_path, emitter.name, "_objects"])
        info("Writing dupli objects to file '%s'" % (filepath + ".obj"))
        duplis_world = {}
        for c in emitter.children:
            duplis_world[c] = c.matrix_world.copy()
            c.matrix_world = Matrix.Identity(4)
        d_type = emitter.dupli_type
        emitter.dupli_type = 'NONE'
        writeDupliObjects(scene, emitter.children, filepath)
        emitter.dupli_type = d_type
        for k, v in duplis_world.items():
            k.matrix_world = v

    emitter.dupli_list_create(scene)
    lst = emitter.dupli_list
    if len(lst) == 0:  # if not on active layers, dupli list = empty
        return
    try:
        fh = open(export_path + emitter.name + ".csv", "w")
        for duplicate in lst.values():
            t = duplicate.matrix.copy()
            writeTransform(oct_t[0] * t * oct_t[1], fh)
        fh.close()
    except IOError as err:
        msg = "IOError during file handling '{0}'".format(err)
        error(msg)
        raise ExportException(msg)
    emitter.dupli_list_clear()


def exportMeshDuplis(scene, obj, users, oct_t):
    """Exports the transforms of Alt+D duplicated objects"""
    octane = scene.octane_render
    export_path = bpath.abspath(octane.path)
    csv_filename = export_path + obj.data.name + ".csv"
    info("Saving transforms for '%s' mesh-dupli objects into file '%s' " % (obj.data.name, csv_filename))

    try:
        if octane.instances_write_dupli:
            filepath = export_path + obj.data.name
            obj_world = obj.matrix_world.copy()
            obj.matrix_world = Matrix.Identity(4)
            writeDupliObjects(scene, [obj], filepath)
            obj.matrix_world = obj_world
        fh = open(csv_filename, "w")
        for o in users:
            t = o.matrix_world.copy()
            writeTransform(oct_t[0] * t * oct_t[1], fh)
        fh.close()
    except IOError as err:
        msg = "IOError during file handling '{0}'".format(err)
        error(msg)
        raise ExportException(msg)


def exportParticles(scene, emitter, psys, oct_t, temp=False):
    """
    Exports a particle system for the specified emitter

    @param scene: Active Blender scene
    @param emitter: Emitter object we are exporting PS of
    @param psys: The particle system we are exporting
    @param oct_t: Octane world transforms tuple
    @param temp: If saving into temporary files with .temp sufix

    @return: Returns a list of files that have been written. At least a .csv file, but can also
                    contain an .obj/.mtl if the vizualisation particle has been written.
                    It can contain duplicate entires for the same file!
    """
    octane = scene.octane_render
    export_path = bpath.abspath(octane.path)
    pset = psys.settings
    infostr = "Exporting PS '%s' (%s) on emitter '%s'" % (psys.name, pset.type, emitter.name)
    particles = [p for p in psys.particles] if pset.type == 'HAIR' else [p for p in psys.particles if p.alive_state == 'ALIVE']
    filenames = []

    if pset.render_type == "OBJECT":
        dupli_ob = pset.dupli_object
        if dupli_ob is not None and octane.instances_write_dupli:
            info(infostr + " with %i instances of '%s' objects" % (len(particles), dupli_ob.name))
            filepath = "".join([bpath.abspath(octane.path), dupli_ob.name])
            info("Writing dupli object to file '%s'" % (filepath + ".obj"))
            dupli_world = dupli_ob.matrix_world.copy()
            transl_inv = Matrix.Translation(-dupli_world.translation)
            dupli_ob.matrix_world = transl_inv * dupli_ob.matrix_world
            filenames.extend(writeDupliObjects(scene, [dupli_ob], filepath, temp))
            dupli_ob.matrix_world = dupli_world
    else:
        warning("Invalid PS visualization type '%s'" % pset.render_type)
        return
    if not pset.use_rotation_dupli:
        warning("'Use object rotation' should be on. Rotations wont conform to Blender veiwport")

    try:
        csv_file = export_path + psys.name + ".csv" if not temp else export_path + psys.name + ".csv.temp"
        fh = open(csv_file, "w")
        for p in particles:
            # if pset.type == 'HAIR' or not p.alive_state == 'DEAD':
            rot = Quaternion.to_matrix(p.rotation).to_4x4()
            if (pset.type == "HAIR"):
                h1 = p.hair_keys[0].co
                h2 = p.hair_keys[-1].co
                loc = Matrix.Translation(h1)
                scale = Matrix.Scale((h2 - h1).length, 4)
                rot = emitter.matrix_world.decompose()[1].to_matrix().to_4x4().inverted() * rot
            else:
                loc = Matrix.Translation(p.location)
                scale = Matrix.Scale(p.size, 4)
            t = loc * rot * scale
            t = emitter.matrix_world * t if pset.type == "HAIR" else t
            writeTransform(oct_t[0] * t * oct_t[1], fh)
        fh.close()
        filenames.append(csv_file)
        return filenames
    except IOError as err:
        msg = "IOError during file handling '{0}'".format(err)
        error(msg)
        raise ExportException(msg)


def exportParticleSystems(scene, temp=False):
    """
    Writes a .csv for each PS of each active emitter

    @param scene: Active Blender scene
    @param temp: If saving into temporary files with .temp sufix

    @return: Returns a list of files that have been written. Can contain multiple .csv/.obj/.mtl filenames
    """
    objects = scene.objects
    octane = scene.octane_render
    oct_scale = Matrix.Scale(SCALE_FACTORS[int(octane.unit_size)], 4)
    oct_glob = Matrix.Rotation(radians(-90.0), 4, 'X') * oct_scale
    oct_loc = Matrix.Rotation(radians(90.0), 4, 'X') * oct_scale.inverted()
    filenames = []
    for ob in objects:
        # only those on active layers (comparing global layer visibility list to ob's layer visibility list)
        if len(ob.particle_systems) > 0 and scene.layers[next((i for i in range(len(ob.layers)) if ob.layers[i]))]:
            if ob.dupli_type == 'NONE' and len(ob.particle_systems) > 0:
                for ps in ob.particle_systems:
                    pset = ps.settings
                    if pset.render_type == "OBJECT":
                        filenames.extend(exportParticles(scene, ob, ps, (oct_glob, oct_loc), temp))
                    else:
                        warning("Unsupported PS vizualisation type '%s' for object '%s'. Skipping..." % (pset.render_type, ob.name))
    # remove all possible duplicate file entries, by converting list to set and back
    return list(set(filenames))

###################
#		GUI		 #
###################
### EXPORT BUTTON ###


class BUTTON_instances_export_selected(Operator):
    bl_idname = "ops.instances_export_selected"
    bl_label = "Write transforms"
    bl_description = "Exports instance transforms of visible emitters to .csv file"

    def execute(self, context):
        sce = context.scene
        octane = sce.octane_render
        start = datetime.datetime.now()
        info("Instance transforms")
        objects = [context.active_object]
        oct_scale = Matrix.Scale(SCALE_FACTORS[int(octane.unit_size)], 4)
        oct_glob = Matrix.Rotation(radians(-90.0), 4, 'X') * oct_scale
        oct_loc = Matrix.Rotation(radians(90.0), 4, 'X') * oct_scale.inverted()
        with_warnings = False
        msg = None

        def report_warning(msg):
            warning(msg)
            self.report({'WARNING'}, msg)
            nonlocal with_warnings
            with_warnings = True

        obj = context.active_object
        if obj is None:
            self.report({'WARNING'}, "No object selected!")
            return {"CANCELLED"}

        if len(obj.particle_systems) > 0:  # and obj.is_visible(sce) and not obj.hide_render:
            info("Found duplicator '%s' of type '%s'" % (obj.name, obj.dupli_type))
            if obj.dupli_type in ('FACES', 'VERTS'):
                exportDuplis(sce, obj, (oct_glob, oct_loc))
            elif obj.dupli_type == 'NONE' and len(obj.particle_systems) > 0:
                if len(obj.particle_systems) > 0:
                    for ps in obj.particle_systems:
                        pset = ps.settings
                        if pset.render_type == "OBJECT":
                            exportParticles(sce, obj, ps, (oct_glob, oct_loc))
                        else:
                            report_warning("Unsupported PS vizualisation type '%s'" % pset.render_type)
                else:
                    report_warning("Object '%s' has no particle systems attached" % obj.name)
            else:
                report_warning("Unsupported duplicator type '%s'" % obj.dupli_type)
        elif obj.type == "MESH" and obj.data.users > 1:
            me = obj.data
            users = [o for o in bpy.data.objects if o.type == "MESH" and o.data == me]
            info("Found %i users for dupli-mesh '%s'" % (len(users), me.name))
            exportMeshDuplis(sce, obj, users, (oct_glob, oct_loc))
        else:
            report_warning("The selected object '%s' is not an instance emitter or mesh-dupli" % obj.name)

        if with_warnings:
            msg = "Script ended with warnings, look into console"
            self.report({'WARNING'}, msg)
        else:
            msg = "Instances export completed in {0})\n".format(datetime.datetime.now() - start)
            info(msg)
            self.report({'INFO'}, msg)
        return {"FINISHED"}

    # export instances button is active only when selected object is a duplicator
    @classmethod
    def poll(self, context):
        obs = context.selected_objects
        if len(obs) < 1:
            return False
        ob = obs[0]
        return (len(ob.particle_systems) > 0) or (ob.type == "MESH" and ob.data.users > 1)
        # return ob.is_duplicator or (ob.type == "MESH" and ob.data.users > 1)

### INSTANCES PANEL ###


class OBJECT_PT_instances(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_label = "Instances export"
    COMPAT_ENGINES = {'OCT_RENDER'}

    @classmethod
    def poll(self, context):
        rnd = context.scene.render
        return rnd.engine == "OCT_RENDER" and rnd.use_game_engine is False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="PARTICLES")

    def draw(self, context):
        layout = self.layout
        octane = context.scene.octane_render
        row = layout.row()
        row.prop(octane, "instances_export_mode", expand=True)
        col = layout.column(align=True)
        col.prop(octane, "instances_write_dupli")
        if octane.instances_export_mode == 'Manual':
            col.operator("ops.instances_export_selected")


def register():
    bpy.utils.register_class(OBJECT_PT_instances)
    bpy.utils.register_class(BUTTON_instances_export_selected)


def unregister():
    del(bpy.types.Scene.instances_write_dupli)
    bpy.utils.unregister_class(BUTTON_instances_export_selected)
    bpy.utils.unregister_class(OBJECT_PT_instances)
