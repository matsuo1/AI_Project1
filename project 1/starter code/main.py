###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================
#testing
from state import State

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
        self.steps = 0


    #***=========================================
    # First implement all the operators
    # I implemented two operators to give you guys an example
    # Please implement the remainder of the operators
    #***=========================================

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
            self.steps += 1
            action = f"Putdown({block1}, table)"
            State.display(self.initial_state, message=action)

    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None   
        """

        # if block1 is clear safe to unstack
        if block1.clear:
            print('unstacking',block1.id, 'from', block2.id)
            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True
            self.steps += 1
            action = f"Unstack({block1}, {block2})"
            State.display(self.initial_state, message=action)
    
    def stack(self, block1, block2):
        #Operator to stack block1 onto block 2
        if block2.clear:
            print('stacking',block1.id, 'onto', block2.id)
            block1.clear = True
            block1.air = False
            block1.on = block2

            block2.clear = False 
            self.steps += 1
            action = f"Stack{block1} on {block2}"
            State.display(self.initial_state, message=action)

    def pickup(self,block1):
        table = State.find(self.initial_state, "table")

        if block1.on == table:
            print('Picking up: ',block1.id)
            block1.air = True
            block1.on = None
            self.steps += 1
            action = f"Pick up {block1} from {table}"
            State.display(self.initial_state, message=action)
            
    def move(self,block1):
        print('Moving...')
        self.steps += 1
        action = f"Moved {block1}"
        State.display(self.initial_state, message=action)


    # ***=========================================
    # After you implement all the operators
    # The next step is to implement the actual plan.
    # Please fill in the sample plan to output the appropriate steps to reach the goal
    # ***=========================================

    def neighbors(self, bestBlock, currState):
        possibleMoves = []
        print("GETTING THE NEIGHBORS FOR BLOCK "+ bestBlock.id)
        if repr(bestBlock.on) == 'table':
            print("picking up block " + bestBlock.id +  " from: ", bestBlock.on)
            self.pickup(bestBlock)
            print("block " + bestBlock.id + " is picked up and on: ", bestBlock.on)
        else: 
            print("unstacking block " + bestBlock.id + " from: ", bestBlock.on)
            self.unstack(bestBlock,bestBlock.on)
            print("block "  + bestBlock.id +  " is unstacked and on: ", bestBlock.on)
        for i in currState:
            if i.type == 3 or i.id == bestBlock.id:
                continue
            if i.clear:
                possibleMoves.append(i)
            print("curr state: ",i," is on ",  i.on, " and clear?: ", i.clear)
            print("possible moves: ", possibleMoves)
        return possibleMoves
   

    def clearBlocks(self,state):
        openMoves = []
        for i in state:
            if i.clear == True:
                openMoves.append(i)
                print("we can move this: ", i)
        return openMoves

    def heuristic(self,moves,goal_state_blocks): 
        blocks = [] # can anyone think of a better/ more efficent way to get the highest #
        for i in range(len(moves)):
            score =0 
            if i == 0:
                continue
            if moves[i].clear == goal_state_blocks[i].clear:
                score += 1
            if moves[i].on == goal_state_blocks[i].on:
                score += 1
            blocks.append((score,moves[i]))
            print("the score for ", moves[i], "is ", score)
            print("blocks list consists of ", blocks)
    
        blocks.sort()
        bestMove = blocks.pop(0)
        print("thebest move,", bestMove)
        return bestMove
    
    def aStar(self,initial_state,goal):
        frontier= [] #priority queue
        currState = initial_state
        #path = [] # dont know yet 
        #path.append(start) # dont know yet  
        #Avistited = [] # temp visited list fro testing  # dont know yet  
        moves = self.clearBlocks(initial_state)
        aScore1 = self.heuristic(moves,goal)  #what block, from the list of the clear blocks should we move? 
        frontier.append((aScore1))
        print ("frontier ", frontier)
         # ***=========================================
        #Avistited.append(start) 
        while(frontier):
            frontier.sort()
            bestBlock = frontier.pop() # node with the lowest ASTAR score in frontier.
            print (bestBlock[1])
           # path.append(node[2])
            #if node[2] == end:
             #   return path #retrun path       
            nextneighbors = self.neighbors(bestBlock[1],currState) 
            print("neighbors", nextneighbors)  
            moveTo = self.heuristic(nextneighbors,goal) #need
            print("move to", moveTo[1])
            self.stack(bestBlock[1], moveTo[1])
            #for neighbor in nextneighbors:
             #   if neighbor not in Avistited:
              #      pathCost = node[1]+1
                     #aScore = heuristic(enpathCost,neighbor)
                #    frontier.append((aScore,pathCost,neighbor))
                 #   Avistited.append(neighbor)
        return 0


    def sample_plan(self):

        # get the specific block objects
        # Then, write code to understand the block i.e., if it is clear (or) on table, etc.
        # Then, write code to perform actions using the operators (pick-up, stack, unstack).

        # Below I manually hardcoded the plan for the current initial and goal state
        # You must automate this code such that it would produce a plan for any initial and goal states.

        block_c = State.find(self.initial_state, "C")
        #block_d = State.find(self.initial_state, "D")
        #block_e = State.find(self.initial_state, "E")
  
        self.aStar(self.initial_state, goal_state_blocks)

        #moves = self.clearBlocks(self.initial_state)
        #print("the open blocks that we can move are: ", moves)
        #self.heuristic(moves,goal_state_blocks)

        
    
      
        #Unstack the block
        #self.unstack(block_d, block_c)

        #print the state
        #action = f"unstack{block_d, block_c}"
        #State.display(self.initial_state, message=action)

        #put the block on the table
        #self.putdown(block_d)

        #print the state
        #action = f"Putdown({block_d}, table)"
        #State.display(self.initial_state, message=action)


if __name__ == "__main__":

    # get the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")
    print(initial_state.blocks)

    #display initial state
    State.display(initial_state_blocks, message="Initial State")

    # get the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")
    

    #display goal state
    State.display(goal_state_blocks, message="Goal State")

    """
    Sample Plan
    """

    p = Plan(initial_state_blocks, goal_state_blocks)
    p.sample_plan()
    






