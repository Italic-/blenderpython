

import bpy,os,sys
import bmesh,math
from bpy.props import IntProperty,BoolProperty,StringProperty,FloatProperty
from bpy_extras import object_utils

dllpath1="B:/GPtools64.dll";
dllpath2="B:/GPtools64.dll";
#dllpath3="B:/GPtools64.dll";

path目录GP = os.path.dirname(__file__);
文件夹此GP=os.path.basename(path目录GP);
"""
if("GPencil_manager.global_var" in sys.modules):
    print("GPencil_manager.global_var",);
    G = sys.modules["GPencil_manager.global_var"];
else:
    try:
        import GPencil_manager.global_var as G;
    except:
        print("!!!ERROR import",);
"""
def  oΔ新建物(s物名,L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序):
    mesh新= bpy.data.meshes.new(s物名);
    mesh新.from_pydata(L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序);
    #mesh新.update();
    return object_utils.object_data_add(bpy.context, mesh新, operator=None).object;
    
def Δ删除物(CoScene,o,b是层级):
    Lo要删除物=[];
        
    #----删除子级-------------------------------------------------------------
    if(b是层级):
        def  Δ收集子(o父):
            for o子 in  o父.children:
                Lo要删除物.append(o子);
                Δ收集子(o子);
        Δ收集子(o);
        for o子 in  Lo要删除物:
            if(o子!=None):
                CoScene.objects.unlink(o子);o子.user_clear();bpy.data.objects.remove(o子); 
                
    if(o!=None):
        CoScene.objects.unlink(o);o.user_clear();bpy.data.objects.remove(o); 
#//////////////////////////////////////////////////
class 卐GP生成线段卐Operator(bpy.types.Operator): 
    bl_idname = "op.gp_gen_lines"
    bl_label = " "
    bl_description = "---"
    bl_options = {"REGISTER", "UNDO"};
    
    @classmethod 
    def poll(self,context):
        return context.active_object.type=="MESH" ;
    """
    def draw(self, context):
        layout = self.layout;
        layout.prop(self, "sp已经有记录");         
    """
    def execute(self,context):
        oA=context.active_object;
        if(oA==None and not context.scene.bp是保留线段s):
            self.report({"ERROR"},"you mush select a mesh");#"INFO" "ERROR" "DEBUG" "WARNING"
            return {"FINISHED"};
        s模式pre=oA.mode;
        #gp=context.gpencil_data;
        #G.DLL=LIB.dllΔ载入dllLIB(_卐DLL,"dll",dllpath1,dllpath2,None);
        fps=context.scene.frame_current;print("fps==",fps);
        gpl1=context.active_gpencil_layer;#GPencilLayer  
        print("len gpl1==",len(gpl1.frames), len(gpl1.frames[0].strokes));
        #gpl=context.active_gpencil_frame;#这个层只有当前帧
        #print("len frames==",len(gpl.frames),context.active_gpencil_layer);
        #gpf=gpl1.frames[0];
        gpf前=None;L点序ξf3位=[]; L边序i2边点ξ=[]; L面序i4面点ξ序=[];
        for gpf in gpl1.frames:
            print("strokes ,frame_number",gpf.strokes,gpf.frame_number);
            if(gpf.frame_number>fps):
                break;
            elif(gpf.frame_number==fps):
                gpf前=gpf;
                break;

            gpf前=gpf;
        #----找到当前的gp--------------------------------------------------------
        iξ艹=0;j前=0;
        if(gpf前):
            if(len(gpf前.strokes)<1):
                self.report({"ERROR"},"no GPencil strokes");#"INFO" "ERROR" "DEBUG" "WARNING"
                return {"FINISHED"};
            for i,gps in enumerate(gpf前.strokes):
                #L边序i2边点ξ.append([]);#[[],]
                jξ最后=len(gps.points)-1;
                for j,gpsp in enumerate(gps.points):
                    #print("gpsp.co",gpsp.co);
                    L点序ξf3位.append(gpsp.co);
                    if(j!=0):
                        if(j!=jξ最后):
                            v后=gps.points[j+1].co;
                            fΛ弧度=(v前-gpsp.co).angle(v后-gpsp.co);
                            if(fΛ弧度>math.radians(context.scene.fp精简角度s)):
                                L点序ξf3位.pop();
                                continue;
                        
                        L边序i2边点ξ.append([j前,iξ艹]);#[[j前,j],]
                    j前=iξ艹;
                    iξ艹+=1;
                    v前=gpsp.co;
                    #gpsp.co*=1.1;
                    
        #----新建物--------------------------------------------------------
        #print("L边序i2边点ξ==",L边序i2边点ξ);
        if(oA.mode!="OBJECT"):
            bpy.ops.object.mode_set(mode="OBJECT");
        o新=oΔ新建物("cut_path",L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序);
        o新.location=(0,0,0);o新.select=True;
        context.scene.objects.active=oA;
        if(not context.scene.bp不切割s):
            bpy.ops.object.mode_set(mode="EDIT");
            bpy.ops.mesh.knife_project(cut_through=False);
            
        if(not context.scene.bp是保留线段s):            
            Δ删除物(context.scene,o新,False);
            gpl1.frames.remove(gpf前);
            
        if(oA.mode!=s模式pre):
            bpy.ops.object.mode_set(mode=s模式pre);
            
        #context.scene.objects.link(o新);
        #print("len active_gpencil_frame==",len(context.active_gpencil_frame.frames),context.active_gpencil_frame);
        #print("gpf.active_frame==",gpl.active_frame);
        #gpf=gpl.active_frame;
        #if(gpf!=None):
            #print(" gpf strokes==", len(gpf.strokes));#Χ crush
        return {"FINISHED"};
        

        
    
