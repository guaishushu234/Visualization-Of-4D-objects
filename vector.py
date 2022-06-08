import numpy as np

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        (self.x, self.y, self.z) = (x, y, z)
    def __mul__(self, k):
        return Vector3(self.x * k, self.y * k, self.z * k)
    def __rmul__(self, k):
        return Vector3(self.x * k, self.y * k, self.z * k)
    def __truediv__(self, k):
        return Vector3(self.x / k, self.y / k, self.z / k)
    # def __rtruediv__(self, k):
    #     return Vector3(k.x / self.x, k.y / self.y, k.z / self.z)
    def __add__(self, k):
        return Vector3(self.x + k.x, self.y + k.y, self.z + k.z)
    def __sub__(self, k):
        return Vector3(self.x - k.x, self.y - k.y, self.z - k.z)
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    def dot(self, k):
        return (self.x * k.x) + (self.y * k.y) + (self.z * k.z)
    def __abs__(self):
        return self.dot(self)
    def __str__(self):
        return 'Vector3(%s,%s,%s)'%(self.x,self.y,self.z)
    def norm(self):
        return np.sqrt(abs(self))
    def normalize(self):
        return self * (1/self.norm())
    def components(self):
        return (self.x, self.y, self.z)
    def nparray(self, type=0):
        arr= np.array([self.x, self.y, self.z])
        if type == 1: return arr
        elif type == 0: return np.transpose(arr)
    def cross(self, u, v):
        u = u.components()
        v = v.components()
        
        self.x = (u[1] * v[2]) - (u[2] * v[1])
        self.y = (u[2] * v[0]) - (u[0] * v[2])
        self.z = (u[0] * v[1]) - (u[1] * v[0])
        
        #return Vector3(x, y, z)

class Vector4:
    def __init__(self, x=0, y=0, z=0, w=0):
        (self.x, self.y, self.z, self.w) = (x, y, z, w)
    def __mul__(self, k):
        return Vector4(self.x * k, self.y * k, self.z * k, self.w * k)
    def __rmul__(self, k):
        return Vector4(self.x * k, self.y * k, self.z * k, self.w * k)
    def __truediv__(self, k):
        return Vector4(self.x / k, self.y / k, self.z / k, self.w / k)
    # def __rtruediv__(self, k):
    #     return Vector4(k.x / self.x, k.y / self.y, k.z / self.z, k.w / self.w)
    def __add__(self, k):
        return Vector4(self.x + k.x, self.y + k.y, self.z + k.z, self.w + k.w)
    def __sub__(self, k):
        return Vector4(self.x - k.x, self.y - k.y, self.z - k.z, self.w - k.w)
    def __neg__(self):
        return Vector4(-self.x, -self.y, -self.z, -self.w)
    def dot(self, k):
        return (self.x * k.x) + (self.y * k.y) + (self.z * k.z) + (self.w * k.w)
    def __abs__(self):
        return self.dot(self)
    def __str__(self):
        return 'Vector4(%s,%s,%s,%s)'%(self.x,self.y,self.z,self.w)
    def norm(self):
        return np.sqrt(abs(self))
    def normalize(self):
        return self * (1/self.norm())
    def components(self):
        return (self.x, self.y, self.z, self.w)
    def nparray(self, type=0):
        arr= np.array([self.x, self.y, self.z, self.w])
        if type == 1: return arr
        elif type == 0: return np.transpose(arr)
    def cross(self, u, v, k):
        u = u.components()
        v = v.components()
        k = k.components()
        
        A = (v[0] * k[1]) - (v[1] * k[0])
        B = (v[0] * k[2]) - (v[2] * k[0])
        C = (v[0] * k[3]) - (v[3] * k[0])
        D = (v[1] * k[2]) - (v[2] * k[1])
        E = (v[1] * k[3]) - (v[3] * k[1])
        F = (v[2] * k[3]) - (v[3] * k[2])
        
        self.x =   (u[1] * F) - (u[2] * E) + (u[3] * D)
        self.y = - (u[0] * F) + (u[2] * C) - (u[3] * B)
        self.z =   (u[0] * E) - (u[1] * C) + (u[3] * A)
        self.w = - (u[0] * D) + (u[1] * B) - (u[2] * A)
        
        #return Vector4(x, y, z, w)

class Vertex:
    def __init__(self, position:tuple):
        (x, y, z, w) = position
        self.position = Vector4(x, y, z, w)
        self.project = Vector3(x, y, z)
        (self.x, self.y, self.depth) = (0, 0, 0)

class Edge:
    def __init__(self, arg:tuple):
        self.v1 = arg[0]
        self.v2 = arg[1]
        self.color = arg[2]