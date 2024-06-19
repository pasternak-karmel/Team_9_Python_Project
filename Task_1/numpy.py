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
    

D2_Array = Array([[1, 2], [3, 4], [5, 6], [7, 8]])
print(D2_Array)
print(D2_Array.elements)
print(D2_Array.shape)  