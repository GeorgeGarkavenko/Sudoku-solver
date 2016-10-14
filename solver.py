""" Small script that solve every sudok """

blueprint_layout = (
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    )

initial_layout = (
    [6, 0, 0, 0, 0, 1, 7, 0, 5], 
    [0, 0, 0, 0, 0, 5, 9, 0, 4], 
    [8, 0, 0, 7, 0, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0, 0, 6, 2, 0], 
    [0, 2, 0, 0, 0, 0, 0, 3, 0], 
    [0, 9, 4, 0, 0, 0, 0, 0, 1], 
    [0, 0, 0, 0, 0, 8, 0, 0, 3], 
    [9, 0, 3, 1, 0, 0, 0, 0, 0], 
    [2, 0, 5, 6, 0, 0, 0, 0, 7], 
    )

initial_layout = blueprint_layout

NUMBERS = set(range(1,10))

iterations = 0



def main():
    """ Main routine """
    global iterations
    
    import time
    
    addreses = []
    
    hints_count = sum(1 if initial_layout[i][j] else 0 for j in range(9) for i in range(9))
    
    layout = tuple(elem[:] for elem in initial_layout)
    
    layout_to_update = True
    
    start = time.time()
    
    # 1. Handle empty cells with one posible variant 

    while(layout_to_update):
        
        layout_to_update = False
        
        t_layout = zip(*layout)
        
        quadrants = tuple( [tuple(qudrant_numbers(layout, row, col)) for col in range(3)] for row in range(3) )
        
        for row in range(9):
            for col in range(9):
                iterations += 1
                
                if layout[row][col]:
                    all_numbers = layout[row] + list(t_layout[col]) + list(quadrants[row / 3][col / 3])
                    current_numbers = filter(lambda x: x == layout[row][col], all_numbers)
                    assert len(current_numbers) == 3, "Redundancy at ({0}, {1})".format(row, col)
                    continue
                
                posible_numbers = NUMBERS - \
                    set(layout[row]) - \
                    set(t_layout[col]) - \
                    set(quadrants[row / 3][col / 3])
                # no number
                assert posible_numbers, "Inconsistent layout"
                # one number
                if len(posible_numbers) == 1:
                    layout[row][col] = posible_numbers.pop()
                    layout_to_update = True
                    addreses = []
                    break
                # two and more numbers
                else:
                    addreses.append((row, col))
            if layout_to_update:
                break
        
    pre_iterations = iterations
    pre_solved_numbers = sum(1 if layout[i][j] else 0 for j in range(9) for i in range(9))- hints_count
    
    # 2. Handle empty cells with [2..9] posible variant 
    findSolution(layout, addreses)
    
    print "Hints: {0}, pre solved: {1}".format(hints_count, pre_solved_numbers)
    print "Iterations: {0}, (pre iterations: {1}, post iterations {2})".format(iterations, pre_iterations, iterations - pre_iterations) 
    print "Time to pass: ", time.time() - start
    
    
    
def findSolution(layout, addreses):
    """ Find sudoku solution with use depth-first algorithm """
    global NUMBERS
    
    global iterations
    iterations += 1
    
    if iterations % 100000 is 0:
        print "Iterations: {}".format(iterations)
    
    if not addreses:
        print "Result: "
        for l in layout:
            for cell in l:
                print cell,'\t',
            print
        return True
    
    i, j = addreses[0]
    
    row = set(layout[i])
    col = set( zip(*layout)[j] )
    quadrant = set( qudrant_numbers(layout, i / 3, j / 3) )
    
    posible_numbers = NUMBERS - row - col - quadrant
    
    for n in sorted(posible_numbers):
        layout[i][j] = n
        if findSolution(layout, addreses[1:]):
            return True
    
    layout[i][j] = 0
    
    return False
    


def qudrant_numbers(layout, row, col):
    """ Get 3x3 matrix of sudoku layout """
    row_range = range(row * 3, (row + 1) * 3)
    col_range = range(col * 3, (col + 1) * 3)
    
    return (layout[i][j] for i in row_range for j in col_range)


if __name__ == "__main__":
    main()
