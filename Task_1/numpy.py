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
                return self.data[idx]       
        else:
            # Indexation pour un tableau 1D.
            if len(self.shape) == 1:
                return self.data[0][idx]
            else:
                return self.data[idx]

    def __add__(self, other: Union['Array', int]) -> 'Array':
        # Addition élément par élément.
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise addition.")
            if len(self.shape) == 1:
                # Addition élément par élément pour les tableaux 1D.
                result = [self.data[0][i] + other.data[0][i] for i in range(self.shape[0])]
            else:
                # Addition élément par élément pour les tableaux 2D.
                result = [[self.data[i][j] + other.data[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
        else:
            # Addition d'un scalaire à chaque élément.
            if len(self.shape) == 1:
                result = [elem + other for elem in self.data[0]]
            else:
                result = [[elem + other for elem in row] for row in self.data]
        return Array(result if len(self.shape) > 1 else result)

    def __sub__(self, other: Union['Array', int]) -> 'Array':
        # Soustraction élément par élément.
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise subtraction.")
            if len(self.shape) == 1:
                # Soustraction élément par élément pour les tableaux 1D.
                result = [self.data[0][i] - other.data[0][i] for i in range(self.shape[0])]
            else:
                # Soustraction élément par élément pour les tableaux 2D.
                result = [[self.data[i][j] - other.data[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
        else:
            # Soustraction d'un scalaire à chaque élément.
            if len(self.shape) == 1:
                result = [elem - other for elem in self.data[0]]
            else:
                result = [[elem - other for elem in row] for row in self.data]
        return Array(result if len(self.shape) > 1 else result)

    def __mul__(self, other: Union['Array', int]) -> 'Array':
        # Multiplication élément par élément.
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise multiplication.")
            if len(self.shape) == 1:
                # Multiplication élément par élément pour les tableaux 1D.
                result = [self.data[0][i] * other.data[0][i] for i in range(self.shape[0])]
            else:
                # Multiplication élément par élément pour les tableaux 2D.
                result = [[self.data[i][j] * other.data[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
        else:
            # Multiplication d'un scalaire à chaque élément.
            if len(self.shape) == 1:
                result = [elem * other for elem in self.data[0]]
            else:
                result = [[elem * other for elem in row] for row in self.data]
        return Array(result if len(self.shape) > 1 else result)

    def __truediv__(self, other: Union['Array', int]) -> 'Array':
        # Division élément par élément.
        if isinstance(other, Array):
            # Vérification que les shapes correspondent.
            if self.shape != other.shape:
                raise ValueError("Shapes must be the same for element-wise division.")
            if len(self.shape) == 1:
                # Division élément par élément pour les tableaux 1D.
                result = [self.data[0][i] / other.data[0][i] for i in range(self.shape[0])]
            else:
                # Division élément par élément pour les tableaux 2D.
                result = [[self.data[i][j] / other.data[i][j] for j in range(self.shape[1])]
                          for i in range(self.shape[0])]
        else:
            # Division d'un scalaire à chaque élément.
            if len(self.shape) == 1:
                result = [elem / other for elem in self.data[0]]
            else:
                result = [[elem / other for elem in row] for row in self.data]
        return Array(result if len(self.shape) > 1 else result)

    def __matmul__(self, other: 'Array') -> int:
        # Produit scalaire pour les tableaux 1D uniquement.
        if self.shape[0] != 1 or other.shape[0] != 1:
            raise ValueError("Dot product is only supported for 1D arrays.")
        if self.shape[1] != other.shape[1]:
            raise ValueError("Shapes must be the same for dot product.")
        # Calcul du produit scalaire.
        return sum(self.data[0][i] * other.data[0][i] for i in range(self.shape[1]))

    def __contains__(self, item: int) -> bool:
        # Recherche d'un élément avec l'opérateur 'in'.
        for row in self.data:
            if item in row:
                return True
        return False

# Tests de démonstration
if __name__ == "__main__":
    a = Array([1, 2, 3])
    b = Array([7, 5, 6])
    c = Array([[1, 2], [3, 4]])
    d = Array([4, 5, 5, 6, 8, 14])
    e = Array([8, 9, 5, 6, 8, 32])
    f = d + e

    print(b.shape)
    print()

    print(c)  # Array([[1, 2], [3, 4]])
    print(c * 2)  # ([[2, 4], [6, 8]])
    print(a @ b) # 35
    print(4 in a)  # True
    print(c[1, 1])  # 4
    print(c[:1])  # [[1], [2]]
    print([row[1] for row in c.data])  # [2, 4]
    print(d + e)  
    print()# Array([[12, 14, 10, 12, 16, 46]])
    print(12 in f)  # True
    print(a.shape)
    print(c.data)  # Array([[1, 2], [3, 4]])
