from pysat.solvers import Glucose3
import sys

file = None
g = Glucose3()

def add_clauses():
     with open(file) as f:
        for clause in f:
            sep_index = clause.index(',')
            left_part = clause[:sep_index].split()
            negatives = [int(var) * -1 for var in left_part if not var.isspace()]
            positive = clause[sep_index + 2]
            if positive.isspace() or positive == '\n':
                g.add_clause(negatives)
            else:
                add = negatives + [int(positive)]
                g.add_clause(add)
        f.close()
            
if __name__ == '__main__':
    file = sys.argv[1]
    add_clauses()
    print(g.solve())
    print(g.get_model())