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
    

mon_tableau_2d = Array([[1, 2], [3, 4], [5, 6], [7, 8]])
print(mon_tableau_2d)
print(mon_tableau_2d.elements)
print(mon_tableau_2d.shape)  