import sys
import random
import matplotlib.pyplot as plt
import timeit
import copy
import math

iterations = 50

class Problem:
   def __init__(self, size : int):
      self.size = size
      self.solution = list(range( size ))
      for i, _ in enumerate( self.solution ):
         self.solution[ i ] = random.randint( 0, size-1 ) 
      self.cost = 0
      self.computeCost()
         
   def __str__(self):
      result = "\n"
      for x in range( self.size ):
         row = ""
         for y in range( self.size ):
            if self.solution[x] == y:
               row += "X|"
            else:
               row += " |"
         result += '|' + row + '\n'
      return str(self.cost) # result + str(self.solution) + ' ' +
      
   def __lt__(self, s2):
      return self.cost < s2.cost
      
   def computeCost(self): 
      self.cost = 0
      for x in range( self.size ):
         for y in range( x+1, self.size ): 
            if self.solution[x] == self.solution[y]:
               self.cost += 1
            if abs(y - x) == abs(self.solution[x] - self.solution[y]):
               self.cost += 1
      return 
      
def local_search( size : int, num_tries : int ):
   problem = Problem( size )
   for x in range( num_tries ):
      new_problem = Problem( size )
      if new_problem < problem:
         problem = new_problem
   return problem

def local_search2( size : int, num_tries : int ):
   problem = Problem( size )
   for x in range( num_tries ):
      new_problem = Problem( size )
      if new_problem < problem:
         problem = new_problem
      for i in range( size ):
         cloned = copy.deepcopy(problem)
         cloned.solution[i] = (cloned.solution[i] + 1) % size
         cloned.computeCost()
         if cloned < problem:
            problem = cloned
   return problem


def simulated_annealing( size : int, num_tries : int, temperature = 1 ):
   """ simulated annealing """
   cooling_val = 1 / (size * num_tries)
   problem = Problem( size )
   for _ in range( num_tries ):
      new_problem = Problem( size )
      if new_problem < problem:
         problem = new_problem
      for i in range( size ):
         cloned = copy.deepcopy(problem)
         cloned.solution[i] = random.randint(0, size - 1)
         cloned.computeCost()
         if cloned < problem:
            problem = cloned
         elif cloned > problem:
            cost_difference = cloned.cost - problem.cost
            P = 1 - math.exp(-1 / cost_difference) # normalized P (range [0, 1]) related to cost difference
            rand = random.random()
            if P > rand and temperature > rand:
               problem = cloned
         if temperature - cooling_val >= 0:
            temperature -= cooling_val
         else:
            temperature = 0
   return problem


def time_complexity(size: int, tries: int) -> list[float]:
   execution_time_LS = timeit.timeit(lambda: local_search(size, tries), number=iterations)
   execution_time_LS2 = timeit.timeit(lambda: local_search2(size, tries), number=iterations)
   execution_time_SAnnealing = timeit.timeit(lambda: simulated_annealing(size, tries), number=iterations)
   return [execution_time_LS, execution_time_LS2, execution_time_SAnnealing]

def compute_mean_cost(size: int, tries: int) -> list[float]:
   LS_costs, LS2_costs, SAnnealing_costs = [], [], []

   for _ in range(iterations):
      problem = local_search(size, tries)
      LS_costs.append(problem.cost)
   mean_LS = sum(LS_costs) / iterations

   for _ in range(iterations):
      problem = local_search2(size, tries)
      LS2_costs.append(problem.cost)
   mean_LS2 = sum(LS2_costs) / iterations

   for _ in range(iterations):
      problem = simulated_annealing(size, tries)
      SAnnealing_costs.append(problem.cost)
   mean_SAnnealing = sum(SAnnealing_costs) / iterations

   return [mean_LS, mean_LS2, mean_SAnnealing]

def plot(times: list[float], solution_qualities: list[float]) -> None:
   colors = ['green', 'red', 'blue']
   alphas = [1, 0.75, 0.5]
   labels = ['Basic Local Search', 'Neighborhood Local Search', 'Simulated Annealing']
   plt.style.use('seaborn-bright')
   fig, ax = plt.subplots()
   for time, quality, color, label, alpha in zip(times, solution_qualities, colors, labels, alphas):
        ax.scatter(time, quality, linewidth=1, edgecolor='black', alpha=alpha, color=color, s=250, label=label)
   ax.set_title(f'Time complexity and solution quality ({iterations} iterations)')
   ax.set_xlabel('Time (s)')
   ax.set_ylabel('Mean cost')

   plt.legend(loc='lower left')
   plt.show()

if __name__ == "__main__":
   size, tries = int(sys.argv[1]), int(sys.argv[2])
   solving_times = time_complexity(size, tries)
   solution_qualities = compute_mean_cost(size, tries)
   print(f'Random basic local search has mean cost of {solution_qualities[0]} '
      f'with mean time complexity of {round(solving_times[0], 2)}s '
      f'with {iterations} iterations.')

   print(f'Neighborhood local search has mean cost of {solution_qualities[1]} '
      f'with mean time complexity of {round(solving_times[1], 2)}s '
      f'with {iterations} iterations.')
   
   print(f'Simulated annealing has mean cost of {solution_qualities[2]} '
      f'with mean time complexity of {round(solving_times[2], 2)}s '
      f'with {iterations} iterations.')
   
   plot(solving_times, solution_qualities)