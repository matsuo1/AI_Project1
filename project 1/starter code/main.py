###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================
#testing
from state import State
import itertools

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
   
    def newneighbors(self,currentstate):
        #Make 5 lists: putdown, unstack, stack, pickup, move
        putdown = []
        unstack =[]
        stack = []
        pickup = []
        move =[]
        #Make a copy of the current state
        curr = currentstate.deepcopy()

        #Make a table with the initial_state

        #blocks in the air list
        #loop through each block in the state and check whether the block is in the air
        #Add those blocks into the list
        air =[]
        for items in curr:
            if items.air == True:
                air.append(items)

        #blocks on the table and clear list
        #loop through each block in the state and check the appropriate conditions for the blocks to be on table and clear
        #Add those blocks into the list
        ontable_clear = []
        for items in curr:
            if items.on =='table' and items.clear == True:
                ontable_clear.append(items)
            

        #blocks that are clear and not on the table
        #loop through each block in the state and check the appropriate conditions for
        #the blocks to be not on table and clear
        #Add those blocks into the list
        nottable_clear = []
        for items in curr:
            if items.on !='table' and items.clear == True:
                nottable_clear.append(items)

        #if block in air list have element(s) then only do putdown and stack
        if air:
            #putdown
            #copy the state
            tryputdown = curr.deepcopy()#Maybe not curr
            for items in tryputdown:#get the equivalent block from the copied state
                if items == air[0]:
                    self.putdown(items)#apply the operator
            print(air)
            putdown.append(tryputdown) #add those into putdown list (made in the previous step)

            #stack
            clear = ontable_clear + nottable_clear
                #it is a combination of (blocks_air & blocks_clear) (itertool recommendation)
                #loop through all combinations:
            stackblockproduct = itertools.product(air[0],clear)
            print(stackblockproduct)
            for block,block1 in stackblockproduct:
                trystack = curr.deepcopy()
                    #make a copy 
                # Figure out the Ids for block and block 1 using find
                block_id = State.find(trystack, block)
                block1_id = State.find(trystack, block1)
                self.stack(block_id,block1_id) 
                stack.append(trystack, f"stack{block_id, block1_id}")  
                    #get the equivalent block from the copied state
                    #apply operator for the two blocks in the operator
                    #add those into stack list (made in the previous step)
        else:
    #if the block is not in the air - options: pickup, unstack, move (the steps for these should be somewhat the same as putdown and stack)
        #pickup options
            for items in ontable_clear:
                trypick = curr.copy()
                for stuff in trypick:
                    if items == stuff:
                        self.pickup(stuff)
                        break
                pickup.append(trypick)

            #apply pick operator on all blocks that are clear and are on the table
            #Add those into the pick list (made in the previous step)
        #unstack
            for items in nottable_clear:
                tryunstack = curr.copy()
                
            #apply unstack operator to all blocks that are clear and are not on table
            #Add those into the unstack list (made in the previous step)
        #move

            #apply move operator to all bloakcs that are clear and not on the table to any block that is clear
            #it is the combination of blocks that are clear and not on table with blocks are simply clear (itertools recommendation)

    #return all five lists
        return pickup,putdown,stack,unstack,move

    def clearBlocks(self,state):
        openMoves = []
        for i in state:
            if i.clear == True:
                openMoves.append(i)
                print("we can move this: ", i)
        return openMoves

    def heuristic(self,moves,goal_state_blocks,initial_state_blocks): #pick-up function 
        totalnow = 0
        target = 0
        blocks = [] # can anyone think of a better/ more efficent way to get the highest #
        for i in range(len(initial_state_blocks)):
            score =0 
            if i == 0:
                continue
            target += 2
            if initial_state_blocks[i].clear == goal_state_blocks[i].clear:
                score += 1
                #print("CLEAR",initial_state_blocks[i],initial_state_blocks[i].clear)
            #print("what it should be: ", goal_state_blocks[i],goal_state_blocks[i].clear)
            if initial_state_blocks[i].on == goal_state_blocks[i].on:
                score += 1
                #print("ON",initial_state_blocks[i],initial_state_blocks[i].on)
            #print("what it should be: ", goal_state_blocks[i],goal_state_blocks[i].on)
            totalnow += score
            if initial_state_blocks[i] in moves:
                blocks.append((score,initial_state_blocks[i].id,initial_state_blocks[i]))
            #print("the score for ", initial_state_blocks[i], "is ", score)
            #print("blocks list consists of ", blocks)
            #print(initial_state_blocks[i], "is clear?", initial_state_blocks[i].clear, "and is on?", initial_state_blocks[i].on)
        #blocks.sort()
        print(totalnow, "vs", target)
        # bestMove = blocks.pop(0)
        # print("thebest move,", bestMove)
        return blocks
    
    def putdown_priority(self,block1,current_state,goal_state_blocks): 
        current_state[0].clear = True
        goal = goal_state_blocks
        match = block1
        for i in range(len(goal)):
            if block1 == goal[i]: #If the loop finds the same block as the one in the air
                match = goal[i]
                break
        for j in range(len(current_state)):
            if match.on == current_state[j]:
                print("helpme",current_state[j])
                if current_state[j] == "table":
                    self.putdown(block1)
                elif current_state[j].clear == True:
                    self.stack(block1,current_state[j])
    

    def aStar(self,initial_state,goal):
        frontier= [] #priority queue
        currState = initial_state
        #path = [] # dont know yet 
        #path.append(start) # dont know yet  
        #Avistited = [] # temp visited list fro testing  # dont know yet  
        moves = self.clearBlocks(initial_state)
        print("SOS",moves)
        frontier = self.heuristic(moves,goal,initial_state_blocks)  #what block, from the list of the clear blocks should we move? 
        print ("frontieraf ", frontier)
         # ***=========================================
        #Avistited.append(start) 
        while(frontier):
            frontier = self.heuristic(moves,goal,initial_state_blocks)
            frontier.sort()
            print("yuh", frontier)
            bestBlock = frontier.pop(0) # node with the lowest ASTAR score in frontier.
            print (bestBlock[2])
           # path.append(node[2])
            #if node[2] == end:
             #   return path #retrun path       
            nextneighbors = self.neighbors(bestBlock[2],currState) 
            print("neighbors", nextneighbors)  
            #moveTo = self.putdown_priority(aScore1,currState,goal) #need
            #print("move to", moveTo[1])
            #self.stack(bestBlock[1], moveTo[1])
            #for neighbor in nextneighbors:
             #   if neighbor not in Avistited:
              #      pathCost = node[1]+1
                     #aScore = heuristic(enpathCost,neighbor)
                #    frontier.append((aScore,pathCost,neighbor))
                 #   Avistited.append(neighbor)
            print("This it?", frontier)
            self.putdown_priority(bestBlock[2],currState,goal)
            #break
        return 0


    def sample_plan(self):

        # get the specific block objects
        # Then, write code to understand the block i.e., if it is clear (or) on table, etc.
        # Then, write code to perform actions using the operators (pick-up, stack, unstack).

        # Below I manually hardcoded the plan for the current initial and goal state
        # You must automate this code such that it would produce a plan for any initial and goal states.

        block_c = State.find(self.initial_state, "C")
        block_d = State.find(self.initial_state, "D")
        #block_e = State.find(self.initial_state, "E")
  
        self.aStar(self.initial_state, goal_state_blocks)

        #moves = self.clearBlocks(self.initial_state)
        #print("the open blocks that we can move are: ", moves)
        #self.heuristic(moves,goal_state_blocks)

        
    
      
        #Unstack the block
        #self.unstack(block_d, block_c)

        #print the state
        action = f"unstack{block_d, block_c}"
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
    






