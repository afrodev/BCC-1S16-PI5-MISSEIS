
'''
from math import sqrt, asin

class Vector3D(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    # define as funcoes como propriedades da classe, assim pode ser acessada pela outra classe
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

    
    
    def __mul__(self, other):
        return Vector3D(self._x*other._x, self._y*other._y, self._z*other._z)
    def mag(self):
        return sqrt((self._x)^2 + (self._y)^2 + (self._z)^2)
    def dot(self, other):
        temp = self * other
        return temp._x + temp._y + temp._z
    def cos_theta(self):
        #vector's cos(angle) with the z-axis
        return self.dot(Vector3D(0,0,1)) / self.mag() #(0,0,1) is the z-axis unit vector
    def phi(self):
        #vector's 
        return asin( self.dot(Vector3D(0,0,1)) / self.mag() )
    def __repr__(self):
        return "({x}, {y}, {z})".format(x=self._x, y=self._y, z=self._z)
    
    
    
    
    
    
    
if __name__ == "__main__":
    samplevector = Vector3D(1,1,1)
    print(samplevector)
    print(samplevector.mag())
    print(samplevector*Vector3D(1,1,1))
    print(samplevector.cos_theta())
    print(samplevector.phi())
    
'''