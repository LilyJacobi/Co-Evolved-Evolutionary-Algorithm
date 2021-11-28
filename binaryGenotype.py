import random
import math

class binaryGenotype():
	def __init__(self):
		self.fitness = 0
		self.objectives = None
		self.gene = None
		self.numRepairs = 0
		self.fitsFromCompetition = []
		self.rawFitness = 0

	def randomInitialization(self, length):
		#for each index in given length random either 1 or 0 to populate list.
		self.gene = [random.randint(0,1) for i in range(length)]
		return self.gene
	
	def blendTwoValues(self, value1, value2, minValue, maxValue, a):
		distance = abs(value1 - value2)
		lowerBound = min(value1, value2) - a*distance
		upperBound = max(value1, value2) + a*distance
		blendedValue = random.uniform(lowerBound, upperBound)
		if(blendedValue > maxValue):
			blendedValue = maxValue
		elif(blendedValue < minValue):
			blendedValue = minValue
		return blendedValue
	def recombine(self, mate, method, **kwargs):
		child = binaryGenotype()
		childGene = []
		# TODO: Recombine genes of self with mate and assign to child's gene member variable
		assert method.casefold() in {'uniform', '1-point crossover', 'multi-dimensional', 'blx'}
		if method.casefold() == 'uniform':
			for i in range(len(self.gene)):
				if(random.randint(0,1) == 0):
					childGene.append(self.gene[i])
				else:
					childGene.append(mate.gene[i])
		elif method.casefold() == '1-point crossover':
			crossoverPoint = random.randrange(1, len(self.gene))
			for geneticBit in self.gene[:crossoverPoint]:
				childGene.append(geneticBit)
			for geneticBit in mate.gene[crossoverPoint:]:
				childGene.append(geneticBit)
		elif method.casefold() == 'multi-dimensional':
			# this is a red deliverable (i.e., bonus for anyone)

			height, width = kwargs['height'], kwargs['width']
			# transform the linear gene of both parents to a 2-dimensional representation.
			# Recombine 2D parent genes into 2D child gene using the method of your choice.
			# Convert child gene back down to 1-dimension.
			pass
		elif method.casefold() == 'blx':
			for i in range(len(self.gene)):
				#because python inheritance is weird, and I made the blend stuff a second function to make it a little easier on the eyes
				#I have to call binaryGenotype.blendTwoValues instead of just blendTwoValues
				#also I used it to determing the childs parameter since I thought the algorithm was nice
				childGene.append(round(binaryGenotype.blendTwoValues(self, self.gene[i], kwargs['minValue'], kwargs['maxValue'], mate.gene[i], kwargs['a'])))

		child.gene = childGene
		return child

	def mutate(self, **kwargs):
		copy = binaryGenotype()
		copy.gene = self.gene.copy()
		method = ''
		if 'method' in kwargs:
			method = kwargs['method']
		else:
			method = 'bitflip'
		#pick a random bit to flip
		bitToFlip = random.randrange(len(self.gene))
		copy.gene[bitToFlip] = 0 if copy.gene[bitToFlip]  == 1 else 1
		return copy

	@classmethod
	def initialization(cls, mu, *args, **kwargs):
		population = [cls() for _ in range(mu)]
		for i in range(len(population)):
			population[i].randomInitialization(*args, **kwargs)
		return population