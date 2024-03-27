"""
A basic pattern for the implementation of a genetic algorithm 
to solve the n-queens problem.
"""

import random
import sys
import matplotlib.pyplot as plt

def fitness_function(chromosome : list[int]) -> int:
    """Computes the fitness from a chromosome (conflicts)""" 
    cost = 0
    for x in range(len(chromosome)):
         for y in range(x + 1, len(chromosome)): 
            if chromosome[x] == chromosome[y]:
               cost += 1
            if abs(y - x) == abs(chromosome[x] - chromosome[y]): 
               cost += 1
    return cost

def compute_conflicts(population: list[list[int]]) -> int:
    """ Computes the total conflicts of a population """
    return sum(fitness_function(chromosome) for chromosome in population)

def badness(chromosome: list[int], conflicts: int) -> float:
    """ Computes how bad (in %) is a given chromosome in relation of it's population """
    return round(fitness_function(chromosome) / conflicts, 2) * 100

def select_mate(population : list[list[int]]) -> list[int]:
    """Selects one of the members in the population """
    conflicts = compute_conflicts(population)
    normalized_probabilities = [100 - badness(chromosome, conflicts) for chromosome in population]
    return random.choices(population, weights=normalized_probabilities, k=1)[0]

def crossover(mate1 : list[int], mate2 : list[int]) -> list[int]:
    """Creates a new offspring from the crossover of mate1 and mate2"""
    size = len(mate1)
    mate1_range = mate1[:size // 2]
    mate2_range = mate2[size // 2:]
    return mate1_range + mate2_range

def mutate(chromosome : list[int], mutation_probability : float) -> list[int]:
    """Mutates one of the genes in the chromosome"""
    probabilities = [mutation_probability, 1 - mutation_probability]
    mutate = [True, False]
    if random.choices(mutate, weights=probabilities, k=1)[0]:
        chromosome[random.randint(0, len(chromosome) - 1)] = random.randint(0, len(chromosome) - 1)
    return chromosome

def create_generation(population : list[list[int]], mutation_prob = 0.03) \
    -> list[list[int]]:
    """
    Creates a new generation. Original implementation.
    """
    next_generation = []
    for _ in range(len(population)):
        mate1 = select_mate(population)
        mate2 = select_mate(population)
        offspring = crossover(mate1, mate2)
        offspring = mutate(offspring, mutation_prob)
        next_generation += [offspring]
    return next_generation

def create_elitist_generation(population : list[list[int]], mean: float, mutation_prob = 0.03, elitism_degree = 1) \
    -> list[list[int]]:
    """
    Creates a new generation with elitism. Optimized implementation.

    Args:
    - population: a population of chromosomes.
    - mean: mean value of the fitness of a population.
    - mutation_prob: The mutation probability of an offspring.
    - elitism_degree: Makes selection of elite chromosomes more restrictive (better chromosomes).

    Returns:
    - A new population.
    """
    next_gen = []
    elite_chromosomes = len(population) // 2
    
    elite = [chr for chr in population if fitness_function(chr) < mean - elitism_degree][:elite_chromosomes]
    next_gen.extend(elite)
    non_elite = len(population) - len(elite)

    for _ in range(non_elite):
        mate1 = select_mate(population)
        mate2 = select_mate(population)
        offspring = crossover(mate1, mate2)
        offspring = mutate(offspring, mutation_prob)
        next_gen += [offspring]
    return next_gen

def evaluate(population : list[list[int]]) -> int:
    """Is the fitness goal reached?"""
    mean = sum(fitness_function(chr) for chr in population) / len(population)
    best = min(fitness_function(chr) for chr in population)
    print(best)
    print(mean)
    return best, mean

def genetic_algorithm(nqueens : int, fitness_goal=0, population_size=100) -> None:
    """The genetic algorithm"""
    generations, fits, means = [0], [], []
    generation = 0
    population = [[random.randint(1, nqueens) for _ in range(nqueens)] for _ in range(population_size)] 
    best_fit, mean = evaluate(population) 
    fits.append(best_fit)
    means.append(mean)

    while best_fit != fitness_goal:
        population = create_generation(population) # or create_generation()
        generation += 1
        best_fit, mean = evaluate(population)
        fits.append(best_fit)
        means.append(mean)
        generations.append(generation)
    plot(generations, fits, means)

def plot(generations: list[int], fits: list[int], means: list[int]) -> None:
    plt.style.use('seaborn-bright')
    fig, ax = plt.subplots()
    
    # Plot best individual
    ax.scatter(generations, fits, edgecolor='black', linewidth=1, alpha=0.75, color='springgreen')
    ax.fill_between(generations, fits, color='lightgrey', alpha=0.1)
    ax.plot(generations, fits, linestyle='--', color='slategrey', label='best individual')
    ax.set_title(f'Best Individual Evolution (Board size:{sys.argv[1]})')
    ax.set_xlabel('Generation')

    # Plot mean
    ax.scatter(generations, means, edgecolor='black', linewidth=1, alpha=0.75, color='orange')
    ax.plot(generations, means, linestyle='--', color='darkorange', label='mean')
    ax.legend()

    plt.yticks(list(range(0, int(max(means)) + 1)))
    total_gens = len(generations)
    plt.xticks(list(range(0, len(generations) + 1,  pow(10, len(str(total_gens)) - 1))))
    ax.set_ylabel('Fitness')
    plt.show()

if __name__ == "__main__":
    nqueens = int(sys.argv[1])
    genetic_algorithm(nqueens)
