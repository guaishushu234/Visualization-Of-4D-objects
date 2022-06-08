from w4_utils import *
from w4_display import *
import math

RefCubeVert = [Vertex(i[0],i[1]) for i in (((0)*4,(-1,-1,-1)),((0)*4,(-1,-1, 1)),
                                           ((0)*4,(-1, 1, 1)),((0)*4,(-1, 1,-1)),
                                           ((0)*4,( 1,-1,-1)),((0)*4,( 1,-1, 1)),
                                           ((0)*4,( 1, 1, 1)),((0)*4,( 1, 1,-1)))]
RefCubeEdge = [Edge(i) for i in ((0,1,1), (1,2,1), (2,3,1), (3,0,1), 
                                 (4,5,1), (5,6,1), (6,7,1), (7,4,1),
                                 (0,4,1), (1,5,1), (2,6,1), (3,7,1))]
rp = [[0, 1, 2, 0, 1, 2],[1, 2, 0, 3, 3, 3]]
rptext = ["XY", "YZ", "ZX", "XW", "YW", "ZW"]
snapname = "snapshots"

def Initialize():
    Root3 = math.sqrt(3.0)
    Tan2Vangle4 = math.tan(Radians(Vangle4/2.0))
    Tan2Vangle3 = math.tan(Radians(Vangle3/2.0))
    
    Temp3 = From3 - To3
    Dist3Initial = Temp3.norm()
    Dist3Auto    = Root3 / Tan2Vangle3
    
    '''Find the radius of the 4D data.  The radius of the 4D data is the
    radius of the smallest enclosing sphere, centered at the To point.
    Note that during the loop through the vertices, Data4Radius holds
    the squared radius value.'''
    
    Data4Radius = 0.00
    for ii in range(OBJ_VSTART,NumVerts):
        Temp4 = VertList[ii].position - To4
        dist = Temp4.dot(Temp4) #Current Vertex Distance From To4 Point
        if dist > Data4Radius:
            Data4Radius = dist
    Data4Radius = math.sqrt(Data4Radius)
    Temp4 = From4 - To4
    Dist4Initial = Temp4.norm()
    Dist4Auto    = Data4Radius / Tan2Vangle4
    
    #Set up the near and far depthcue distances.
    if dc_DepthNear < 0.0:
        dc_DepthNear = Dist4Initial - Data4Radius
    if dc_DepthFar  < 0.0:
        dc_DepthFar  = Dist4Initial + Data4Radius
    dc_DFar_DNear = dc_DepthFar - dc_DepthNear
    
    #Initialize the 3D reference cube vertices and edges.
    for ii in range(OBJ_VSTART):
        VertList[ii] = RefCubeVert[ii]

    for ii in range(OBJ_ESTART):
        EdgeList[ii] = RefCubeEdge[ii]
        
    #Set up the depthcue color map.
    for rgb in range(3):
        range = dc_ColorFar[rgb] - dc_ColorNear[rgb] #Color Component Range
        if range < 0: range-=1
        else: range+=1
        for ii in range(dc_Levels):
            cmap[400+ii][rgb] = (dc_ColorNear[rgb])+((ii * range) / dc_Levels)
    InitDisplay()
def main():
    Initialize()
    CalcV3Matrix()
    CalcV4Matrix()
    ProjectTo3D()
    ProjectToScreen()
    DrawStatus()