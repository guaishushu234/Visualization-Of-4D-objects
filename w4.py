from constants import *
import math

def CalcV3Matrix():
    global Va, Vb, Vc
    Vc = To3-From3
    norm = Vc.norm()
    if norm == 0.0:
        raise ValueError("To Point and From Point are the same")
    Vc = Vc / norm
    Va.cross(Vc, Up3)
    norm = Va.norm()
    if norm == 0.0:
        raise ValueError("Invalid Up Vector")
    Va = Va / norm
    Vb.cross(Va,Vc)

def CalcV4Matrix():
    global Wa, Wb, Wc, Wd
    Wd = To4 - From4
    norm = Wd.norm()
    if norm < EPSILON:
        raise ValueError("4D To Point and From Point are the same")
    Wd = Wd / norm

    Wa.cross(Up4,Over4,Wd)
    norm = Wd.norm()
    if norm < EPSILON:
        raise ValueError("4D up, over and view vectors are not perpendicular")
    Wa = Wa / norm

    Wb.cross(Over4,Wd,Wa)
    norm = Wb.norm()
    if norm < EPSILON:
        raise ValueError("Invalid 4D over vector")
    Wb = Wb / norm

    Wc.cross(Wd,Wa,Wb)
   
def ProjectToScreen():
    global NumVerts, VertList
    if Project3 == PARALLEL:
        rtemp  = 1.0 / Root3
    else:
        pconst = 1.0 / Tan2Vangle3

    if RefCube: ii=0
    else: ii = OBJ_VSTART

    while ii < NumVerts:
        vert = VertList[ii]
        TempV = vert.project - From3

        if Project3 != PARALLEL:
            rtemp = pconst / TempV.dot(Vc)

        vert.x = rtemp * TempV.dot(Va)
        vert.y = rtemp * TempV.dot(Vb)

        ii += 1
        
def ProjectTo3D():
    global NumVerts, VertList
    if Project4 == PARALLEL:
        rtemp  = 1.0 / Data4Radius
    else:
        pconst = 1.0 / Tan2Vangle4

    ii = OBJ_VSTART

    while ii < NumVerts:
        vert = VertList[ii]
        TempV = vert.position - From4

        vert.depth = TempV.dot(Wd)

        if Project4 != PARALLEL:
            rtemp = pconst / vert.depth

        vert.project.x = rtemp * TempV.dot(Wa)
        vert.project.y = rtemp * TempV.dot(Wb)
        vert.project.z = rtemp * TempV.dot(Wc)

        ii += 1

def Rotate3View(Cos, Sin, rp1, rp2, To, From, Up):
#    Real     Cos, Sin;   /* Cosine and Sine of the Rotation Angle */
#    int      rp1, rp2;   /* The Coordinate Indices of the Rotation Plane */
#    Vector3  To;         /* To Point (Rotate About This Point) */
#    Vector3  From, Up;   /* The 3D From and Up Vectors */
    # Rotate the from-vector.
    t1 = Cos * (From[rp1]-To[rp1])  +  Sin * (From[rp2]-To[rp2])
    t2 = Cos * (From[rp2]-To[rp2])  -  Sin * (From[rp1]-To[rp1])
    From[rp1] = t1 + To[rp1]
    From[rp2] = t2 + To[rp2]
    # Rotate the Up Vector
    t1 = Cos * Up[rp1]  +  Sin * Up[rp2]
    t2 = Cos * Up[rp2]  -  Sin * Up[rp1]
    Up[rp1] = t1
    Up[rp2] = t2
    CalcV3Matrix()
    ProjectToScreen()

def Rotate4View(Cos, Sin, rp1, rp2, To, From, Up, Over):
    # Real     Cos, Sin;           /* Cosine and Sine of the Rotation Angle */
    # int      rp1, rp2;           /* Coordinate Indices of Rotation Plane */
    # Vector4  To;                 /* To Point (Rotate About This Point) */
    # Vector4  From, Up, Over;     /* The 4D From, Up and Over Vectors */
    # Rotate the from-vector.
    t1 = Cos * (From[rp1]-To[rp1])  +  Sin * (From[rp2]-To[rp2])
    t2 = Cos * (From[rp2]-To[rp2])  -  Sin * (From[rp1]-To[rp1])
    From[rp1] = t1 + To[rp1]
    From[rp2] = t2 + To[rp2]
    # Rotate the Up Vector.
    t1 = Cos * Up[rp1]  +  Sin * Up[rp2]
    t2 = Cos * Up[rp2]  -  Sin * Up[rp1]
    Up[rp1] = t1
    Up[rp2] = t2
    # Rotate the Over Vector
    t1 = Cos * Over[rp1]  +  Sin * Over[rp2]
    t2 = Cos * Over[rp2]  -  Sin * Over[rp1]
    Over[rp1] = t1
    Over[rp2] = t2
    CalcV4Matrix()
    ProjectTo3D()
    ProjectToScreen()

def Initialize():
    global Root3, Tan2Vangle3, Tan2Vangle4, Dist3Initial, Dist3Auto, Dist4Initial, Dist4Auto, Data4Radius
    global cmap, dc_DepthNear, dc_DepthFar, dc_DFar_DNear
    global VertList, EdgeList, NumVerts, NumEdges
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
        rangee = dc_ColorFar[rgb] - dc_ColorNear[rgb] #Color Component Range
        if rangee < 0: rangee-=1
        else: rangee+=1
        for ii in range(dc_Levels):
            cmap[400+ii][rgb] = (dc_ColorNear[rgb]) + ((ii * rangee) / dc_Levels)
    
def GenerateScene():
    print("OK")

def main():
    global VertList, EdgeList, NumVerts, NumEdges
    
    AddVertex = ((-1,-1,-1,-1),( 1,-1,-1,-1),( 1, 1,-1,-1),(-1, 1,-1,-1),
                 (-1,-1, 1,-1),( 1,-1, 1,-1),( 1, 1, 1,-1),(-1, 1, 1,-1),
	             (-1,-1,-1, 1),( 1,-1,-1, 1),( 1, 1,-1, 1),(-1, 1,-1, 1),
	             (-1,-1, 1, 1),( 1,-1, 1, 1),( 1, 1, 1, 1),(-1, 1, 1, 1))
    VertList = [(0,0,0,0) for _ in range(OBJ_VSTART)]
    VertList = VertList + [Vertex(i) for i in AddVertex]
    NumVerts = 16

    AddEdge = ((0, 1, 3),(1, 2, 2),(2, 3, 3),(3, 0, 5),
               (4, 5, 3),(5, 6, 2),(6, 7, 3),(7, 4, 5),
               (0, 4, 5),(1, 5, 2),(2, 6, 2),(3, 7, 5),
               (8, 9, 3),(9,10, 2),(0,11, 3),(1, 8, 5),
               (2,13, 3),(3,14, 2),(4,15, 3),(5,12, 5),
               (8,12, 5),(9,13, 2),(0,14, 2),(1,15, 5),
               (0, 8, 5),(1, 9, 2),(2,10, 2),(3,11, 5),
               (4,12, 5),(5,13, 2),(6,14, 2),(7,15, 5))
    EdgeList = [(0,0,0) for _ in range(OBJ_ESTART)]
    EdgeList = EdgeList + [Edge(i) for i in AddEdge]
    NumEdges = 32
    
    Initialize()
    CalcV3Matrix()
    CalcV4Matrix()
    ProjectTo3D()
    ProjectToScreen()
    GenerateScene()
if __name__ == "__main__":
    main()