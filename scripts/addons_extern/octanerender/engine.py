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

# This script by Lionel Zamouth & Matej Moderc

import subprocess
import os
import time
import datetime
import mathutils
import bpy
from . import settings
from .utils import *
from .export import *
from .ocs_nodes import *
from .instances import exportParticleSystems
from .scripting import OctaneCamera, getCamUpdateScript


def appendCamData(scene, args, unitFactor):
    """
    Appends camera command line args and creates an OctaneCamera object

    @param args: list where to put camera cmdline args
    @param unitFactor: the Octane scaling Factor

    @return: A newly created OctaneCamera object
    """
    octane_render = scene.octane_render
    blender_render = scene.render
    octaneCamera = OctaneCamera()
    x = blender_render.resolution_x
    y = blender_render.resolution_y
    axes = ['x', 'y', 'z']
    paramDsp = ''
    # Check if we have a valid camera
    camOBJ = scene.camera
    if not camOBJ:
        error('Scene has no camera selected')
    camCAM = camOBJ.data
    if camCAM.type != 'PERSP':
        error('Only Perspective cameras can be exported')
    log('Using camera : <%s.%s>' % (camOBJ.name, camCAM.name))

    # Set Lens Shift and fov
    fov = camCAM.angle * 180.0 / 3.1415926536

    if y > x:
        # Portrait mode
        args.append('--cam-lensshift-right')
        args.append('%f' % (camCAM.shift_x * y / x))
        args.append('--cam-lensshift-up')
        args.append('%f' % (camCAM.shift_y))
        fov *= x / y
    else:
        # Landscape mode
        args.append('--cam-lensshift-right')
        args.append('%f' % (camCAM.shift_x))
        args.append('--cam-lensshift-up')
        args.append('%f' % (camCAM.shift_y * x / y))

    args.append('--cam-fov')
    args.append('%f' % (fov))
    octaneCamera.P_FOV = fov

    # Manage Lens Aperture
    if camCAM.OCT_use_lens_aperture:
        args.append('--cam-aperture')  # --cam-aperture
        args.append('%f' % (camCAM.OCT_lens_aperture))
        log('Lens aperture: %f' % (camCAM.OCT_lens_aperture))
        octaneCamera.P_APERTURE = camCAM.OCT_lens_aperture

    # Manage Focal Depth / Depth of Field
    fd = 100.0
    log('Using Depth of Field from : %s' % (camCAM.name))
    if camCAM.dof_object:
        tarOBJ = bpy.data.objects.get(camCAM.dof_object.name)
        if camCAM.dof_object.name == camOBJ.name:
            error('Narcissic camera... stop looking at yourself!')
        fd = (tarOBJ.location - camOBJ.location).magnitude
        log('Using DoF with distance to <%s> : %f * unitSize' % (tarOBJ.name, fd))
    else:
        fd = camCAM.dof_distance
        if fd < 0.00001:
            fd = 0
        log('Using DoF from blender camera: %f * unitSize' % (fd))
    fd *= unitFactor
    # Ignore DoF of 0
    if fd > 0:
        args.append('--cam-focaldepth')
        args.append('%f' % (fd))
        octaneCamera.P_FOCAL_DEPTH = fd

    # Set camera position and target
    matrix = camOBJ.matrix_world
    if octane_render.export_ROTX90 == True:
        position = rotate90x(matrix_vect(matrix, [0.0, 0.0, 0.0, 1.0]))
        # position = rotate90x(camOBJ.location)
        target = rotate90x(matrix_vect(matrix, [0.0, 0.0, -1.0, 1.0]))
        up = rotate90x(matrix_vect(matrix, [0.0, 1.0, 0.0, 0.0]))
    else:
        position = matrix_vect(matrix, [0.0, 0.0, 0.0, 1.0])
        # position = camOBJ.location
        target = matrix_vect(matrix, [0.0, 0.0, -1.0, 1.0])
        up = matrix_vect(matrix, [0.0, 1.0, 0.0, 0.0])
    for i in range(3):
        args.append('--cam-pos-%s' % (axes[i]))
        args.append('%f' % (position[i] * unitFactor))
        if i == 0:
            paramDsp = ''
        paramDsp += '%s %f ' % (axes[i], position[i] * unitFactor)
    log('Camera position: %s' % (paramDsp))
    for i in range(3):
        args.append('--cam-target-%s' % (axes[i]))
        args.append('%f' % (target[i] * unitFactor))
        if i == 0:
            paramDsp = ''
        paramDsp += '%s %f ' % (axes[i], target[i] * unitFactor)
    log('Camera target: %s' % (paramDsp))
    for i in range(3):
        args.append('--cam-up-%s' % (axes[i]))
        args.append('%f' % (up[i] * unitFactor))
        if i == 0:
            paramDsp = ''
        paramDsp += '%s %f ' % (axes[i], up[i] * unitFactor)
    log('Camera up: %s' % (paramDsp))

    octaneCamera.P_POSITION = (position[0] * unitFactor, position[1] * unitFactor, position[2] * unitFactor)
    octaneCamera.P_TARGET = (target[0] * unitFactor, target[1] * unitFactor, target[2] * unitFactor)
    octaneCamera.P_UP = (up[0] * unitFactor, up[1] * unitFactor, up[2] * unitFactor)

    # Manage camera Motion
    if camCAM.OCT_use_camera_motion:
        currentFrame = scene.frame_current
        # Interpolate on next frame
        if camCAM.OCT_interpolate_frame == '0':
            scene.frame_set(currentFrame + 1)
            log('Motion interploate on next frame')
        # Interpolate on previous frame
        elif currentFrame > 1:
            scene.frame_set(currentFrame - 1)
            log('Motion interpolate on previous frame')

        matrix = camOBJ.matrix_world
        if octane_render.export_ROTX90 is True:
            position = rotate90x(matrix_vect(matrix, [0.0, 0.0, 0.0, 1.0]))
            target = rotate90x(matrix_vect(matrix, [0.0, 0.0, -1.0, 1.0]))
            up = rotate90x(matrix_vect(matrix, [0.0, 1.0, 0.0, 0.0]))
        else:
            position = matrix_vect(matrix, [0.0, 0.0, 0.0, 1.0])
            target = matrix_vect(matrix, [0.0, 0.0, -1.0, 1.0])
            up = matrix_vect(matrix, [0.0, 1.0, 0.0, 0.0])
        up = rotate90x(matrix_vect(matrix, [0.0, 1.0, 0.0, 0.0]))

        for i in range(3):
            args.append('--cam-motion-pos-%s' % (axes[i]))
            args.append('%f' % (position[i] * unitFactor))
            if i == 0:
                paramDsp = ''
            paramDsp += '%s %f ' % (axes[i], position[i] * unitFactor)
        log('Camera motion position: %s' % (paramDsp))
        for i in range(3):
            args.append('--cam-motion-target-%s' % (axes[i]))
            args.append('%f' % (target[i] * unitFactor))
            if i == 0:
                paramDsp = ''
            paramDsp += '%s %f ' % (axes[i], target[i] * unitFactor)
        log('Camera motion target: %s' % (paramDsp))
        for i in range(3):
            args.append('--cam-motion-up-%s' % (axes[i]))
            args.append('%f' % (up[i] * unitFactor))
            if i == 0:
                paramDsp = ''
            paramDsp += '%s %f ' % (axes[i], up[i] * unitFactor)
        log('Camera motion up: %s' % (paramDsp))
        scene.frame_set(currentFrame)
    return octaneCamera


