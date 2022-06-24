import string
import random

class Node:
  def __init__(self, state=None, parent=None, parent_list=[], cost=0):
    self.state = state
    self.parent = parent
    # Parent list is added to differentiate between nodes with same state but different parents
    self.parent_list = parent_list
    self.children = []
    self.cost = cost

  def add_children(self, children):
    self.children.extend(children)

# Expands the selected node and return the list of children nodes
def expand_and_return_children(state_space, explored, node):
  children = []
  print("Node state: " + str(node.state))
  parent_list = node.parent_list
  print("Node Parents: " + str(parent_list))
  for [m,n,c] in state_space:
    print([m, n, c])
    if m == node.state:
      children.append(Node(n, node.state, parent_list + [m], node.cost+c))
    elif n == node.state:
      children.append(Node(m, node.state, parent_list + [n], node.cost+c))
  print("Expand and return children:" + str(children))
  return children

# Insert valid nodes into the frontier based on cost
def append_and_sort(frontier, node, explored):
  # If a node state is found in its list of parent nodes, the node is invalid
  invalid = False
  if node.state in node.parent_list:
    invalid = True

  if (not invalid):
    insert_index = len(frontier)
    for i, f in enumerate(frontier):
      if f.cost > node.cost:
        insert_index = i
        break
    frontier.insert(insert_index, node)
  return frontier

# Obtain the number of persons for the state space
def input_no_of_persons():
  no_of_persons = int(input('Enter the number of people to be seated: '))
  return no_of_persons

# Obtain and generate the state space for the search algorithm
def input_state_space(no_of_persons):
  alp_list = list(string.ascii_uppercase)
  # Represent N number of people with the first N alphabet
  person_list = alp_list [:no_of_persons]
  
  # Define initial state
  first_person = random.choice(person_list)
  initial_state = first_person
  print("Initial State: " + str(initial_state))

  print("Please enter two uncomfortability value for each pair of person.\n")
  print("The uncomfortability value range from 1 (least uncomfortable) to 5 (most uncomfortable)\n")
  print("eg: 1,2") 
  print("There is no space between the numbers and comma.") 
    
  # Show all possible pairs from the list
  pair = []
  person_pair = [] 
  for i in range (len(person_list)-1):
      j = i + 1
      while j < (len(person_list)):
          pair=[person_list[i],person_list[j]]
          person_pair.append(pair)
          j += 1
          
  # Ask the user to input the uncomfortability value for each pair of persons
  uncomfort_val = []
  state_space = []
  for i in range (len(person_pair)):
      print('Enter the uncomfort value of', person_pair[i][0], 'and', person_pair[i][1],':')
      x,y = input().split(",")
      
      # Standardise the uncomfortability value to double
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
  # Add initial state to frontier
  frontier.append(Node(initial_state, None))
  
  while not found_goal:
    # The goal is tested at expansion of node
    # The goal is found when the first frontier node has the correct number of parents
    if (len(frontier[0].parent_list)) == (no_of_persons - 1):
      found_goal = True
      print("All persons have been allocated to a seat!")
      goalie = frontier[0]
      break
    # Expand the first node in the frontier
    children = expand_and_return_children(state_space, explored, frontier[0])
    # Add children list to the expanded node
    frontier[0].add_children(children)
    # Add to the explored list
    explored.append(frontier[0])
    # Remove the expanded frontier
    del frontier[0]
    # Add children to the frontier
    for child in children:
      # check if a node with its associated parents was expanded or generated previously
      if not ((child.parent_list + [child.state]) in [ e.parent_list + [e.state] for e in explored ]):
        frontier = append_and_sort(frontier, child, explored)
    print("Explored:", [e.state for e in explored])
    print("Frontier:", [(f.state, f.cost) for f in frontier])
    print("Children:", [c.state for c in children])
    print("")
  
  # Output the solution
  solution = str(goalie.parent_list)[:-1] + ", \'" + str(goalie.state) + "\']"
  path_cost = goalie.cost
  return solution, path_cost

if __name__ == "__main__":
  # Obtain the number of persons
  no_of_persons = input_no_of_persons()
  # Obtain the generated state space and initial state
  [state_space, initial_state] = input_state_space(no_of_persons)
  print("State space generated:")
  for state in state_space:
    print(state)
  
  # Perform uniform cost search and output the results
  [solution, cost] = ucs(state_space, initial_state, no_of_persons)
  print("Solution:", solution)
  print("Path Cost:", cost)