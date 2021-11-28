from baseEvolution import baseEvolutionPopulation
from random import random
class geneticProgrammingPopulation(baseEvolutionPopulation):
	def generate_children(self):
		children = list()
		
		numberOfParents = 2*self.num_children
		parents = self.parent_selection(self.population, numberOfParents, **self.parent_selection_kwargs)
		for i in range(0, numberOfParents, 2):
			if(random() < self.mutation_rate): 
				child = parents[1].mutate(**self.mutation_kwargs)
			else:
				child = parents[i].recombine(parents[i+1], **self.recombination_kwargs)
			children.append(child)
		return children