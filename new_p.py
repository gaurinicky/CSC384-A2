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
     has a single element which is the size N; it represents the
     dimension of the square board.

     Every other list represents a constraint a cage imposes by
     having the indexes of the cells in the cage (each cell being an
     integer out of 11,...,NN), followed by the target number and the
     operator (the operator is also encoded as an integer with 0 being
     '+', 1 being '-', 2 being '/' and 3 being '*'). If a list has two
     elements, the first element represents a cell, and the second
     element is the value imposed to that cell. With this representation,
     the input will look something like this:

     [[N],[cell_ij,...,cell_i'j',target_num,operator],...]

       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {1-N}.

       This model will also contain BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.) and an n-ary constraint for each cage in the grid.
    '''

    ##IMPLEMENT
    size = kenken_grid.pop(0)[0]
    variable_array = [[x for x in range(size)] for y in range(size)]
    domain = []
    vars = []
    map_vars_row = []
    string_row = []
    map_vars_column = [[] for x in range(size)]
    string_column = []
    string_row = []
    cons = []
    mapVars = {}

    #initialize domain range for vars------------------------------------------
    for i in range (1, size+1):
      domain.append(i)

    #is range inclusive? -- it is [1,size)
    for i in range (0,size):
      row = []
      for j in range(0,size):
        variable_array[i][j] = Variable("(V{}{})".format(i+1,j+1), domain)
        vars.append(variable_array[i][j])
        row.append(variable_array[i][j])
        map_vars_column[j].append(variable_array[i][j])
        mapVars[int(str(i+1) + str(j+1))] = variable_array[i][j]
      map_vars_row.append(row)


    #-----------------------------------------------------------------------------

    # #binary constraints of not equal between all pairs of vars in the same row, column--------------

    rowCon=[]
    for i in range(size):
      for j in range(size-1):
        for k in range (j+1, size):
          rowCon.append(binaryTupleConstraint(int(str(i+1) + str(j+1)),int(str(i+1) + str(k+1)), mapVars))
          #cons.append(con)
    colCon = []
    for j in range(size):
      for i in range(size-1):
        for k in range (i+1, size):
          colCon.append(binaryTupleConstraint(int(str(i+1) + str(j+1)),int(str(k+1) + str(j+1)), mapVars))


    #-------------------------------------------------------------------------------------------
      # allRow = []
      # for i in range(len(map_vars_row)):
      #   name = "C({0})".format(",".join(var.name[-2:] for var in map_vars_row[i]))
      #   con = Constraint(name, map_vars_row[i])
      #   allRow.append(con)

      #-------------------------------------------------------------------------------------------
      # allCol = []
      # for i in range(len(map_vars_column)):
      #   name = "C({0})".format(",".join(var.name[-2:] for var in map_vars_column[i]))
      #   con = Constraint(name, map_vars_column[i])
      #   allCol.append(con)
    #---------------------------------------------------------------------
    #pop values to not have to deal with them
    # create constraints
    # do the permutations possible to satisfy that value
    cageCons = []
    for cage in kenken_grid:
      operator = cage.pop()
      target_num = cage.pop()
      cageSize = len(cage)
      cageVars = []
      stringName = "C("
      #print("cagesize: ",cageSize)
      sat_tuples = []
      #in the case that target num becomes the cage coord and operator the value [44,3]
      if(cageSize == 0 ):
        cageVars.append(mapVars.get(target_num))
        stringName += "V"+ str(target_num)+")"
        con = Constraint("C(V{})".format(target_num),cageVars)
        # (operator,) makes a one element tuple
        sat_tuples.append((operator,))
      else:
        for i in range(cageSize-1):
          cageVars.append(mapVars.get(cage[i]))
          #print(cage[i])
          stringName += "V"+str(cage[i])+","
        cageVars.append(mapVars.get(cage[cageSize-1]))
        #print(cage[cageSize-1])
        #print("-----------------------------")
        stringName += "V"+ str(cage[cageSize-1])+")"

        con = Constraint(stringName, cageVars)
        #do some math see if value combinations = target as satsifying tuple
        #take the different combinations of the domain including doubles equal to the size of the cage
        #4444 2312   231
        tuples = list(set(itertools.product(domain, repeat = cageSize)))
        for t in tuples:
          #print(t)
          if findCageTuples(t, cageSize, operator, target_num, cageVars):
            sat_tuples.append(t)
            # print("-------")
            # print (t )
            # print (stringName,"targetnum: ",target_num, "operator:",operator,"cagesize:",cageSize)
            # print("----------")
      con.add_satisfying_tuples(sat_tuples)
      cageCons.append(con)


    #---------------------------------------------------------------------------------------------------

    cons = rowCon + colCon + cageCons
    #-----------------------------------------------------------------------------------
    csp = CSP("{}->>>KenKen".format(size), vars)
    for c in cons:
        csp.add_constraint(c)

    return csp, variable_array

def findCageTuples(tupleVal, cageSize, operator, target_num, cageVars):
    '''Return array of satisfying tuples
    '''
    # for i in range(cageSize):
    #   if tupleVal[i] not in cageVars[i].domain():
    #     return False
    # add
    if(operator == 0):
      result = tupleVal[0]
      for i in range(1, cageSize):
        result += tupleVal[i]
    #subtract
    elif(operator == 1):
      tuples = list(set(itertools.permutations(tupleVal, cageSize)))
      for t in tuples:
        result = t[0]
        for i in range(1, cageSize):
          result -= t[i]
        if result == target_num:
          return True
    #divide
    elif(operator == 2):
      tuples = list(set(itertools.permutations(tupleVal, cageSize)))
      for t in tuples:
        result = t[0]
        for i in range(1, cageSize):
          result /= t[i]
        if result == target_num:
          return True
    #multiply
    else:
      result = tupleVal[0]
      for i in range(1, cageSize):
        result *= tupleVal[i]
    return result == target_num

def binaryTupleConstraint(var1Key, var2Key, mapVars):
  var1 = mapVars[var1Key]
  var2 = mapVars[var2Key]

  con = Constraint("C(V{},V{})".format(var1Key,var2Key),[var1, var2])
  sat_tuples = []
  for value1 in var1.domain():
    for value2 in var2.domain():
      if value1!=value2:
        sat_tuples.append((value1, value2))
  con.add_satisfying_tuples(sat_tuples)

  return con
