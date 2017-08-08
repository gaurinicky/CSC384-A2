from kenken_csp import *
from propagators import *
from orderings import *

test_ord_mrv = False;
test_props = True;

boards = [ [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]],
[[4],[11,21,6,3],[12,13,3,0],[14,24,3,1],[22,23,7,0],[31,32,2,2],[33,43,3,1],[34,44,6,3],[41,42,7,0]],
[[5],[11,21,4,1],[12,13,2,2],[14,24,1,1],[15,25,1,1],[22,23,9,0],[31,32,3,1],[33,34,44,6,3],[35,45,9,0],[41,51,7,0],[42,43,3,1],[52,53,6,3],[54,55,4,1]],
[[6],[11,21,11,0],[12,13,2,2],[14,24,20,3],[15,16,26,36,6,3],[22,23,3,1],[25,35,3,2],[31,32,41,42,240,3],[33,34,6,3],[43,53,6,3],[44,54,55,7,0],[45,46,30,3],[51,52,6,3],[56,66,9,0],[61,62,63,8,0],[64,65,2,2]],
[[5],[11,12,21,22,10,0],[13,14,23,24,34,18,0],[15,25,35,2,1],[31,32,33,1,1],[41,42,43,51,52,53,600,3],[44,54,55,2,2],[45,3]],
[[6],[11,12,13,2,2],[14,15,3,1],[16,26,36,11,0],[21,22,23,2,2],[24,25,34,35,40,3],[31,41,51,61,14,0],[32,33,42,43,52,53,3600,3],[44,54,64,120,3],[45,46,55,56,1,1],[62,63,5,1],[65,66,5,0]]]


'''boards = [[[9],[11,12,21,240,3],[13,22,23,12,0],[15,16,5,1],[17,27,72,3],[18,28,38,7,0],[19,29,2,2],[24,33,34,56,3],[25,26,11,0],[31,32,2,2],[35,36,46,10,0],[37,47,48,42,3],[39,49,59,69,79,27,0],[41,51,2,2],[42,43,44,19,0],[45,55,65,16,0],[53,54,1,1],[56,57,58,24,0],[61,71,72,73,252,3],[62,63,64,6,0],[66,75,76,216,3],[67,68,77,15,0],[74,84,94,16,0],[78,88,98,90,3],[81,91,92,23,0],[82,83,93,15,0],[85,86,3,1],[95,96,2,1],[87,97,12,3],[89,99,7,1]],
[[4],[11,12,21,16,3],[13,22,23,9,3],[24,34,2,2],[31,32,41,3,3],[33,42,43,32,3]],
[[8],[11,21,31,22,576,3],[12,13,23,33,17,0],[14,15,24,14,0],[16,17,26,21,3],[18,27,28,38,448,3],[25,34,35,5,3],[36,37,46,47,22,0],[41,42,51,52,8,0],[43,44,45,15,0],[48,58,67,68,72,3],[53,63,73,42,3],[54,55,65,75,18,0],[56,57,66,76,1920,3],[61,62,72,120,3],[64,74,2,2],[77,78,87,88,11,0],[81,82,30,3],[83,84,85,86,21,0]]]'''


def print_kenken_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":

    if test_props:
        for b in boards:
            print("Solving board")
            csp, var_array = kenken_csp_model(b)
            solver = BT(csp)
            print("=======================================================")
            #print("FC")
            #solver.bt_search(prop_FC, ord_mrv)
            print("GAC")
            solver.bt_search(prop_GAC)
            print("Solution")
            print_kenken_soln(var_array)

    if test_ord_mrv:

        a = Variable('A', [1])
        b = Variable('B', [1])
        c = Variable('C', [1])
        d = Variable('D', [1])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        count = 0
        for i in range(0,len(simpleCSP.vars)):
            simpleCSP.vars[count].add_domain_values(range(0, count))
            count += 1

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[0].name):
                print("Passed First Ord MRV Test")
            else:
                print("Failed First Ord MRV Test")
        else:
           print("No Variable Returned from Ord MRV")

        a = Variable('A', [1,2,3,4,5])
        b = Variable('B', [1,2,3,4])
        c = Variable('C', [1,2])
        d = Variable('D', [1,2,3])
        e = Variable('E', [1])

        simpleCSP = CSP("Simple", [a,b,c,d,e])

        var = []
        var = ord_mrv(simpleCSP)

        if var:
            if((var.name) == simpleCSP.vars[len(simpleCSP.vars)-1].name):
                print("Passed Second Ord MRV Test")
            else:
                print("Failed Second Ord MRV Test")
        else:
           print("No Variable Returned from Ord MRV")
