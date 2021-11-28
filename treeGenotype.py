
# GPac primitives
# internal_nodes = {'+','-','*','/','RAND'}
# leaf_nodes = {'G','P','W','F','#.#'}
from parseTree import *
from random import randrange
from copy import deepcopy
class treeGenotype():
	def __init__(self):
		self.fitness = None
		self.rawFitness = None
		self.fitsFromCompetition = []
		self.rawFitsFromCompetition = []
		self.gene = None
		self.log = None

	def halfAndHalfInitialization(self, depth_limit, operatorPrimitives, sensorPrimitives, constantRange = [-10, 10], **kwargs):
		self.gene = parseTree(depth_limit, operatorPrimitives, sensorPrimitives, constantRange)
		halfDepth = int(depth_limit/2)
		self.gene.full(halfDepth)
		for node in self.gene.nodesAtDepth[halfDepth]:
			self.gene.grow(nodeFromWhichToGrow = node, maxDepthToGrow = depth_limit)
	def recombine(self, mate, **kwargs):
		child = self.__class__()
		
		child.gene = deepcopy(self.gene)
		insertionPoint = child.gene.randomNode()
		newSubtree = deepcopy(mate.gene.randomNode())
		insertionPoint.left = newSubtree.left
		insertionPoint.right = newSubtree.right
		insertionPoint.data = newSubtree.data
		child.gene.fixDepth(insertionPoint, insertionPoint.depth)


		return child

	def mutate(self, **kwargs):
		copy = self.__class__()
		copy.gene = deepcopy(self.gene)
		growthPoint = copy.gene.randomNode()
		copy.gene.grow(nodeFromWhichToGrow = growthPoint, mode = 'growMutate')

		return copy

	def print(self):
		return str(self.gene)
		

	@classmethod
	def initialization(cls, mu, *args, **kwargs):
		population = [cls() for _ in range(mu)]
		for i in range(len(population)):
			population[i].halfAndHalfInitialization(*args, **kwargs)

		return population