#//////////////////////////////////////////////////
class 卐载入DLL卐Operator (bpy.types.Operator):
    bl_idname = 'load.gp_dll';
    bl_label = '载入dll';
    bl_options = {'REGISTER', 'UNDO'};
    
    @classmethod
    def poll(cls, context):      
        return True; #(obj and obj.type == 'MESH')
    def execute(self, context):
        #D=_卐DLL();
        G.DLL=LIB.dllΔ载入dllLIB(_卐DLL,"dll",dllpath1,dllpath2,None);
        print("LIB.dllΔ载入dllLIB",LIB.dllΔ载入dllLIB);
        """
        try:
            _卐DLL.dll = CDLL(dllpath64B);
        except:
            _卐DLL.dll = CDLL(dllpath64E);
        """
        return {'FINISHED'}; 
        
class 卐删除DLL卐Operator (bpy.types.Operator):
    bl_idname = 'dele.gp_dll';
    bl_label = '删除dll';
    bl_options = {'REGISTER', 'UNDO'};
    
    @classmethod
    def poll(cls, context):      
        return True; #(obj and obj.type == 'MESH')
    def execute(self, context):     
        G.DLL=LIB.dllΔ卸载dllLIB(_卐DLL,"dll");
        print("DEL DLL~~~~~~~~~~",);
        return {'FINISHED'};

#////////////////////////////////////////////////
def dllΔ载入dll(DLL,dllpath1,dllpath2,dllpath3):   
    if(DLL==None):
        try:
            DLL= CDLL(dllpath1);
            print("ok",);
        except:
            try:
                DLL= CDLL(dllpath2);
                print("not susses",);    
            except:    
                DLL= CDLL(dllpath3);
                print("not susses",);
                
    return DLL;

def dllΔ卸载dll(DLL):   
    if(platform.system()=="Windows"):  
        while(DLL):
            windll.kernel32.FreeLibrary.argtypes = [HMODULE];
            windll.kernel32.FreeLibrary(DLL._handle);#释放dll
            print("delete DLL~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  \n",);
            DLL=None;
    return DLL;
    
    
    
    
    
    