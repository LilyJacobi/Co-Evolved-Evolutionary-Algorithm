import random
from math import inf
# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
	parents = random.choices(population, k=n)
	return parents

def singleFight(population, k):
	contestants = random.sample(population, k=k)
	winner = max(contestants, key = lambda contestant : contestant.fitness)
	return winner

def k_tournament_with_replacement(population, n, k, **kwargs):
	winners = []
	for i in range(n):
		winners.append(singleFight(population, k))
	return winners

def modifyFitness(population):
	minFitness = min([individual.fitness for individual in population])
	minFitness *= 1.5
	modifiedFitness = [individual.fitness - minFitness for individual in population]
	return modifiedFitness

def fitness_proportionate_selection(population, n, **kwargs):
	modifiedFitness = []
	if(min([individual.fitness for individual in population]) <  0):
		modifiedFitness = modifyFitness(population)
	else:
		modifiedFitness = [individual.fitness for individual in population]
	minModifiedFitness = min(modifiedFitness)
	proportionalFitnesses = [(fitness/minModifiedFitness)*100 for fitness in modifiedFitness]
	proportionalParents = random.choices(population, weights = proportionalFitnesses, k=n)
	
	return proportionalParents


# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
	# TODO: perform truncation selection to select n individuals
	populationSorted = sorted(population, key = lambda individual : individual.fitness, reverse = True)

	return populationSorted[:n]

def k_tournament_without_replacement(population, n, **kwargs):
	# TODO: perform n k-tournaments without replacement to select n individuals
	#		Note: an individual should never be cloned from surviving twice!
	nonWinners = population.copy()
	winners = []
	for i in range(n): 
		if(kwargs['k'] > len(nonWinners)):
			k = len(nonWinners)
		else:
			k = kwargs['k']
		winner = singleFight(nonWinners, k=k)
		winners.append(winner)
		nonWinners.remove(winner)
	return winners

# Yellow deliverable parent selection function---------------------------------
def stochastic_universal_sampling(population, n, **kwargs):
	# Recall that yellow deliverables are required for students in the grad
	# section but bonus for those in the undergrad section.
	# TODO: select n individuals using stochastic universal sampling
	modifiedFitness = modifyFitness(population)
	fitnessSum = (sum(modifiedFitness))
	distanceBetweenPoints = fitnessSum / n
	start = random.randrange(int(distanceBetweenPoints))
	pointers = [start + (i*distanceBetweenPoints) for i in range(n)]
	parents = []
	for point in pointers:
		i = 0
		while abs(sum(modifiedFitness[:i+1])) < point:
			i+=1
		parents.append(population[i])
	return parents