def appendCommandArgs(scene, args, outimage):
    """Appends the rest of the command line arguments (except cam)"""
    octane_render = scene.octane_render
    blender_render = scene.render
    x = blender_render.resolution_x
    y = blender_render.resolution_y
    # Manage the resolution option
    resSize = blender_render.resolution_percentage / 100
    if octane_render.export_resolution:
        log('Resolution set to %d x %d at %d%%' % (x, y, resSize * 100))
        args.append('--film-width')
        args.append('%i' % (x * resSize))
        args.append('--film-height')
        args.append('%i' % (y * resSize))

    # Set the GPUs option
    if octane_render.GPU_selector:
        for val in octane_render.GPU_use_list.split(' '):
            args.append('-g')
            args.append('%s' % (val))
        log('GPUs to use: %s' % (octane_render.GPU_use_list))

    # Setting stuff if pulling image
    if octanerender.pullImage:
        # Set the exit after rendering flag (for animation or pulling back image)
        args.append('-e')
        args.append('-q')
        if octane_render.output_mode == 'OUTPUT_PNG':
            args.append('--output-png')
        if octane_render.output_mode == 'OUTPUT_PNG16':
            args.append('--output-png16')
        if octane_render.output_mode == 'OUTPUT_EXR':
            args.append('--output-exr')
        if octane_render.output_mode == 'OUTPUT_EXR_TM':
            args.append('--output-exr-tm')
        args.append(outimage)

    # Set samples to render
    args.append('-s')
    args.append('%d' % (octane_render.export_samples_per_image))
    log('Samples per image: %d' % (octane_render.export_samples_per_image))

