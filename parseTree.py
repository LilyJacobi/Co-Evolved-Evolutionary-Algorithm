import random
import re
from fitness import manhattan_distance
class parseTree():
    def __init__(self, depthMax, operatorPrimitives, sensorPrimitives, constantRange = [-10, 10], **kwargs):
        self.depthMax = depthMax
        self.operatorPrimitives = operatorPrimitives
        self.sensorPrimitives = sensorPrimitives
        self.constantRange = constantRange
        self.root = None
        self.nodesAtDepth = [[] for i in range(depthMax+1)]
        
    def addNodesUntilDepth(self, node, currentDepth, mode, maxDepthToFill):
        if(currentDepth < maxDepthToFill):
            if(node == None or (mode == 'growMutate' and currentDepth < maxDepthToFill)):
                if(mode != 'growMutate' or node == None):
                    node = parseNode()
                if('grow' in mode):
                    if(currentDepth == 0):
                        listToChooseFrom = self.operatorPrimitives
                    else: 
                        listToChooseFrom = random.choice([self.operatorPrimitives, self.sensorPrimitives])
                elif(mode == 'full'):
                    listToChooseFrom = self.operatorPrimitives
                node.assignRandomValueFromList(listToChooseFrom, self.constantRange)
                if(node.data in self.sensorPrimitives or bool(re.search(r'[0-9].+', node.data))):
                    node.left = None
                    node.right = None
                node.depth = currentDepth
                self.nodesAtDepth[currentDepth].append(node)
            if(node.data in self.operatorPrimitives):
                node.left = self.addNodesUntilDepth(node.left, currentDepth+1, mode, maxDepthToFill)
                node.right = self.addNodesUntilDepth(node.right, currentDepth+1, mode, maxDepthToFill)
        elif(currentDepth == self.depthMax):
            node = parseNode()
            node.assignRandomValueFromList(self.sensorPrimitives, self.constantRange)
            node.depth = currentDepth
            self.nodesAtDepth[currentDepth].append(node)
        elif(currentDepth == maxDepthToFill):
            node = parseNode()
            node.assignRandomValueFromList(self.operatorPrimitives, self.constantRange)
            node.depth = currentDepth
            self.nodesAtDepth[currentDepth].append(node)
            
        return node

    def full(self, maxDepthToFill = None):
        if(maxDepthToFill == None):
            maxDepthToFill = self.depthMax
        self.root = self.addNodesUntilDepth(None, 0, 'full', maxDepthToFill)

    def grow(self, nodeFromWhichToGrow = None, maxDepthToGrow = None, mode = 'grow'):
        currentDepth = 0
        if(maxDepthToGrow == None):
            maxDepthToGrow= self.depthMax
        if(nodeFromWhichToGrow != None):
            currentDepth = nodeFromWhichToGrow.depth
            self.addNodesUntilDepth(nodeFromWhichToGrow, currentDepth, mode,maxDepthToGrow)
        else:   
            self.root = self.addNodesUntilDepth(nodeFromWhichToGrow, currentDepth, 'grow', maxDepthToGrow)
    def findNearestGhost(self, state, player):
        playerLocation = state['players'][player]
        minDistance = float('inf')
        for i in range(len(state['players'])-1):
            if(i != player):
                distToCurrentGhost = manhattan_distance(playerLocation, state['players'][str(i)])
                if(distToCurrentGhost < minDistance):
                    minDistance = distToCurrentGhost
        return minDistance
    #This is for the red delivarables, gets the dist from current ghost to pacman
    def findPacDist(self, state, player):
        pacManLocation = state['players']['m']
        minDistance = float('inf')
        distToPacFromCurrentGhost = manhattan_distance(pacManLocation, state['players'][player])
        return minDistance
    def findNearestPill(self, state):
        pacManLocation = state['players']['m']
        minDistance = min([manhattan_distance(pacManLocation, pill) for pill in state['pills']])
        return minDistance
    def findNearestFruit(self, state):
        pacManLocation = state['players']['m']
        if(state['fruit'] != None):
            minDistance = manhattan_distance(pacManLocation, state['fruit'])
        else:
            #I think setting min distance to 1 should like probably cause the least damage and weirdness, since it doesn't modify the value too much in any case but RAND, or adding to a devimal?????
            #I considered setting to none and handling in the evaluate function but decided against it becaue if both leafs were none then what would I assign the value too, Idk it seemed more trouble than it was worth
            minDistance = 1
        return minDistance
    def findNumberOfAdjacentWalls(self, state, player):
        pacManLocation = state['players'][player]
        walls = state['walls']
        adjWalls = 0
        for x_shift, y_shift in ((0,-1), (1,0), (0,1), (-1,0)):
            x = pacManLocation[0] + x_shift
            y = pacManLocation[1] + y_shift
            if(not 0<=x<len(walls) or not 0<=y<len(walls[x]) or walls[x][y]==1):
                adjWalls += 1
        return adjWalls
    def evaluateTree(self, state, node, player = "m"):
        if(node.data == '+'):
            return self.evaluateTree(state, node.left) + self.evaluateTree(state, node.right, player)
        elif(node.data == '-'):
            return self.evaluateTree(state, node.left) - self.evaluateTree(state, node.right, player)
        elif(node.data == '*'):
            return self.evaluateTree(state, node.left) * self.evaluateTree(state, node.right, player)
        elif(node.data == '/'):
            try:
                return self.evaluateTree(state, node.left) / self.evaluateTree(state, node.right, player)
            except ZeroDivisionError:
                return 0
        elif(node.data == 'RAND'):
            return random.uniform(self.evaluateTree(state, node.left, player), self.evaluateTree(state, node.right, player))
        elif(node.data == 'G'):
            return self.findNearestGhost(state, player)
        elif(node.data == 'P'):
            return self.findNearestPill(state)
        elif(node.data == 'W'):
            return self.findNumberOfAdjacentWalls(state, player)
        elif(node.data == 'F'):
            return self.findNearestFruit(state)
        elif(bool(re.search(r'[0-9].+', node.data))):
            return float(node.data)
        #This is for the red delivarables, gets the dist from current ghost to pacman
        elif(node.data == 'PAC'):
            return self.findNearestPac(state, player)
    def countChildren(self, node):
        if(node == None):
            return 0
        return(self.countChildren(node.left) + self.countChildren(node.right) + 1)
    def updateChildrenCount(self, node):
        if(node == None):
            return 0 
        node.childrenCount = self.countChildren(node) - 1
        self.updateChildrenCount(node.left)
        self.updateChildrenCount(node.right)
    
    def childrenCountHandler(self, node):
        if(node == None):
            return 0
        return node.childrenCount +1
    
    def randomNodeHelper(self, node, index):
        if(node == None):
            return None
        elif(index == self.childrenCountHandler(node.left)):
            return node
        elif(index < self.childrenCountHandler(node.left)):
            return self.randomNodeHelper(node.left, index)
        else:
            return self.randomNodeHelper(node.right, index - self.childrenCountHandler(node.left) - 1)
        
    def randomNode(self):
        self.updateChildrenCount(self.root)
        rangeWithoutRootAsValidOption = list(range(self.root.childrenCount))
        rangeWithoutRootAsValidOption.remove(self.root.left.childrenCount+1)
        index = random.choice(rangeWithoutRootAsValidOption)
        return self.randomNodeHelper(self.root, index)

    def fixDepth(self, node, depth):
        if(node is None):
            return
        node.depth = depth
        if(depth == self.depthMax):
            if(node.data not in self.sensorPrimitives or  bool(re.search(r'[0-9].+', node.data))):
                node.assignRandomValueFromList(self.sensorPrimitives, self.constantRange)
                node.left = None
                node.right = None
            return
        self.fixDepth(node.left, depth+1)
        self.fixDepth(node.right, depth+1)

    def buildString(self, node, currentString):
        if(node == None):
            return currentString
        currentString = currentString + str(node) + '\n'
        currentString = self.buildString(node.left, currentString)
        currentString = self.buildString(node.right, currentString)
        return currentString
    def __str__(self):
        treeString = self.buildString(self.root, '')
        return treeString
    
class parseNode():
    def __init__(self):
        self.data = None
        self.depth = None
        self.right = None
        self.left = None
        self.childrenCount = None
    def __str__(self):
        return '|' * self.depth + self.data
    #this will be used to assign from operator primitives or sensor primitives randomly
    def assignRandomValueFromList(self, valueList, constantRange):
        randomIdx = random.randrange(len(valueList))
        if(valueList[randomIdx] == '#.#'):
            self.data = str(random.uniform(constantRange[0], constantRange[1]))
        else:
            self.data = valueList[randomIdx]
