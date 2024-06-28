from typing import List, Tuple, Union

class Array:
    def __init__(self, data: Union[List[int], List[List[int]]]):
        # 2D Array Case
        if isinstance(data[0], list):
            self.data = data
            self.shape = (len(data), len(data[0]))
        else:
            # 1D Array Case
            self.data = [data]
            self.shape = (1, len(data))

    def __repr__(self) -> str:
        # Représentation en chaîne de caractères pour l'affichage.
        return f"{self.data}"

    def __len__(self) -> int:
        if self.shape[0] == 1:
            return self.shape[1]
        else:
            return self.shape[0]

    def __getitem__(self, idx: Union[int, Tuple[int, int], slice]) -> Union[int, List[int]]:
        # Gestion de l'indexage et du slicing.
        if isinstance(idx, tuple):
            # Indexation pour un tableau 2D.
            return self.data[idx[0]][idx[1]]
        elif isinstance(idx, slice):
            # Slicing pour un tableau 1D ou 2D.
            if self.shape[0] == 1:
                return self.data[0][idx]
            else:
                # Slicing pour obtenir les lignes spécifiées.
                return self.data[idx]       
        else:
            # Indexation pour un tableau 1D.
            if self.shape[0] == 1:
                return self.data[0][idx]
            else:
                return self.data[idx]

    # Addition élément par élément.
    def __add__(self, other: Union['Array', int]) -> 'Array':
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise addition.") 
            result = [
                [sum(pair) for pair in zip(row1, row2)]  
                for row1, row2 in zip(self.data, other.data)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x + other for x in self.data[0]]]
            else:
                # 2D Array Case
                result = [
                    [x + other for x in row]
                    for row in self.data
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Array' and '{}'".format(type(other)))
        
    # Addition Commutative
    def __radd__(self, other: Union['Array', int]) -> 'Array':
        return self.__add__(other)

    # Soustraction élément par élément.
    def __sub__(self, other: Union['Array', int]) -> 'Array':
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise subtraction.")
            result = [
                [x - y for x, y in zip(row1, row2)]  
                for row1, row2 in zip(self.data, other.data)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x - other for x in self.data[0]]]
            else:
                # 2D Array Case
                result = [
                    [x - other for x in row]
                    for row in self.data
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Array' and '{}'".format(type(other)))

    # Soustraction commutative
    def __rsub__(self, other: Union['Array', int]) -> 'Array':
        return self.__sub__(other)
    
    # Multiplication élément par élément et par un scalaire
    def __mul__(self, other: Union['Array', int]) -> 'Array':
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise multiplication.") 
            result = [
                [x * y for x, y in zip(row1, row2)]  
                for row1, row2 in zip(self.data, other.data)
            ] 
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
                # 1D Array Case
                result = [[x * other for x in self.data[0]]]
            else:
                # 2D Array Case
                result = [
                    [x * other for x in row]
                    for row in self.data
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Array' and '{}'".format(type(other)))

    # Multiplication Commutative
    def __rmul__(self, other: Union['Array', int]) -> 'Array':
        return self.__mul__(other)
    
    # Division élément par élément.
    def __truediv__(self, other: Union['Array', int]) -> 'Array':
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise division.")
            result = [
                [x / y for x, y in zip(row1, row2)]
                for row1, row2 in zip(self.data, other.data)
            ]
            return Array(result)
        elif isinstance(other, int) or isinstance(other, float):
            if self.shape[0] == 1:
            # 1D Array Case
                result = [[x / other for x in self.data[0]]]
            else:
            # 2D Array Case
                result = [
                    [x / other for x in row]
                    for row in self.data
                ]
            return Array(result)
        else:
            raise TypeError("Unsupported operand type(s) for /: 'Array' and '{}'".format(type(other)))
        
        
    # Divison commutative
    def __rtruediv__(self, other: Union['Array', int]) -> 'Array':
        return self.__truediv__(other)
     
    # Produit scalaire pour les tableaux 1D uniquement.
    def __matmul__(self, other: 'Array') -> int:        
        if self.shape[0] != 1 or other.shape[0] != 1:
            raise ValueError("Dot product is only supported for 1D arrays.")
        if self.shape[1] != other.shape[1]:
            raise ValueError("Shapes must be the same for dot product.")
        # Calcul du produit scalaire.
        return sum(self.data[0][i] * other.data[0][i] for i in range(self.shape[1]))

    # Recherche d'un élément avec l'opérateur 'in'.
    def __contains__(self, item: int) -> bool:  
        for row in self.data:
            if item in row:
                return True
        return False

# Tests de démonstration
if __name__ == "__main__":
    a = Array([1, 2, 3])
    b = Array([7, 5, 6])
    c = Array([[1, 2], [3, 4]])
    h = Array([[1, 2], [3, 4]])
    g = Array([[1, 2], [3, 4], [5, 6], [7, 8]])
    d = Array([4, 5, 5, 6, 8, 14])
    e = Array([8, 9, 5, 6, 8, 32])
    f = d + e

    print(b.shape)
    print(c.shape)
    print()

    print(c + h)
    print(c - h)
    print(c * h)
    print(c / h)
    print("Add")
    print(c + 1)
    print(1 + c)
    print("Mul")
    print(c * 2)
    print(2 * c)
    print("Sub")
    print(c - 2)
    print(2 - c)
    print("Div")
    print(c / 2)
    print(2 / c)
    print("Scalar Product")
    print(a @ b)
    print("Search")
    print(4 in a)  # True
    print(c[1, 1])  # 4
    print(g[:2])
    print(c[1:2])
