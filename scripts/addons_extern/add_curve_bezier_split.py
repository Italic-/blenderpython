bl_info = {
    'name': "Bezier Curve Split",
    'author': "luxuy blendercn",
    'version': (1, 0, 0),
    'blender': (2, 70, 0),
    'location': "Property window-->Curve Data Tab-->Shape-->Bezier Curve Split",
    'warning': "",
    'category': 'Add Curve'}


import bpy,math,mathutils
from bpy.props import FloatProperty, IntProperty, BoolProperty,EnumProperty,StringProperty
from mathutils import Matrix,Vector
#----------------------------------------------------------------------                       
class BezierCurveSplit(bpy.types.Operator):
    bl_idname = "bpt.bezier_curve_split"
    bl_label = "Bezier Curve Split"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        cv=context.object
        flag=1
        for spl in cv.data.splines:
            flag*=(spl.type=='BEZIER')
        if  cv.type=='CURVE' and context.mode=='EDIT_CURVE' and flag:
            return True
        return False

    def execute(self, context):
        
        cv=context.object
        spl_pts=[]
        sel_pts={}
        j=0
        for spl in cv.data.splines:
            pts={}
            sel_pts[j]=[len(spl.bezier_points)]
            for i in range(len(spl.bezier_points)):
                bpt=spl.bezier_points[i]
                
                pts[i]=[bpt.co[:],bpt.handle_left[:],bpt.handle_right[:]]
                
                
                if spl.bezier_points[i].select_control_point:
                    #print("sel pt !!")
                    
                    sel_pts[j].append(i)
            j+=1
            spl_pts.append(pts)

        cv.data.splines.clear()
        
        for key in sel_pts:
            
            num=0
            
            if sel_pts[key][-1]==sel_pts[key][0]-1:
                sel_pts[key].pop()
            for i in sel_pts[key][1:]+[sel_pts[key][0]-1]:
               
                if i!=0:
                    
                    spl=cv.data.splines.new('BEZIER')
                    spl.bezier_points.add(i-num)
                  
                    for j in range(num,i):
                        bpt=spl.bezier_points[j-num]
                       
                        bpt.co=spl_pts[key][j][0]
                        bpt.handle_left=spl_pts[key][j][1]
                        bpt.handle_right=spl_pts[key][j][2]
                    bpt=spl.bezier_points[-1]
                    bpt.co=spl_pts[key][i][0]
                    bpt.handle_left=spl_pts[key][i][1]
                    bpt.handle_right=spl_pts[key][i][2]
                    num=i
   
        return {'FINISHED'}
        
#==========================================================================================
def menu_func(self, context):

    self.layout.operator(BezierCurveSplit.bl_idname)
    


def register():
    bpy.utils.register_module(__name__)
    bpy.types.DATA_PT_shape_curve.append(menu_func)
def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()