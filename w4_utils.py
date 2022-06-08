from vector import *
from constants import *

global Va, Vb, Vc
global Wa, Wb, Wc, Wd

Va = Vector3();Vb = Vector3();Vc = Vector3()
Wa = Vector4();Wb = Vector4();Wc = Vector4();Wd = Vector4()

class Vertex:
    def __init__(self, position:tuple, project:tuple):
        self.position = Vector4(position)
        self.project = Vector3(project)
        (self.x, self.y, self.depth) = (0, 0, 0)
class Edge:
    def __init__(self, arg:tuple):
        self.v1 = arg[0]
        self.v2 = arg[1]
        self.color = arg[2]

def CalcV3Matrix():
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
    Wd = To4 - Form4
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

        vert.project[0] = rtemp * TempV.dot(Wa)
        vert.project[1] = rtemp * TempV.dot(Wb)
        vert.project[2] = rtemp * TempV.dot(Wc)

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