
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11159677, 'Saskia', 'Wells'), (12059544, 'Harrison', 'Mollenhauer'), (11323442, 'Joshua', 'Oates')]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    
    C = warehouse.ncols
    R = warehouse.nrows

    walls = set(warehouse.walls)
    targets = set(warehouse.targets)

    def wall(x,y):
        return (x,y) in walls
    
    taboo = set()

    rows = []
    for y in range(R):
        row = ""
        for x in range(C):
            if (x, y) in walls:
                row += "#"
            else:
                row += " "
        rows.append(row)

    trimmed_len = [len(rows[y].rstrip()) for y in range(R)]

    # -- Rule 1 -- #

    def corner(x,y):
        return (
            (wall(x-1, y) and wall(x, y-1)) or
            (wall(x+1, y) and wall(x, y-1)) or
            (wall(x-1, y) and wall(x, y+1)) or
            (wall(x+1, y) and wall(x, y+1))
        )
    
    for y in range(R):
        for x in range(C):
            if x >= trimmed_len[y]:
                continue
            if (x, y) not in walls and (x, y) not in targets:
                if corner(x, y):
                    taboo.add((x, y))

    # -- Rule 2 -- #
    for y in range(R):
        corner = [x for x in range(C) if (x,y) in taboo]
        for i in range(len(corner)-1):
            x1, x2 = corner[i], corner[i+1]
            segment = [(x, y) for x in range(x1+1, x2)]
            segment = [(x, y) for (x, y) in segment if x < trimmed_len[y]]
            if all ((x,y) not in targets for x, y in segment):
                for (x,y) in segment:
                    if (x,y) not in walls:
                        taboo.add((x,y))

    for x in range(C):
        corner = [y for y in range(R) if (x,y) in taboo]
        for i in range(len(corner)-1):
            y1, y2 = corner[i], corner[i+1]
            segment = [(x, y) for y in range(y1+1, y2)]
            segment = [(x, y) for (x, y) in segment if x < trimmed_len[y]]
            if all ((x,y) not in targets for x, y in segment):
                for (x,y) in segment:
                    if (x,y) not in walls:
                        taboo.add((x,y))

    out = []
    for y in range(R):
        row = ""
        for x in range (C):
            if (x,y) in walls:
                row += '#'
            elif (x,y) in taboo:
                row += "X"
            else:
                row += " "
        out.append(row)
    
    return "\n".join(out)
        

    # raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        wh = state.copy()
        worker = list(wh.worker)
        boxes = set(wh.boxes)
        walls = set(wh.walls)

        possible = []

        DIR = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
        }
        wx,wy = worker

        for action in DIR:
            # check each actions possible before adding action to possible list
            dx,dy = DIR[action]
            nx,ny = wx + dx, wy + dy
            if (nx, ny) in walls:
                continue
            if (nx, ny) in boxes:
                bx, by = nx + dx, ny + dy
                if (bx, by) in walls or (bx, by) in boxes:
                    continue
            possible.append(action)    

        return possible
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        DIR = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
        }

        wh = state.copy()
        worker = list(wh.worker)
        boxes = set(wh.boxes)

        wx, wy = worker
        dx,dy = DIR[action]
        nx,ny = wx+dx, wy+dy

        if (nx, ny) in boxes:
            bx, by = nx + dx, ny + dy

        
            boxes.remove((nx, ny))
            boxes.add((bx, by))
        
        worker = [nx, ny]


        return wh.copy(worker=tuple(worker), boxes=tuple(sorted(boxes)))

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""

        return state == self.goal


    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        ## this function checks the difference in box positions as only they are weighted
        # the fucntion assumes since the states are from the same game, the weights of the boxes are the same and the boxes are also ordered the same.
        # since it checks box location difference, the action variable is unused. 
        #


        wh1 = state1.copy()
        wh2 = state2.copy()

        boxes1 = list(wh1.boxes)
        boxes2 = list(wh2.boxes)

        weights = list(wh1.weights)
        i = 0
        for i in range(len(boxes1)):
            if boxes1[i] != boxes2[i]:
                return c + weights[i]

        return c + 1



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    DIR = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
    }

    wh = warehouse.copy()
    worker = list(wh.worker)
    boxes = set(wh.boxes)
    walls = set(wh.walls)

    for action in action_seq:

        if action not in DIR:
            return "Impossible"
        
        dx, dy = DIR[action]
        wx, wy = worker
        nx, ny = wx + dx, wy+dy

        if (nx, ny) in walls:
            return "Impossible"
        
        if (nx, ny) in boxes:
            bx, by = nx + dx, ny + dy

            if (bx, by) in walls or (bx, by) in boxes:
                return "Impossible"
            
            boxes.remove((nx, ny))
            boxes.add((bx, by))
        
        worker = [nx, ny]
    
    return warehouse.copy(worker=tuple(worker), boxes=tuple(sorted(boxes))).__str__()
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

