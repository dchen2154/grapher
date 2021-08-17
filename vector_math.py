# This is a library of vector classes that allows for simple initialization of
# vectors and operations for vectors. A coordinate vector class is also created
# to allow for traditional addition, scalaing, and inner products of vectors.


# Defines vectors as a collection of objects with addition and scaling operations.
class Vector(object):
    # If there is only one input, then consider the first parameter as a list 
    # of entries for the vector. If not, then consider all the parameters as a
    # list of entries.
    def __init__(self,*elements):
        if len(elements) == 0:
            raise Exception(f"Vector object must contain elements.")
        elif len(elements) == 1:
            self.elements = tuple([ element for element in elements[0] ])
        else:
            self.elements = elements

    # Prints out a one-line string of the elements of a vector.
    def __repr__(self):
        return "(" + ", ".join([str(element) for element in self.elements]) + ")"
    
    def __add_(self,other):
        raise NotImplementedError

    def __mul__(self,other):
        raise NotImplementedError

# Class of coordinate vectors with traditional addition, scalar multiplication, 
# and inner product.
class coordVector(Vector):

    def __init__(self,*elements):
        if len(elements) == 1:
            super().__init__(elements[0])
        else:
            super().__init__(elements)
        for element in self.elements:
            if not isinstance(element,int) and not isinstance(element,float):
                raise Exception(f"Coordinate vector cannot have nonnumeric entries. {elements}")

    # Defines vector addition to be addition on corresponding entries.
    # Overwrite for a different defintion of vector addition.
    def __add__(self,other):
        if not isinstance(other,coordVector):
            raise Exception(f"{other} is not a coordinate Vector.")
        if len(self.elements) != len(other.elements):
            raise Exception(f"{self} and {other} do not have compatible size.")
        return coordVector([ self.elements[i] + other.elements[i] for i in range(len(self.elements)) ])

    # Defines vector scaling to be a number multiplied with each entry of a 
    # vector.
    # Overwrite for a different definition of vector scaling.
    def __rmul__(self,other):
        if isinstance(other,float) or isinstance(other,int):    
            return coordVector([ other*element for element in self.elements ])
        else:
            raise Exception(f"{other} is not a number.")
    
    # Defines the inner product of two vectors as the sum of the product of 
    # corresponding entries.
    # Overwrite for a different definiton of inner product.
    def __mul__(self,other):
        if not isinstance(other,Vector):      
            raise Exception(f"{other} is not a coordinate vector.")
        elif len(self.elements) != len(other.elements):
            raise Exception(f"{self} and {other} do not have compatible size.")
        if len(self.elements) > 0:
            try:
                self.elements[0] * other.elements[0]
            except:
                raise Exception(f"* operator not defined for {self} and {other}.")
        return sum([ self.elements[i]*other.elements[i] for i in range(len(self.elements)) ])
    
    def __neg__(self):
        return coordVector([-1*element for element in self.elements])
