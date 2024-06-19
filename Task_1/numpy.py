class Array:
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

    def __repr__(self) -> str:
        return f"Array(elements={self.elements}, shape={self.shape})"
    
    def __add__(self, other):
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Arrays must have the same shape") 
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
       
    # Commutative addition 
    def __radd__(self, other):
        return self.__add__(other)
    
D2_Array = Array([[1, 2], [3, 4]])
D1_Array = Array([[1, 2], [3, 4]])
D_Array = 5 + D2_Array
print(D_Array)
print(D_Array.elements)
print(D_Array.shape)  