######################
# OctaneRenderEngine #
######################


class OctaneRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'OCT_RENDER'
    bl_label = "Octane Render"
    bl_postprocess = False

    def render(self, scene):
        self.update_stats('', 'Octane: export started for frame# %d (see console for progress), please wait...' % (scene.frame_current))
        # Preset status to ERROR in case of plugin crash
        update_status(3, 'Something wrong happened, please check console logs')

        # Accessors to both render environments
        octane_render = scene.octane_render
        blender_render = scene.render
        world = scene.world

        # Let's start
        start_time = datetime.datetime.now()

        # Get octane_render name
        baseName = fixName(octane_render.project_name)
        if baseName == '' or hasSpace(baseName):
            error('Project name is empty or contains spaces "%s"' % baseName)

        # Set and check project path
        basePath = absPath(octane_render.path)
        if not os.path.isdir(basePath) or hasSpace(basePath):
            error('Project directory is invalid or contains spaces "%s" ("%s")' % (octane_render.path, basePath))
        octanerender.dst_dir = basePath

        # Set and check image output path
        animPath = absPath(octane_render.image_output)
        if octanerender.pullImage is True:
            if (not os.path.isdir(animPath)) or hasSpace(animPath):
                error('Image output directory is invalid or contains spaces "%s" ("%s")' % (octane_render.path, animPath))

        # Set octane scene and obj filenames
        ocsFile = absPath('%s/%s.ocs' % (basePath, baseName))
