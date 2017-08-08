#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools

def kenken_csp_model(kenken_grid):
    '''Returns a CSP object representing a Kenken CSP problem along
       with an array of variables for the problem. That is return

       kenken_csp, variable_array

       where kenken_csp is a csp representing the kenken model
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the board (indexed from (0,0) to (N-1,N-1))


       The input grid is specified as a list of lists. The first list
	   has a single element which is the grid_size_n N; it represents the
	   dimension of the square board.

	   Every other list represents a constraint a cage imposes by
	   having the indexes of the cells in the cage (each cell being an
	   integer out of 11,...,NN), followed by the target countber and the
	   operator (the operator is also encoded as an integer with 0 being
	   '+', 1 being '-', 2 being '/' and 3 being '*'). If a list has two
	   elements, the first element represents a cell, and the second
	   element is the value imposed to that cell. With this representation,
	   the input will look something like this:

	   [[N],[cell_ij,...,cell_i'j',target_count,operator],...]

       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {1-N}.

       This model will also contain BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.) and an n-ary constraint for each cage in the grid.
    '''

    ##IMPLEMENT
    #(0=’+’, 1=’-’, 2=’/’, 3=’*’).
    global final_tuple
    global cons
    global grid_size_n
    grid_size_n = kenken_grid[0][0]
    variables = []
    var_array = []
    max_domain = grid_size_n + 1
    global final_tuple
    global permutations
    cage = kenken_grid[1:]
    count = 1
    global combinations
    global scope
    MAX_SIZE = 10 # base to divide the digits to get the coordinates for x and y

    domain = list(range(1, max_domain))
    #Initialize the grid
    for i in range(grid_size_n):
        var_array.append([])
        for j in range(grid_size_n):
            var_name = "V" + str(i) + str(j)
            variables = Variable(var_name, domain)
            var_array[i].append(variables)

    variables = var_array

    cons = []
    #row_cons = float("inf")
    #row constraint

    row_cons = [binary(i, j1, i, j2, variables)
                for i in range(grid_size_n)
                for j1 in range(grid_size_n) for j2 in range(grid_size_n)
                if j1 < j2]

    col_cons = [binary(i1, j, i2, j, variables)
                for j in range(grid_size_n)
                for i1 in range(grid_size_n) for i2 in range(grid_size_n)
                if i1 < i2]

    #total row and column constraint
    rc = row_cons + col_cons


    #cage formation

    for i in cage:

        scope = []
        coordinates = []
        operator = i[-1]
        value = i[-2]

        for var in i[:-2]:
            #print("var," i[-2])
            length = len(i[:-2])
            if (var > 0):
                cx = (var // MAX_SIZE)
                cy = (var % MAX_SIZE)
                scope.append(variables[cx-1][cy-1])
                coordinates.append((cx, cy))
            '''elif (var == 0):
                cx = 0
                cy = 0
                scope.append(variables[cx][cy])
                coordinates.append((cx, cy))'''


        x = set([int(cx[0]) for cx in coordinates])
        y = set([int(cy[1]) for cy in coordinates])



        if (len(x) > 1) and (len(y) > 1):
            combinations = list(itertools.combinations_with_replacement(range(1, max_domain), length))

        else:
            combinations = list(itertools.combinations(range(1, max_domain), length))


        final_tuple = []
        op_cons = operators(operator, value)
        #rc += op_cons


    #cons.extend(row_cons)
    #cons.extend(col_cons)
    cons.extend(rc)
    v_new = []

    for i in range(len(variables)):
        for j in range(len(variables)):
            v_new.append(variables[i][j])
    kenken_csp = CSP("kenken_csp", v_new)
    for c in cons:
        kenken_csp.add_constraint(c)
    return kenken_csp, variables


def binary(i, j, i2, j2, variables):
    var1 = variables[i][j]
    var2 = variables[i2][j2]
    name = "RC({0},{1})".format(var1.name[-2:], var2.name[-2:])
    scope = [var1, var2]
    constraint = Constraint(name, scope)
    sat_tup = [(v1, v2) for v1 in var1.domain() for v2 in var2.domain() if v1 != v2]
    constraint.add_satisfying_tuples(sat_tup)
    return constraint



def operators(operator, value):
    count = 1
    for tup in combinations:
        #to get all possible combinations
        #(361) would have length 3
        permutations = list(itertools.permutations(list(tup), len(tup)))
        if operator == 0:
            for p in permutations:
                result = p[0] #get the first number
                for n in range(1, len(p)):
                    result = result + p[n]
                if result == value:
                    final_tuple.extend(permutations)
        if operator == 1:
            for p in permutations:
                result = p[0] #get first number in tuple
                for n in range(1, len(p)):
                    result = result - p[n]
                if result == value:
                    final_tuple.extend(permutations)
        if operator == 2:
            for p in permutations:
                result = p[0]
                for n in range(1, len(p)):
                    result = result / p[n]
                if result == value:
                    final_tuple.extend(permutations)
        if operator == 3:
            for p in permutations:
                result = p[0]
                for n in range(1, len(p)):
                    result = result * p[n]
                if result == value:
                    final_tuple.extend(permutations)


    name = "N({0})".format(count)
    count += 1
    constraint = Constraint(name, scope)
    constraint.add_satisfying_tuples(final_tuple)

    #return constraint
    cons.append(constraint)
