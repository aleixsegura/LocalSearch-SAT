"""
Generator of Horn clauses of the form 
        x1 and x2 ... xN ==> y
where x and y are positives in the starting point. 
"""
import random
import os
import argparse

nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
void = ' ' 
num_unitaries = 0
num_clauses = 0
propositional_vars_per_clause = 0

def main():
    if os.path.exists('clauses.txt'):
        os.remove('clauses.txt')
    parse_args()
    generate_clauses()
    generate_unitaries()

def generate_clauses():
    global num_clauses, propositional_vars_per_clause, num_unitaries
    
    if propositional_vars_per_clause == 1:
        alrdy_chosed = []
        with open('clauses.txt', '+a') as f:
            for _ in range(num_clauses):
                clause = random.choice(nums)
                while clause in alrdy_chosed:
                    clause = random.choice(nums)
                f.write(clause + ', ' + '\n')
                alrdy_chosed.append(clause)
            f.close(); return

    clause = ''
    with open('clauses.txt', '+a') as f:
        while num_clauses > 0:
            for x in range(propositional_vars_per_clause):
                propositional_var = random.choice(nums)
                while propositional_var in clause.split():
                    propositional_var = random.choice(nums)
                if x == propositional_vars_per_clause - 2:
                    clause += propositional_var + ','
                elif x == propositional_vars_per_clause - 1:
                    while propositional_var in clause.split() or propositional_var in clause[len(clause) - 2]: # or in 'char,'
                        propositional_var = random.choice(nums + [void])
                    formatted_var = ' ' + propositional_var
                    clause += formatted_var
                else:
                    formatted_var = propositional_var
                    if x <= propositional_vars_per_clause - 3: # while not last var of 'left_part (char,)'
                        clause += formatted_var + ' '
                    else:
                        clause += formatted_var #
            f.write(clause + '\n')
            clause = '' 
            num_clauses -= 1
        f.close()    
    
def generate_unitaries():
    global num_unitaries
    unitaries = []

    with open('clauses.txt', '+a') as f:
        for _ in range(num_unitaries):
            unitarie = ', '
            choice = random.choice(nums)
            unitarie += choice
            while unitarie in unitaries:
                unitarie = ', ' + random.choice(nums)
            unitaries.append(unitarie)

            with open('clauses.txt', '+a') as f:
                f.write(unitarie + '\n')
        f.close()

def parse_args():
    global num_clauses, propositional_vars_per_clause, num_unitaries
    parser = argparse.ArgumentParser(description='a generator of Horn clauses')
    parser.add_argument('unitaries', metavar='U unitaries', type=int, help='number of unitary clauses')
    parser.add_argument('num_of_clauses', metavar='C clauses', type=int, help='number of clauses to be generated')
    parser.add_argument('variables_per_clause', metavar='V propositional variables', type=int, help='number of propositional variables per clause')
    args = parser.parse_args()
    num_unitaries = args.unitaries
    num_clauses = args.num_of_clauses
    propositional_vars_per_clause = args.variables_per_clause
    
if __name__ == '__main__':
    main()
    