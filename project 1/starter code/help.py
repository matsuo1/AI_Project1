###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================
from tkinter import N
from numpy import block
from state import State
import itertools
import copy
from queue import PriorityQueue

class Plan:

    def __init__(self, initial_state, goal_state):
        """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
        self.initial_state = initial_state
        self.goal_state = goal_state

    def pickup(self, block1):
        """
        Operator to pickup the block from the table
        :param block1: block1 to pick up from the table
        :type block1: Object of block.Block
        :return: None
        """
        if block1.type == 2:
            block1.air = True
            block1.on = None

        if block1.clear and not block1.air:
            block1.unclear()
            block1.air = True
            block1.on = None

    def putdown(self, block1):
        """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block1.air:
            block1.on = table
            block1.clear = True
            block1.air = False
            if block1.type == 2: block1.clear = False

    def stack(self, block1, block2):
        """
        Operator to stack block1 onto block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """
        if block1.air and block2.clear: #block 1 is in air and 2 does not have anything on top
            block1.air = False #We placed in on block2, no longer in air
            block1.on = block2 #place it on block2
            block2.unclear()
            if block1.type != 2: 
                block1.clear = True

    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        # if block1 is clear safe to unstack
        if block1.clear and block1.type == 2:

            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True
    

    def findValidMoves(self, currentState):
        # block = currentState[2]
        # statecopy = copy.deepcopy(currentState)
        # print([x.id for x in currentState].index(block.id))
  

         neighborList  = []

         for block in currentState[1::]: 
            #print(f"{block.id}:{block.clear}")       
            if (block.clear or block.type == 2) and block.on.id == 'table':
                tempState = copy.deepcopy(currentState)
                blockToPickUp = tempState[[x.id for x in currentState].index(block.id)]
    
                self.pickup(blockToPickUp)
                #might need to remember where we picked it from because we don't want to backtrack
                 
                looper = iter(tempState[1::]) #we don't want the table here because we don't want to put it back to where it was
                currBlock = next(looper)
                #print("Current Block ", currBlock)
                while True:
                    try:
                        if currBlock.clear:
                            #print("We need to stack on top of this ", currBlock)
                            neighborState = copy.deepcopy(tempState)
                            blocktoStack = neighborState[[x.id for x in tempState].index(blockToPickUp.id)]
                            ontoBlock = neighborState[[x.id for x in tempState].index(currBlock.id)]
                            #blocktoUnstackOnto = neighborState[[x.id for x in currentState].index(currBlock.id)]

                            self.stack(blocktoStack, ontoBlock)
                            action = f"Stack({blockToPickUp}) on {ontoBlock}"
                            neighborList.append([action, neighborState])
                            #State.display(neighborState, message=action)
                            
                        currBlock = next(looper)
                    except StopIteration:
                        break
                

            elif (block.clear or block.type ==2) and not block.on.id == 'table':
                tempState = copy.deepcopy(currentState)
                
                blockToUnstack = tempState[[x.id for x in currentState].index(block.id)]
                blockonTopOf = blockToUnstack.on.id #remember where it was unstacked form
                self.unstack(blockToUnstack, blockToUnstack.on)
                
                looper = iter(tempState)
                currBlock = next(looper)
                #print("Current Block ", currBlock.clear)

                #find a place to stack it onto
                while True:
                    try:
                        if currBlock.clear and not currBlock.id == blockonTopOf:
                            #print(f"We need to stack {blockToUnstack} on top of {currBlock}")

                            neighborState = copy.deepcopy(tempState)
                            blocktoStack = neighborState[[x.id for x in tempState].index(blockToUnstack.id)]
                            #print("Block to Stack: ", blocktoStack)
                            ontoBlock = neighborState[[x.id for x in tempState].index(currBlock.id)]
                            #print("Block to Stack onto: ", ontoBlock)
                            #blocktoUnstackOnto = neighborState[[x.id for x in currentState].index(currBlock.id)]
                            if not ontoBlock.id == 'table':
                                self.stack(blocktoStack, ontoBlock)
                                action = f"Stack({blockToUnstack}) on {ontoBlock}"
                                #State.display(neighborState, message=action)
                                neighborList.append([action, neighborState])
                            else:
                                self.putdown(blocktoStack)
                                #print(f"{neighborState[2]} is on top of {neighborState[2].on}")
                                action = f"Putdown({blockToUnstack}) on the table"
                                
                                #State.display(neighborState, message=action)
                                neighborList.append([action, neighborState])

                        currBlock = next(looper)
                    except StopIteration:
                        break
               
            # elif block.type == 2 and block.on.id == 'table':
            #     tempState = copy.deepcopy(currentState)
            #     blockToPickUp= tempState[[x.id for x in currentState].index(block.id)]
            #     action = f"Pickup({blockToPickUp})"
            #     self.pickup(blockToPickUp)
            #     State.display(tempState, message = action)
         

         return neighborList
         #print([block.air for block in neighborList[2]])
    

                 
        
    def h1(currentState, goalState): #in this approach we will assign a block +1 if it is on top of the correct block, -1 otherwise (local heuristic)
        score = 0
        for index in range(1, len(goalState.blocks)):
            if currentState.blocks[index].on == goalState.blocks[index].on:
                score += 1
        return score

    def h2(self, currentState, goalState):  #a global heuristic (number of correct blocks underneath the current one; if the support structure underneath is not correct, assign it -1 *(number of incorrect blocks)
        score = 0
        for i in range(1, len(goalState)):
            #print(goalState[i])
            goalStructure = []
            currentStructure = []

            onTopOf = goalState[i].on
            onTopOf2 = currentState[i].on
            #print(f"on top of {onTopOf}")
            goalStructure.append(onTopOf)
            currentStructure.append(onTopOf2)

            while not onTopOf.id == 'table':
                onTopOf = onTopOf.on
                #print(onTopOf)
                goalStructure.append(onTopOf)

            while not onTopOf2.id == 'table':
                onTopOf2 = onTopOf2.on
                #print(onTopOf)
                currentStructure.append(onTopOf2)
            
            print(f"Goal Structure for {goalState[i].id} {goalStructure}")
            print()
            print(f"Current Structure for {currentState[i].id} {currentStructure}")
            print()
          
            if not currentStructure[0].id == 'table':
                if [block.id for block in currentStructure] == [block.id for block in goalStructure]:
                    score += len(currentStructure) -1
                else:
                    score -= 1 * (len(currentStructure) - 1)
        
        #print('----------------------------------------------------------------------')        
        return(score)
            





    # ***=========================================
    # After you implement all the operators
    # The next step is to implement the actual plan.
    # Please fill in the sample plan to output the appropriate steps to reach the goal
    # ***=========================================
    def hasVisited(self,currState, visitedStates):
        hasVisited = True
        for state in visitedStates:
            i = 1 #start from 1 because we don't care about the table
            for block in state[1::]:
                if currState[i].on.id != block.on.id:
                    hasVisited = False
                    break
                else:
                    hasVisited = True
                i += 1
            if hasVisited: return True
        
        return False

    def plan(self):
        count =0
        #greedy best first search
        frontier = PriorityQueue()
        currState = ["Initial State",initial_state.blocks]
        goalState = goal_state.blocks
        visitedStates = []
        frontier.put((-1 *self.h2(currState[1], goalState), currState))
        visitedStates.append(currState[1])
        targetHeuristic = -1 * self.h2(goalState, goalState)
        while not frontier.empty() and (-1*self.h2(currState[1], goalState)) !=  targetHeuristic:
            #print("TEST!!")
            #State.display(currState[1], message = currState[0])
            neighbors = self.findValidMoves(currState[1]) 
            #i = 0
            for neighbor in neighbors:
                #print(f"NEIGHBOR{i}")
                #State.display(neighbor[1], message = neighbor[0])
                if not self.hasVisited(neighbor[1], visitedStates):
                    frontier.put((-1*self.h2(neighbor[1], goalState), neighbor))
                    visitedStates.append(neighbor[1])
                #i += 1
            
            
           
            currState = frontier.get()[1]
            # a = self.h2(currState[1], goalState)
            # b = self.h2(goalState, goalState)
            #print("Empty ", frontier.empty())
            #print("Current h val", self.h2(currState[1], goalState))
            State.display(currState[1], message = currState[0])
            count +=1
        #return visitedNodes
        

        print(count)

if __name__ == "__main__":

    # get the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")
    #print("Initial state blocks ",initial_state_blocks)

    #display initial state
    State.display(initial_state_blocks, message="Initial State")

    # get the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    #display goal state
    State.display(goal_state_blocks, message="Goal State")


    p = Plan(initial_state_blocks, goal_state_blocks)
    p.plan()





