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

# @author Matej Moderc

from string import Template

#############
# LuaScript #
#############
# class LuaScript():
# 	"""A combination of generated Lua functions. Holds methods to generate, save & delete scripts"""
# 	def __init__(self, scriptName):
# 		self.scriptName = scriptName

# 	def saveScript(self, folder):
# 		"""Saves the script to the specified folder"""

# 	def deleteScript(self):
# 		"""Deletes the script file, if it exists"""

# 	def getScript(self):
# 		"""Returns the script text"""

# 	def appendFunction(self, template, functionName):
# 		"""Appends the template to the current script"""


#############
# Templates #
#############
LUA_CAM_UPDATE = Template(
    """
-- updates the camera parameters for a Render Target node
local function updateCamera(cam)
$PINVALUES
end
rtname = '$RTNAME'
root = octane.project.getSceneGraph()
targets = octane.nodegraph.findItemsByName(root, rtname, false)
target = targets[1]
if target == nil then
    print("LUA ERROR: No RenderTargets with name '" .. rtname .. "' found.")
    return
end
cam = target:getConnectedNode(octane.P_CAMERA)
if cam == nil then
    print("LUA INFO: Spcified RT has no camera node. Creating...")
    cam = octane.node.create{type=octane.NT_CAM_THINLENS, pinOwnerNode=target, pinOwnerId=octane.P_CAMERA}
elseif cam:getProperties().type == octane.NT_CAM_THINLENS then
    print("LUA INFO: Found thinlens camera. Updating...")
else
    print("LUA ERROR: Specified RT has a panoramic camera. Cannot update.")
    return
end
updateCamera(cam)
--octane.render.restart()
"""
)

# LUA_RENDER_FLYTHROUGH = Template(
# """
# -- renders a camera flythrough animation
# local function renderFlythrough()

# end
# renderFlythrough()
# """
# )

# LUA_SAVE_IMAGERS = Template(
# """
# -- saves multiple imager results of the current render job
# local function saveImagers()

# end
# saveImagers()
# """
# )

# LUA_RENDER_TURNTABLE

################
# OctaneCamera #
################


class OctaneCamera():
    """A holder object for exported camera info"""

    def __init__(self, fov=45.0, aperture=0.0, position=(0.0, 0.5, 0.1), target=(0.0, 0.0, 0.0), up=(0.0, 1.0, 0.0), lens_shift=(0.0, 0.0), focal_depth=1.1180340):
        self.P_FOV = fov
        self.P_APERTURE = aperture
        self.P_POSITION = position
        self.P_TARGET = target
        self.P_UP = up
        self.P_LENS_SHIFT = lens_shift
        self.P_FOCAL_DEPTH = focal_depth


def getCamUpdateScript(octaneCamera, rtname):
    """
    Returns a Lua script that updates the camera parameters for the specified RenderTarget node

    @param octaneCamera: OctaneCamera object
    @param rtname: String with the RenderTarget node name to apply camera to

    @return: A string that is a Lua script
    """
    members = [attr for attr in dir(octaneCamera) if not callable(attr) and not attr.startswith("__")]
    pinValues = ""
    for pinName in members:
        val = getattr(octaneCamera, pinName)
        if isinstance(val, tuple):
            val = "{0}".format(val).replace("(", "{").replace(")", "}")
        pinValues += "\tcam:setPinValue(octane.%s, %s, true)\n" % (pinName, val)
    script = LUA_CAM_UPDATE.substitute(RTNAME=rtname, PINVALUES=pinValues)
    return script

# testing
if __name__ == "__main__":
    # from engine import OctaneCamera
    cam = OctaneCamera()
    print(getCamUpdateScript(cam, "RT_Test"))
