# decorator for timing
def time_this(original_function):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = original_function(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken by {original_function.__name__}: {end_time - start_time}s")
        return result

    return wrapper


def grid_transpose(_grid):
    _transposed_grid = []
    for i in range(len(_grid)):
        _transp_list = []
        for g in _grid:
            _transp_list.append(g[i - 1])
        _transposed_grid.append(_transp_list)
    return _transposed_grid

@time_this
def check_grid_validity(_grid):
    from itertools import chain
    # row check
    for i in range(1, 10):
        for g in _grid:
            if g.count(i) > 1:
                pass
                return False

    # column check
    _transposed_grid = grid_transpose(_grid)
    for i in range(1, 10):
        for g in _transposed_grid:
            if g.count(i) > 1:
                return False

    # block check
    # try to implement block check
    # check itertools
    _square_list = []
    for i in range(0,len(_grid),3):
        for j in range(0,len(_grid),3):
            _square_list.append(list(chain.from_iterable([_row[j:j+3] for _row in _grid[i:i+3]])))
    for i in range(1,10):
        for _square in _square_list:
            if _square.count(i) > 1:
                return False

    return True

@time_this
def grid_print(_grid):
    for _line in _grid:
        for i, _val in enumerate(_line):
            if i == 0:
                print(f"|{_val}|", end="")
            else:
                print(f"{_val}|", end="")
        print("\r")


# solver is the recursive function that solves the puzzle.
# Algorithm:
# 1. Check for empty cells (populated with 0). The first one is fetched in a tuple. If there are no empty cells, the
#    grid is solved, so we break out of solver. If there is an empty cell, continue.
# 2. Try each number in 1-9 to check if it will be a valid entry in the grid. If valid, enter that number
#    in that position. If not valid, next iteration.
# 3. Call solver recursively on updated grid. End state of solver should be no empty cells.

# @time_this
def solver(_grid):
    _empty_cell = find_empty(_grid)
    if not _empty_cell:
        return True
    else:
        _row, _col = _empty_cell
        for _num in range(1, 10):
            if valid_entry(_grid, _num, (_row, _col)):
                _grid[_row][_col] = _num

                if solver(_grid):
                    return True
                _grid[_row][_col] = 0

    return False


# valid_entry function checks the validity of an entry in the grid at the given position
# 1. Check if the given value appears in the row indicated by the position tuple. If so, return False.
# 2. Check if the given value appears in the column indicated by the position tuple.
# 3. Check if the given value appears in the sector. Sector is found by _row//3,_col//3.
#    (0,0) -> (2,2) -> (0,0)
#    (3,0) -> (3,2) -> (1,0)
# 4. If all checks pass, return True.

def valid_entry(_grid, _num, _pos):
    _column = []
    _row, _col = _pos[0], _pos[1]
    if _num in _grid[_row] and _grid[_row][_col] != _num:
        return False

    # column check
    for _line in _grid:
        _column.append(_line[_col])
    if _num in _column and _column[_row] != _num:
        return False

    # block check
    _box_x = _col // 3
    _box_y = _row // 3

    for i in range(_box_y * 3, _box_y * 3 + 3):
        for j in range(_box_x * 3, _box_x * 3 + 3):
            if _num == _grid[i][j] and (i, j) != (_row, _col):
                return False

    return True


# find_empty returns the first 0 it encounters

def find_empty(_grid):
    for i,row in enumerate(_grid):
        for j,val in enumerate(row):
            if row[j] == 0:
                return i, j
    return None


@time_this
def __main__():
    board = [[2,9,0,0,0,0,0,7,0],
       [3,0,6,0,0,8,4,0,0],
       [8,0,0,0,4,0,0,0,2],
       [0,2,0,0,3,1,0,0,7],
       [0,0,0,0,8,0,0,0,0],
       [1,0,0,9,5,0,0,6,0],
       [7,0,0,0,9,0,0,0,1],
       [0,0,1,2,0,0,3,0,6],
       [0,3,0,0,0,0,0,5,9]]
    print(check_grid_validity(board))
    grid_print(board)
    print("_" * 50)
    solver(board)
    print("_" * 50)
    grid_print(board)
    print(check_grid_validity(board))


__main__()
