class Node:
  def __init__(self, state=None, parent=None, cost=0):
    self.state = state
    self.parent = parent
    self.children = []
    self.cost = cost

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(state_space, node):
  children = []
  for [m,n,c] in state_space:
    if m == node.state:
      children.append(Node(n, node.state, node.cost+c))
    elif n == node.state:
      children.append(Node(m, node.state, node.cost+c))
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

def ucs(state_space, initial_state, goal_state):
  frontier = []
  explored = []
  found_goal = False
  goalie = Node()
  solution = []
  # add initial state to frontier
  frontier.append(Node(initial_state, None))
  
  while not found_goal:
    # goal test at expansion
    if frontier[0].state == goal_state:
      found_goal = True
      goalie = frontier[0]
      break
    # expand the first in the frontier
    children = expandAndReturnChildren(state_space, frontier[0])
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
    solution.insert(0, goalie.parent)
    for e in explored:
      if e.state == goalie.parent:
        goalie = e
        break
  return solution, path_cost

if __name__ == "__main__":
  # state space and step cost definition
  state_space = [
    ["Arad", "Zerind", 75],
    ["Zerind", "Oradea", 71],
    ["Oradea", "Sibiu", 151],
    ["Sibiu", "Arad", 140],
    ["Sibiu", "Fagaras", 99],
    ["Sibiu", "Rimnicu Vilcea", 80],
    ["Fagaras", "Bucharest", 211],
    ["Bucharest", "Giurgiu", 90],
    ["Bucharest", "Pitesti", 101],
    ["Pitesti", "Rimnicu Vilcea", 97],
    ["Rimnicu Vilcea", "Craiova", 146],
    ["Craiova", "Pitesti", 138],
    ["Craiova", "Drobeta", 120],
    ["Drobeta", "Mehadia", 75],
    ["Mehadia", "Lugoj", 70],
    ["Lugoj", "Timisoara", 111],
    ["Arad", "Timisoara", 118],
    ["Bucharest", "Urziceni", 85],
    ["Urziceni", "Vaslui", 142],
    ["Vaslui", "Iasi", 92],
    ["Iasi", "Neamt", 87],
    ["Urziceni", "Hirsova", 98],
    ["Hirsova", "Eforie", 86]
  ]

  initial_state = "Arad"

  goal_state = "Bucharest"

  [solution, cost] = ucs(state_space, initial_state, goal_state)
  print("Solution:", solution)
  print("Path Cost:", cost)
