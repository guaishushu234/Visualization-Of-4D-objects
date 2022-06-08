from vector import *

global DepthCue,dc_ColorFar,dc_ColorNear,dc_DepthFar,dc_DepthNear,dc_Levels,RefCube,RotSpace,RotPlane,Vangle3,Vangle4,Project3,Project4,camp,Form3,Form4,Over4,To3,To4,Up3,Up4
global Data4Radius,Dist3Auto,Dist3Initial,Dist4Auto,Dist4Initial,Root3,Tan2Vangle3,Tan2Vangle4,dc_DFar_DNear
global VertList,EdgeList,NumEdges,NumVerts

cmap = ((  0,  0,  0),(120,120,120),(  0,255,  0),(255,255,  0),
        (  0,  0,255),(255,  0,255),(  0,255,255),(255,255,255),
        (255,  0,  0),(200,200,200),(100,100,100),(188,255,  0),
        (  0,  0,128),(  0,128,128),(  0,256,128),(128,  0,128),
        (128,128,128),(128,256,128),(256,128,128),(256,256,128),
        (  0,128,  0),(  0,128,256),(128,128,  0),(128,128,256),
        (256,128,256),(128,  0,  0),(128,  0,256),(128,256,  0)) #Color Map
for i in range(512): cmap.append((0, 0, 0))

From3 = Vector3(10,11,13)  #3D Viewpoint
To3   = Vector3(0,0,0)     #3D Target Point
Up3   = Vector3(0,0,1)     #3D Up Vector
Vangle3 = 45.0             #3D View Angle

From4 = Vector4(0,0,0,100) #4D Viewpoint
To4   = Vector4(0,0,0,0)   #4D Target Point
Up4   = Vector4(0,0,1,0)   #4D Up View Vector
Over4 = Vector4(0,1,0,0)   #4D Other Up View Vector
Vangle4 = 45.0             #4D View Angle

DepthCue = True                      #boolean / DepthCue Switch
dc_ColorFar = (63, 63, 63)           #RGBvalue / Far DepthCue Color
dc_ColorNear = (244,244,244)         #RGBvalue / Near DepthCue Color
dc_DepthFar = -1.0                   #Real / Far DepthCue Distance
dc_DepthNear = -1.0                  #Real / Near DepthCue Distance
dc_Levels = 16                       #short / Number of DepthCue Levels
RefCube = True                       #boolean / 3D Reference Cube Switch
RotSpace = 3                         #ushort / Dimension of Rotation (3 or 4)
RotPlane = 0                         #ushort / Rotation Plane, Index to `rp'
Project3 = 1                         #uchar / 3D View Type
Project4 = 1                         #uchar / 4D View Type


#Defined Constants
DB_DEPTHCUE=0
EPSILON = 1e-10

PI=3.14159265358979323846

#Status Box Dimensions
AXES_WIDTH=136
SBOX_WIDTH=136
SBOX_HEIGHT=40

#ViewMode Values
PERSPECTIVE=1#Perspective-Projection
PARALLEL=2#Parallel-Projection
AUTOSIZE=3#Automatic-Sized Perspective Projection

XMAXSCREEN=1920
YMAXSCREEN=1080

XMAX=XMAXSCREEN
YMAX=YMAXSCREEN

if XMAX > YMAX:		#MAXSCREEN is the largest box
    MAXSCREEN=YMAX	#(in pixels) that can be
else:				#displayed on the screen.
    MAXSCREEN=XMAX

XCENTER=((XMAXSCREEN+1-SBOX_WIDTH)/2) #Screen Center Coordinates
YCENTER=((YMAXSCREEN+1)/2)

OBJ_VSTART=8	#Start of Object Vertices
OBJ_ESTART=12	#Start of Object Edges


#Axes Display Box Constants and Macros
def AXES_INTERIOR(x,y):	return (x),(y),(x)+AXES_WIDTH-1,(y)+AXES_WIDTH-1
def AXES_OUTLINE(x,y): return (x)-1,(y)-1,(x)+AXES_WIDTH,(y)+AXES_WIDTH

AXES3D_X=(XMAX-1-AXES_WIDTH)	#4D Axes Display Box
AXES3D_Y=(YMAX-1-AXES_WIDTH)

AXES4D_X=(XMAX-1-AXES_WIDTH)	#3D Axes Display Box
AXES4D_Y=(AXES3D_Y-AXES_WIDTH-10)


#Status Display Box Constants and Macros
def SBOX_INTERIOR(x,y): return (x),(y),(x)+SBOX_WIDTH-1,(y)+SBOX_HEIGHT-1
def SBOX_OUTLINE(x,y): return (x)-1,(y)-1,(x)+SBOX_WIDTH,(y)+SBOX_HEIGHT

SB_3DPROJ_X=(XMAX-SBOX_WIDTH)	#4D Projection Status
SB_3DPROJ_Y=(AXES4D_Y-25-SBOX_HEIGHT)

SB_4DPROJ_X=(XMAX-SBOX_WIDTH)	#3D Projection Status
SB_4DPROJ_Y=(SB_3DPROJ_Y-10-SBOX_HEIGHT)

SB_ROTSPC_X=(XMAX-SBOX_WIDTH)    #Rotation Dimension Status
SB_ROTSPC_Y=(SB_4DPROJ_Y-10-SBOX_HEIGHT)

SB_ROTPLN_X=(XMAX-SBOX_WIDTH)    #Rotation Plane Status
SB_ROTPLN_Y=(SB_ROTSPC_Y-10-SBOX_HEIGHT)


#Keyboard Menu Location
KEYMENU_X=(XMAX-SBOX_WIDTH)	#Key Menu Left Side
KEYMENU_Y=1			#Key Menu Bottom Side

def Radians(degrees): return (((degrees) / 180.0) * PI)
def streqic(s1,s2): return (s1.upper() == s2.upper())

#ifdef _STDC_
#   define ARGS(arglist)	arglist
#else
#   define ARGS(arglist)	()
#endif

#if (GL_LEVEL < 1)
#   define  subpixel(x)		/* empty macro */
#endif
