###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================
#testing
from state import State
import itertools
import copy

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
            #action = f"Putdown({block1}, table)"
            #State.display(self.initial_state, message=action)

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
            #print('unstacking',block1.id, 'from', block2.id)
            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True
            self.steps += 1
            #action = f"Unstack({block1}, {block2})"
            #State.display(self.initial_state, message=action)
    
    def stack(self, block1, block2):
        #Operator to stack block1 onto block 2
        if block2.clear:
            print('stacking',block1.id, 'onto', block2.id)
            block1.clear = True
            block1.air = False
            block1.on = block2

            block2.clear = False 
            self.steps += 1
            #action = f"Stack{block1} on {block2}"
            #State.display(self.initial_state, message=action)

    def pickup(self,block1):
        table = State.find(self.initial_state, "table")

        if block1.on == table:
            print('Picking up: ',block1.id)
            block1.clear = False
            block1.air = True
            block1.on = None
            self.steps += 1
           # action = f"Pick up {block1} from {table}"
            #State.display(self.initial_state, message=action)
            
    def move(self,curr):
        print("******************")
        print('Moving...')
        print("******************")
        self.steps += 1
        #action = f"Moved {block1}"
        #State.display(curr, message=action)


    # ***=========================================
    # After you implement all the operators
    # The next step is to implement the actual plan.
    # Please fill in the sample plan to output the appropriate steps to reach the goal
    # ***=========================================

  
   
    def neighbors(self,currentstate):
        #Make 5 lists: putdown, unstack, stack, pickup, move
        putdown = []
        unstack =[]
        stack = []
        pickup = []
        move =[]
        #Make a copy of the current state
        curr = copy.deepcopy(currentstate)

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
            if repr(items.on) =='table' and items.clear == True:
                ontable_clear.append(items)
            

        #blocks that are clear and not on the table
        #loop through each block in the state and check the appropriate conditions for
        #the blocks to be not on table and clear
        #Add those blocks into the list
        nottable_clear = []
        for items in curr:
            if repr(items.on) !='table' and items.clear == True and repr(items) != "table":
                nottable_clear.append(items)

        #if block in air list have element(s) then only do putdown and stack
        if air:
            #putdown
            #copy the state
            tryputdown = copy.deepcopy(curr)#Maybe not curr
            for items in air:#get the equivalent block from the copied state
                block_id = State.find(tryputdown, items.id)
                self.putdown(block_id)#apply the operator
                putdown.append((tryputdown, f"putdown {block_id}")) #add those into putdown list (made in the previous step)

            #stack
            clear = ontable_clear + nottable_clear
                #it is a combination of (blocks_air & blocks_clear) (itertool recommendation)
                #loop through all combinations:
            print("please",clear)
            stackblockproduct = itertools.product(air,clear)
            for block,block1 in stackblockproduct:
                if block.id == block1.id:
                    print("cannot do", block1, block)
                    continue
                print("---------------------")
                print(block1.type)
                if block1.type == 2:
                    print("SKIP A TRIANGLE")
                    continue
                trystack = copy.deepcopy(curr)
                    #make a copy 
                # Figure out the Ids for block and block 1 using find
                block_id = State.find(trystack, block.id)
                block1_id = State.find(trystack, block1.id)
                self.stack(block_id,block1_id) 
                stack.append((trystack, f"stack {block_id, block1_id}"))  
                    #get the equivalent block from the copied state
                    #apply operator for the two blocks in the operator
                    #add those into stack list (made in the previous step)
        else:
    #if the block is not in the air - options: pickup, unstack, move (the steps for these should be somewhat the same as putdown and stack)
        #pickup options       
            for items in ontable_clear:
                trypick = copy.deepcopy(curr)
                block_id = State.find(trypick, items.id)
                self.pickup(block_id)
                pickup.append((trypick, f"pickup {block_id}"))

            #apply pick operator on all blocks that are clear and are on the table
            #Add those into the pick list (made in the previous step)
        #unstack
            for items in nottable_clear:
                tryunstack = copy.deepcopy(curr)
                block_id = State.find(tryunstack, items.id)
                block1_id = State.find(tryunstack, items.on.id)
                self.unstack(block_id,block1_id)
                unstack.append((tryunstack, f"unstack{block_id,block1_id}"))
            #apply unstack operator to all blocks that are clear and are not on table
            #Add those into the unstack list (made in the previous step)
        #move

            #apply move operator to all bloakcs that are clear and not on the table to any block that is clear
            #it is the combination of blocks that are clear and not on table with blocks are simply clear (itertools recommendation)

    #return all five lists
        print("Hello ", stack+pickup+unstack+putdown+move)
        return stack+pickup+unstack+putdown+move

    def reachedGoal(self,curr,goal):
        for i in range(len(curr)):
            if curr[i].on == goal[i].on and curr[i].clear == goal[i].clear and curr[i].air == goal[i].air:
                continue
            else:
                return False
        return True 
    
    def inVisited(self,curr,visited):
        for i in range(len(visited)):
            #print("FIRST FOR LOOP: ", visited[i])
            for j in range(len(visited[i])):
                #print("SEC FOR LOOP: ",curr[j],visited[i][j])
                #print("Test for yooo:", curr[j].on,visited[i][j].on)
                if repr(curr[j].on) != repr(visited[i][j].on) or repr(curr[j].clear) != repr(visited[i][j].clear) or repr(curr[j].air) != repr(visited[i][j].air):
                    break
                if j == (len(visited[i])-1):
                    return True 
        return False
            
                


    def gbfs(self,initial_state,goal):
        Priority_Queue = []
        score = []  
        pathTaken = []
        pathTaken.append(initial_state)
        startingFrom = self.lars_bennet_heuristic(initial_state, goal)
        Priority_Queue.append((startingFrom,initial_state, "Initial_State"))
        print("FOLLOWING LARS: ", Priority_Queue)
        gbfs_visited = [initial_state]
        while Priority_Queue:
            Priority_Queue.sort()
            print("Priority QUEUE SORTED: ", Priority_Queue)
            (heuristic,curr, move) = Priority_Queue.pop(-1)
            Priority_Queue = []
            State.display(curr, message = move)  
            #State.display(curr, message= "Goal State Reached")
            pathTaken.append((curr,move))
            print("After pop:",curr,heuristic)
            if(self.inVisited(curr,gbfs_visited)==True):
                print(curr,"STAY WITH ME")
            if(self.inVisited(curr,gbfs_visited)==False):
                #if heuristic == self.lars_bennet_heuristic(goal, goal):
                if self.reachedGoal(curr,goal):
                    print("Determined that curr == end, returned prev_explored")
                    State.display(curr, message= "Goal State Reached")                   
                    return curr,pathTaken
                else:
                    gbfs_visited.append(curr)

            neighbors= self.neighbors(curr)
            bestN = []
            for i in neighbors:
                print( "The neighbors are , ",i[0])
                print( "The ENTIRE neighbors are , ")
                if self.inVisited(i[0],gbfs_visited):
                    print("SKIPPING SOMETHING__________")
                    continue
                score = self.lars_bennet_heuristic(i[0], goal)
                print("The score is : ", score)
                bestN.append((score,i[0],i[1])) 
                Priority_Queue.append((score,i[0],i[1])) 
            #print("Priority QUEUE : ", Priority_Queue)
            # best =  max(bestN)
            #Priority_Queue.append(best)
            print("Priority QUEUEEEEEEEEE : ", Priority_Queue)
            #print("Best N : ", max(bestN))
            # if Priority_Queue == []:
            #     #We need to do something about this
            #     Priority_Queue.append(best)
            
        return 0

    def lars_bennet_heuristic(self, curr, goal_state):
        curr_score = 0 
        curr_level = self.getLevels(curr)
        level = self.getLevels(goal_state)
        print(curr_level)
        print("-----------------------------")
        print(level)
        #on:
        for i in range(1,len(goal_state)):
            goal_object = State.find(goal_state, goal_state[i].id)
            if curr[i].air == True:
                curr_score += level[i-1] 

            if repr(curr[i].on) == repr(goal_object.on):
                if repr(curr[i].on) == 'table':
                    curr_score += 100
                elif curr_level[i-1] == level[i-1]:
                    curr_score += 30
                else:
                    curr_score -= 20
            else:
                if repr(curr[i].on) == 'table':
                    curr_score += 5
                    #print("Go HERE?", curr_score)
            #clear
            if curr[i].clear == goal_object.clear:
                #if repr(curr[i].on) != 'table':
                    #curr_score += 1
                curr_score += 1
            
    
            
        return curr_score
    
    def global_heuristic(self,curr, goal_state):
        index = 0
    #     curr_score = 0 
        sumTotal = 0
        for i in range(1,len(curr)):
            goal_object = State.find(goal_state, goal_state[i].id)
            if repr(curr[i].on) != 'table':
                sumTotal += 0
                print(curr[i].on)
            index =0
            while(repr(curr[index].on) != 'table'): 
                print(curr[index].on)
                if curr[index].on == goal_object.on:
                    sumTotal += 1
                    index +=1
                else:
                    sumTotal =0
                    break
        return sumTotal


    def getLevels(self, goal_state):
        lst = []
        for i in range(1,len(goal_state)):
            #if(repr(goal_state[i].on) =='table'):
                #print("level 0: ", goal_state[i])
            temp = goal_state[i]
            level = 0 
            #print(temp, "is on", temp.on)
            while repr(temp.on) != 'table':
                if temp.air ==True:
                    level = None
                    break
                temp = temp.on
                level -= 1
            lst.append(level)
        #print(lst)


        return lst


    def sample_plan(self):
        stateFound, pathTaken = self.gbfs(self.initial_state, goal_state_blocks)
        print("This is the path take:", len(pathTaken))
        
        print("THIS IS THE PATH WE TOOK TO SOLVE THAT PROBLEM: ")
        for i in range(1,len(pathTaken)):
            State.display(pathTaken[i][0], message= pathTaken[i][1])
            if i != len(pathTaken)-1:
                self.move(pathTaken[i][0])
        print("Path takes",len(pathTaken)-1,"states and the move count is: ", )

        return 0



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