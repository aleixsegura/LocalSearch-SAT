"""
Horn solver for positive clauses. 
"""
import argparse
import time
import subprocess
import matplotlib.pyplot as plt
import numpy as np

file = None
plot = False

clauses = []
unitaries = []
composed = []
times = []

def parse_clauses() -> None:
    with open(file) as f:
        for clause in f:
            negatives = clause[:clause.find(',')]
            positive = clause[clause.find(',') + 1: len(clause)].strip()
            if not negatives:
                unitaries.append(positive)
            else:
                clauses.append((negatives, positive))

def simplify() -> None:
    global composed
    new_unitaries_discovered = []
    composed = [clause for clause in clauses if not clause[1] in unitaries]

    for i, element in enumerate(composed):
        positive = element[1]
        negatives = element[0]
        if len(positive) == 0: # case: no => positive so can't erase from left part (negatives)
            continue
        for unitary in unitaries:
            if unitary in element[0]:
                negatives = negatives.replace(unitary, '').strip() 
        composed[i] = (negatives, element[1])
        if len(negatives) == 0:
            new_unitaries_discovered.append(element[1])
    propagate_new(new_unitaries_discovered)

def propagate_new(new_unitaries_discovered) -> None:
    global composed
    composed = [clause for clause in composed if not clause[1] in new_unitaries_discovered]

def solve():
    for expr in composed:
        negatives = expr[0].split()
        positive = expr[1]
        if positive == '' and all(var in unitaries for var in negatives):
            return False
    return True

def parse_args() -> None:
    global file, plot
    parser = argparse.ArgumentParser(description='solver for Horn clauses')
    parser.add_argument('-p', '--plot', action='store_true', help='for multiple executions of different sizes and plot')
    parser.add_argument('clauses', metavar='clauses', type=str, help='file with valid Horn clauses')
    
    args = parser.parse_args()
    plot = args.plot
    file = args.clauses
    
def run() -> None:
    if plot:
        number_of_clauses = [x * 10 * 2 for x in range(1, 50)]
        probilities = []
        for size in number_of_clauses:
            probilities.append(compute_complexity(size))
        graph(number_of_clauses, probilities)
    else:
        parse_clauses()
        simplify()
        print(solve())

def compute_complexity(size: int) -> float:
    global clauses, unitaries, composed, times
    local_times = []
    iterations = 25
    sat = 0

    unitaries_to_gen = '5'
    variables_per_clause_to_gen = '4'
    for _ in range(iterations):
        subprocess.run(['python', 
                            'generator.py', unitaries_to_gen, str(size), variables_per_clause_to_gen
                        ])
        start = time.time()
        parse_clauses()
        simplify()
        if solve(): 
            sat += 1
        local_times.append(time.time() - start)
        clauses, unitaries, composed = [], [], []

    mean_time = (sum(local_times)) / iterations
    times.append(mean_time * 1000)
    return sat / iterations

def graph(clauses: list[int], probabilities: list[int]) -> None:
    plt.style.use('seaborn-bright')
    fig, ax = plt.subplots()
    ax.scatter(clauses, probabilities, color='blue', edgecolor='black', linewidth=1, alpha=0.75)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_title('Satisfiability Complexity')
    ax.set_xlabel('Number of clauses')
    ax.set_ylabel('Probability')

    ax2 = ax.twinx()
    ax2.scatter(clauses, times, color='red', edgecolor='black', linewidth=1 ,alpha=0.75)
    ax2.set_ylim(min(times), max(times))
    ax2.set_ylabel('Hardness (ms)')

    # Trend lines
    degree_probabilities = 2  
    degree_times = 2  
    trend_probabilities = np.polyfit(clauses, probabilities, degree_probabilities)
    trend_times = np.polyfit(clauses, times, degree_times)
    ax.plot(clauses, np.polyval(trend_probabilities, clauses), color='lightblue', linewidth=2, label='probability')
    ax2.plot(clauses, np.polyval(trend_times, clauses), color='lightcoral', linewidth=2, label='time')
    ax.legend(loc='upper center')
    ax2.legend(loc='upper right')
    plt.show()

def main() -> None:
    parse_args()
    start = time.time()
    run()
    elapsed = time.time() - start
    print(f'Time of the execution = {elapsed}')

if __name__ == '__main__':
    main() 
