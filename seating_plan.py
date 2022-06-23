class Node:
  def __init__(self, state=None, parent=None, cost=0):
    self.state = state
    self.parent = parent
    self.children = []
    self.cost = cost

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(uncomfort_data, node):
  children = []
  # ['A', 'B', 1.5]
  print("Uncomfort data: " + str(uncomfort_data))
  print("Node state: " + str(node.state))
  # Node state is list, m and n element is string, ['A'] != 'A'
  for [m,n,c] in uncomfort_data:
    if m == node.state:
      print("Found m = node.state")
      children.append(Node(n, node.state, node.cost+c))
    elif n == node.state:
      print("Found n = node.state")
      children.append(Node(m, node.state, node.cost+c))
  print("Expand and return children:" + str(children))
  return children

def appendAndSort(frontier, node):
  duplicated = False
  removed = False
  for i, f in enumerate(frontier):
    if f.state == node.state:
      duplicated = True
      if f.cost > node.cost:
        del frontier[i]
        removed = True
        break    
  if (not duplicated) or removed:
    insert_index = len(frontier)
    for i, f in enumerate(frontier):
      if f.cost > node.cost:
        insert_index = i
        break
    frontier.insert(insert_index, node)
  return frontier

def ucs(uncomfort_data, initial_state, total_persons):
  frontier = []
  explored = []
  found_goal = False
  goalie = Node()
  solution = []
  # add initial state to frontier
  frontier.append(Node(initial_state, None))
  
  while not found_goal:
    # goal test at expansion
    if len(explored) == (total_persons - 1):
      found_goal = True
      print("All persons have been allocated to a seat!")
      print("Allocated persons: " + str(explored))
      goalie = frontier[0]
      break
    # expand the first in the frontier
    print("Selected node: " + str(frontier[0].state))
    children = expandAndReturnChildren(uncomfort_data, frontier[0])
    # add children list to the expanded node
    frontier[0].addChildren(children)
    # add to the explored list
    explored.append(frontier[0])
    # remove the expanded frontier
    del frontier[0]
    # add children to the frontier
    for child in children:
      # check if a node was expanded or generated previously
      if not (child.state in [e.state for e in explored]):        
        frontier = appendAndSort(frontier, child)
    print("Explored:", [e.state for e in explored])
    print("Frontier:", [(f.state, f.cost) for f in frontier])
    print("Children:", [c.state for c in children])
    print("")
  
  solution = [goalie.state]
  path_cost = goalie.cost
  while goalie.parent is not None:
    print("Goalie parent: " + str(goalie.parent))
    solution.insert(0, goalie.parent)
    for e in explored:
      if e.state == goalie.parent:
        goalie = e
        print("Goalie state: " + str(goalie.state))
        break
  return solution, path_cost

if __name__ == "__main__":
  # state space and step cost definition
  uncomfort_data = [
    ['A', 'B', 1.5],
    ['A', 'C', 2],
    ['A', 'D', 2],
    ['A', 'E', 4],
    ['B', 'C', 1],
    ['B', 'D', 4.5],
    ['B', 'E', 2.5],
    ['C', 'D', 3],
    ['C', 'E', 1.5],
    ['D', 'E', 1]
  ]

  # # Get a list of alphabet to represent the peoples
  # alp_list = list(string.ascii_uppercase)
  # n =  int(input('Enter the number of people to be seated: '))
    
  # person_list = alp_list [:n]
  # print(person_list) 

  # Define initial state
  initial_state = 'A'
  # first_person = random.choice(person_list)
  # initial_state.append(first_person)  
  print(initial_state)

  # # Input 
  # print('Please enter the uncomfort value\n')
  # print('The uncomfort value range from 1 (most comfortable) to 5 (most uncomfortable)\n')
  # for i in range (n):
  #   for j in range (n):
  #       if (person_list[i] != person_list[j]):
  #           print('Enter the uncomfort value of', person_list[i], 'towards', person_list[j],':')
  #           v = input()
  #           uncomfortVal=[person_list[i],person_list[j]]
  #           uncomfortVal.append(v)
  #           state_space.append(uncomfortVal) 

  [solution, cost] = ucs(uncomfort_data, initial_state, 5)
  print("Solution:", solution)
  print("Path Cost:", cost)