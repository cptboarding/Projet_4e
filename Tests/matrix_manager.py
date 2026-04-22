
def create_matrix(dim: tuple[int, int] | list[int, int]) -> list:
    return [[None for j in range(dim[0])] for i in range(dim[1])]
