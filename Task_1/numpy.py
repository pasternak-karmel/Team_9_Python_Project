ARRAY_SHAPE_ERROR = "Arrays must have the same shape"
class Array:
    # Initialize the array
    def __init__(self, elements):
        if isinstance(elements[0], list):
            # 2D array case
            self.elements = elements
            self.shape = (len(elements), len(elements[0]))
        else:
            # 1D array case
            self.elements = [elements]
            self.shape = (1, len(elements))
        self.index = 0

    # Print the array
    def __repr__(self) -> str:
        return f"Array(elements={self.elements}, shape={self.shape})"
    
    # Add two arrays
    def __add__(self, other):
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError(ARRAY_SHAPE_ERROR) 
            result = [
                [sum(pair) for pair in zip(row1, row2)]  
                for row1, row2 in zip(self.elements, other.elements)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x + other for x in self.elements[0]]]
            else:
                # 2D Array Case
                result = [
                    [x + other for x in row]
                    for row in self.elements
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Array' and '{}'".format(type(other)))
        
     # Subtract two arrays
    def __sub__(self, other):
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError(ARRAY_SHAPE_ERROR) 
            result = [
                [x - y for x, y in zip(row1, row2)]  
                for row1, row2 in zip(self.elements, other.elements)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x - other for x in self.elements[0]]]
            else:
                # 2D Array Case
                result = [
                    [x - other for x in row]
                    for row in self.elements
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Array' and '{}'".format(type(other)))
    

    # Multiply two arrays  
    def __mul__(self, other):
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError(ARRAY_SHAPE_ERROR) 
            result = [
                [x * y for x, y in zip(row1, row2)]  
                for row1, row2 in zip(self.elements, other.elements)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x * other for x in self.elements[0]]]
            else:
                # 2D Array Case
                result = [
                    [x * other for x in row]
                    for row in self.elements
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Array' and '{}'".format(type(other)))
    
    # Commutative addition 
    def __radd__(self, other):
        return self.__add__(other)
    
    # Commutative multiplication
    def __rmul__(self, other):
        return self.__mul__(other)
    
    # Support for len()
    def __len__(self):
        if self.shape[0] == 1:
            return self.shape[1]
        else:
            return self.shape[0]
        
    # scalar product for 1D arrays
    
        
# Test Operations
D2_Array = Array([[8, 2], [1, 2]])
D1_Array = Array([[1, 2], [1, 2]])
D_Array = D1_Array - D2_Array
print(D_Array)
print(D_Array.elements)
print(D1_Array.shape)  


