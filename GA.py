from Population import Population
from NKModel import NKModel
from Individual import Individual
import numpy as np
import copy

class GeneticAlgorithm:
	def __init__(self, N, K, population_size, mutation_rate):
		self.population = Population(population_size, N)
		self.nk_model = NKModel(N, K)
		self.mutation_rate = mutation_rate
		self.evaluate()

	def do_one_generation(self):
		parent1_index = np.random.randint(len(self.population.array))
		parent2_index = np.random.randint(len(self.population.array))
		while parent1_index == parent2_index:
			parent2_index = np.random.randint(len(self.population.array))
		
		parent1 = self.population.array[parent1_index]
		parent2 = self.population.array[parent2_index]
        # 交叉
		child1, child2 = self.crossover(parent1, parent2)
		# 突然変異
		child1.mutation(self.mutation_rate)
		child2.mutation(self.mutation_rate)

		family = np.array([parent1, parent2, child1, child2])
		elite_individual, random_individual = self.select_individuals(family)

		self.population.array[parent1_index] = copy.deepcopy(elite_individual)
		self.population.array[parent2_index] = copy.deepcopy(random_individual)
		self.evaluate()

	def crossover(self, parent1, parent2):
		point = np.random.randint(1, self.population.individual_size)
		child1 = Individual(self.population.individual_size)
		child2 = Individual(self.population.individual_size)
		child1.gene = parent1.gene[0:point] + parent2.gene[point:self.population.individual_size]
		child2.gene = parent2.gene[0:point] + parent1.gene[point:self.population.individual_size]
		return np.array([child1, child2])
	
	def calc_evaluation(self, population):
		for individual in population.array:
			individual.fitness = self.nk_model.calc_eval(individual.gene)
		return population

	def evaluate(self):
		self.population = self.calc_evaluation(self.population)

	def sort_fitness(self, population):
		population = self.calc_evaluation(population)
		sorted_population = Population(len(population.array), population.individual_size)
		sorted_population.array = sorted(population.array, key=lambda x: x.fitness)[::-1] #降順に並べ替え
		return sorted_population

	def select_individuals(self, family):
		family_population = Population(4, len(self.population.array[0].gene))
		family_population.array = family
		sorted_family = self.sort_fitness(family_population)
		elite_gene = sorted_family.array[0]
		random_index = np.random.randint(1, len(sorted_family.array))
		random_gene = sorted_family.array[random_index]
		return elite_gene, random_gene

	def print_pop(self):
		self.population.print_array()


if __name__ == '__main__':
	N = 5
	K = 0
	population_size = 10
	mutation_rate = 0.01

	ga = GeneticAlgorithm(N, K, population_size, mutation_rate)
	print("===before===")
	ga.print_pop()
	for i in range(50):
		ga.do_one_generation()
	print("===after===")
	ga.print_pop()