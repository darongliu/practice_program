'''
using sat solver to solve soduku
'''
from satispy import Variable, Cnf
from satispy.solver import Minisat

def main():
    all_origin_number = {}

    for i in range(9):
        while True:
            row_input = input('please input '+str(i+1)+' row: ')
            if valid_input(row_input):
                break
        for j in range(9):
            if row_input[j] != 'n':
                all_origin_number[(i,j)] = int(row_input[j])-1

    all_variable = [[[Variable('v'+str(i)+str(j)+str(k)) for k in range(9)] for j in range(9)] for i in range(9)]
    true_var = Variable('v_true')

    exp = true_var
    exp = exp & all_element(all_variable, true_var)
    exp = exp & valid_all(all_variable, true_var)

    for keys in all_origin_number.keys():
        exp = exp & all_variable[keys[0]][keys[1]][all_origin_number[keys]]

    solver = Minisat()
    solution = solver.solve(exp)
    if solution.success:
        for i in range(9):
            print('row'+str(i+1)+': ',end='')
            for j in range(9):
                for index, var in enumerate(all_variable[i][j]):
                    if solution[var]:
                        print(index+1,end='')
                        break
            print('\n',end='')
    else:
        print('no solution')

def all_element(list_var, true_var):
    exp = true_var
    for i in range(9):
        for j in range(9):
            exp = exp & one_element(list_var[i][j], true_var)
    return exp

def one_element(list_var, true_var):
    exp = list_var[0]
    for i in range(8):
        exp = exp | list_var[i+1]

    exp2 = true_var
    for i in range(9):
        for j in range(9):
            if j<=i:
                continue
            exp2 = exp2 & ((-list_var[i])|(-list_var[j]))
    return exp & exp2

def valid_all(all_list_var, true_var):
    exp=true_var
    for i in range(9):
        exp = exp & valid(all_list_var[i], true_var)
    for i in range(9):
        exp = exp & valid([list_var[i] for list_var in all_list_var], true_var)
    for i in [0,3,6]:
        for j in [0,3,6]:
            list_var = []
            for index in range(3):
                for index2 in range(3):
                    list_var.append(all_list_var[i+index][j+index2])
            exp = exp & valid(list_var, true_var)
    return exp

def valid(list_var, true_var):
    #list_var is list of list
    exp=true_var
    for i in range(9):
        for j in range(9):
            if j<=i :
                continue
            for d in range(9):
                exp = exp & ((-list_var[i][d])|(-list_var[j][d]))
    return exp


def merge_var(v1, v2):
    if v1 is None:
        return v2
    if v2 is None:
        return v1
    return v1 & v2
def valid_input(input_str):
    used_number = {}
    for i in range(9):
        used_number[str(i+1)]=False
    if len(input_str) != 9:
        print('length is not nine')
        return False
    for char in input_str:
        if char not in '123456789n':
            print('have invalid char')
            return False
        if char != 'n':
            if used_number[char] == True:
                print('have repeat number')
                return False
            else:
                used_number[char] = True
    return True

if __name__ == '__main__':
    main()
    #print(valid_input('12nnn58nn'))
