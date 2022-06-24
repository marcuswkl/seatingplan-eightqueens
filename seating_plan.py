import string
import random

class Node:
  def __init__(self, state=None, parent=None, parent_list=None, cost=0):
    self.state = state
    self.parent = parent
    self.parent_list = parent_list
    self.children = []
    self.cost = cost

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(state_space, explored, node):
  children = []
  # ['A', 'B', 1.5]
  print("State space: " + str(state_space))
  print("Node state: " + str(node.state))
  parent_list = get_parent_list(node, explored)
  print("Node Parents: " + str(parent_list))
  for [m,n,c] in state_space:
    if m == node.state:
      # print (['A', n, c])
      # print("Found m = node.state")
      children.append(Node(n, node.state, parent_list, node.cost+c))
    elif n == node.state:
      # print ([m, 'A', c])
      # print("Found n = node.state")
      children.append(Node(m, node.state, parent_list, node.cost+c))
  print("Expand and return children:" + str(children))
  return children

def appendAndSort(frontier, node, explored):
  # print("Evaluating current node: " + node.state)
  # Check if node is found in preceding nodes
  parent_list = get_parent_list(node, explored)
  # print("Parent List: " + str(parent_list))
  duplicated = False
  if node.state in parent_list:
    duplicated = True

  # duplicated = False
  # removed = False
  # for i, f in enumerate(frontier):
    # if f.state == node.state:
      # print("Current node is a duplicate.")
      # duplicated = True
      # if f.cost > node.cost:
      #   del frontier[i]
      #   removed = True
      #   break
  # if (not duplicated) or removed:
  if (not duplicated):
    insert_index = len(frontier)
    for i, f in enumerate(frontier):
      if f.cost > node.cost:
        insert_index = i
        break
    # print("Current node inserted into frontier.")
    frontier.insert(insert_index, node)
  return frontier

def get_parent_list(node, explored):
  parent_list = []
  while node.parent is not None:
    parent_list.append(node.parent)
    for e in explored:
      if e.state == node.parent:
        node = e
        break
  return parent_list

def get_parent_count(node, explored):
  parent_count = 0
  while node.parent is not None:
    parent_count += 1
    for e in explored:
      if e.state == node.parent:
        node = e
        break
  return parent_count

def input_no_of_persons():
  no_of_persons = int(input('Enter the number of people to be seated: '))
  return no_of_persons

def input_state_space(no_of_persons):
  alp_list = list(string.ascii_uppercase)
  # Represent N number of people with the first N alphabet
  person_list = alp_list [:no_of_persons]
  
  # Define initial state
  first_person = random.choice(person_list)
  initial_state = first_person
  print("Initial State: " + str(initial_state))

  print('Please enter two uncomfort value for each pair of people.\n')
  print('The uncomfort value range from 1 (most comfortable) to 5 (most uncomfortable)\n')
  print('eg: 1,2 ') 
    
  # Show all possible pairs from the list
  pair = []
  person_pair = [] 
  for i in range (len(person_list)-1):
      j = i + 1
      while j < (len(person_list)):
          pair=[person_list[i],person_list[j]]
          person_pair.append(pair)
          j += 1
          
  # Ask the user to input the uncomfort value for each pair of people
  uncomfort_val = []
  state_space = []
  for i in range (len(person_pair)):
      print('Enter the uncomfort value of', person_pair[i][0], 'and', person_pair[i][1],':')
      x,y = input().split(",")
      
      # Standardise the uncomfort value to double
      avg_val = float((int(x) + int(y)) / 2)
      uncomfort_val=[person_pair[i][0],person_pair[i][1]]
      uncomfort_val.append(avg_val)
      state_space.append(uncomfort_val)
      
  return [state_space, initial_state]

def ucs(state_space, initial_state, no_of_persons):
  frontier = []
  explored = []
  found_goal = False
  goalie = Node()
  solution = []
  # add initial state to frontier
  frontier.append(Node(initial_state, None))
  # depth = 0
  parent_count = 0
  
  while not found_goal:
    # goal test at expansion
    if parent_count == (no_of_persons - 1):
      found_goal = True
      print("All persons have been allocated to a seat!")
      print("Allocated persons: " + str(explored))
      goalie = frontier[0]
      break
    # expand the first in the frontier
    children = expandAndReturnChildren(state_space, explored, frontier[0])
    # add children list to the expanded node
    frontier[0].addChildren(children)
    # add to the explored list
    explored.append(frontier[0])
    # remove the expanded frontier
    del frontier[0]
    # add children to the frontier
    for child in children:
      # print("Iterating over current child: " + child.state)
      # check if a node was expanded or generated previously
      # if child.state in [e.state for e in explored]: 
      #   print("Current node is expanded previously.")    
      # if not (child.state in [e.state for e in explored]): 
      #   print("Current node is not expanded previously.")
      if not (child.state in [e.state for e in explored]) and not (child.parent_list == [e.parent_list for e in explored]):
        frontier = appendAndSort(frontier, child, explored)
    # print("Frontier[0] Parent: " + str(frontier[0].parent))
    # print("Explored[-1] State: " + str(explored[-1].state))
    # if frontier[0].parent == explored[-1].state:
    #   print("Depth increased.")
    #   depth += 1
    parent_count = get_parent_count(frontier[0], explored)
    print("Explored:", [e.state for e in explored])
    print("Frontier:", [(f.parent, f.state, f.cost) for f in frontier])
    print("Children:", [c.state for c in children])
    # print("Depth: " + str(depth))
    print("Frontier Node Parent List: " + str(get_parent_list(frontier[0], explored)))
    print("Frontier Node Parent Count: " + str(get_parent_count(frontier[0], explored)))

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
  no_of_persons = input_no_of_persons()
  [state_space, initial_state] = input_state_space(no_of_persons)
  print("State space generated:")
  for state in state_space:
    print(state)
  
  [solution, cost] = ucs(state_space, initial_state, no_of_persons)
  print("Solution:", solution)
  print("Path Cost:", cost)