#        ocsTemp = absPath('%s/%s.ocs.temp' % (basePath,baseName))
        objFile = absPath('%s/%s.obj' % (basePath, baseName))
        objTemp = absPath('%s/%s.obj.temp' % (basePath, baseName))
        mtlFile = absPath('%s/%s.mtl' % (basePath, baseName))
        mtlTemp = absPath('%s/%s.mtl.temp' % (basePath, baseName))
        log('Output ocs: "%s"' % (ocsFile))
        log('Output obj: "%s"' % (objFile))
        log('Output mtl: "%s"' % (mtlFile))

        # Set the unit factor (meters, centimeters, inches, etc...
        unitFactor = 1
        unitFactor = {0: 0.001, 1: 0.01, 2: 0.1, 3: 1, 4: 10, 5: 100, 6: 1000, 7: 0.0254, 8: 0.3048, 9: 0.9144, 10: 201.168, 11: 1609.344}[int(octane_render.unit_size)]
        log('Unit Factor (rescaling): %.4f' % (unitFactor))

        # Since the new version of .ocs structure in 1.5, all the old functions to write the .ocs
        # do not work anymore. ONLY write a .ocs, if the file does not yet exist!
        if not os.path.isfile(ocsFile):
            OCS = ocsParse(template_ocs.splitlines())
            ocsMeshNameUpdate(OCS, objFile)
            if world.OCT_kernel_use:
                ocsKernelUpdate(OCS, scene)
            if world.OCT_environment_use:
                ocsEnvironmentUpdate(OCS, scene)
            if world.OCT_imager_use:
                ocsImagerUpdate(OCS, scene)
            ocsWriteFile(ocsFile, OCS)

        # if animation start at first frame else export current
        if octane_render.export_mode == 'MODE_ANIMATION':
            frame_start = scene.frame_start
            frame_end = scene.frame_end
            frame_current = frame_start
        else:
            frame_start = frame_end = frame_current = scene.frame_current

        x = blender_render.resolution_x
        y = blender_render.resolution_y
        resSize = blender_render.resolution_percentage / 100
        importImage = octane_render.import_render or octane_render.export_mode == 'MODE_ANIMATION'
        temp_files = []

        def export_geometry(temp_files):
            obj_list = obj_export(scene)
            mtl_list = write_obj(objTemp, mtlFile, obj_list, scene, unitFactor)
            # if octane_render.export_materials:
            write_mtl(mtlTemp, mtl_list, scene, octane_render.export_copy_images)
            temp_files.extend([objTemp, mtlTemp])
            # export instances, append their file names to temporary list
            if octane_render.instances_export_mode == 'Auto':
                temp_files.extend(exportParticleSystems(scene, temp=True))

        # LOOP through frames for rendering
        while frame_current <= frame_end:
            log('Exporting frame #%d' % (frame_current))
            frame_time = datetime.datetime.now()
            scene.frame_set(frame_current)

            if not octane_render.export_camera_only or octane_render.export_mode == 'MODE_GEOMETRY':
                # this is executed only for the first frame. export, rename immediately and clear temp list
                if len(temp_files) == 0:
                    export_geometry(temp_files)
                rename_temporary_files(temp_files)
                temp_files = []
            else:
                log('Camera update only, skipping geometry export')

            # if geometry only we are already done
            if octane_render.export_mode == 'MODE_GEOMETRY':
                break

            # we are going to call Octane, prepare cmdline args
            command_args = []

            # check Octane binary
            exeFile = absPath(octane_render.binary)
            if not os.path.isfile(exeFile):
                error('Invalid Octane binary file "%s" ("%s")' % (octane_render.binary, exeFile))
            command_args.append(exeFile)

            # set mesh node to render, if blank use project name
            command_args.append('-m')
            if octane_render.node_render_geometry == '':
                command_args.append('%s.obj' % (baseName))
            else:
                command_args.append(octane_render.node_render_geometry)

            # set RenderTarget node to render, ignore if blank
            if octane_render.node_render_target:
                command_args.append('-t')
                command_args.append(octane_render.node_render_target)

            # append camera settings
            if octane_render.export_camera:
                octaneCamera = appendCamData(scene, command_args, unitFactor)
                # also generate the lua script for camera update and save it to file, if a RT has been specified
                if octane_render.node_render_target:
                    script = getCamUpdateScript(octaneCamera, octane_render.node_render_target)
                    luaFile = absPath('%s/%s.lua' % (basePath, "camUpdate"))
                    try:
                        fh = open(luaFile, "w")
                        fh.write(script)
                        fh.close()
                    except IOError as e:
                        error(e.msg)
                        fh.close()
                    command_args.append('--script')
                    command_args.append(luaFile)

            # determine output image file name & extension
            outext = 'exr' if octane_render.output_mode in ['OUTPUT_EXR', 'OUTPUT_EXR_TM'] else 'png'
            outimage = absPath('%s/%s_%06d.%s' % (animPath, baseName, frame_current, outext))

            # append the rest of cmdargs
            appendCommandArgs(scene, command_args, outimage)
            # Last argument is the ocs file
            command_args.append(ocsFile)

            # start Octane process
            log('Launching Octane: {}'.format(command_args))
            octane_process = subprocess.Popen(command_args, executable=exeFile)
            rendering = True

            # if animation or importing render back to Blender, wait subprocess, check for interrupt
            if octane_render.export_mode == 'MODE_ANIMATION' or importImage:
                while octane_process.poll() is None:
                    if self.test_break():  # if the render op should be cancelled
                        try:
                            octane_process.terminate()
                        except Exception as e:
                            print("Exception during Octane subprocess terminaton: '%s'" % e.msg)
                        error('Render aborted by user')
                        break
                    # at this point Octane has started, we have time to export the next frame to
                    # temporary files and wait untill rendering is finished
                    if len(temp_files) == 0 and not octane_render.export_camera_only:
                        scene.frame_set(frame_current + scene.frame_step)
                        export_geometry(temp_files)
                    time.sleep(1)  # sleep a second between poll tests

            # render finished properly, get RenderResult
            if importImage:
                result = self.begin_result(0, 0, x * resSize, y * resSize)
                try:
                    log('Load image from file: %s' % outimage)
                    result.layers[0].load_from_file(outimage)
                except:
                    log('Unable to load image from file: %s' % outimage)
                self.end_result(result, False)
            self.update_stats('', 'Octane: last frame/export took %s, now rendering frame# %d...' % (elapsed_short(frame_time), frame_current + scene.frame_step))
            frame_current += scene.frame_step

        # rendering done, cleanup & go back to start frame
        # print("TEMP FILES: %s" % temp_files)
        rename_temporary_files(temp_files)
        scene.frame_set(frame_start)
        # octane_render.replace_project = False
        update_status(0, 'Completed in %s' % elapsed_long(start_time))
