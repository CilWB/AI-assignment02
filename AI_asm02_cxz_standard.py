import math
import queue
# import sys

# print(sys.version)

class Problem:
  def __init__(self,prb):
    
    self.sol = []       #solution
    self.state = prb    #current map
    self.x,self.y,self.bx,self.by,self.gx,self.gy = -1,-1,-1,-1,-1,-1  #initial position of S,B,T
    self.directionS = [[-1,0,'n'],[0,-1,'w'],[1,0,'s'],[0,1,'e']]      #S actions                     
    self.directionB = [[-1,0,'N',-2,0],[1,0,'S',2,0],[0,-1,'W',0,-2],[0,1,'E',0,2]] #S and B actions
    self.fn = 0# len(self.sol) + self.euclidean(self.bx,self.by,self.gx,self.gy)  #f(n) = g(n) + h(n)

    #------get S,B,T positions from map------#
    for i in range(len(self.state)):
      for j in range(len(self.state[0])):
        if self.state[i][j] == 'S':
          self.setposition(i,j)
        elif self.state[i][j] == 'T':
          self.setGoalposition(i,j)
        elif self.state[i][j] == 'B':
          self.setBoxposition(i,j)

  # compatible with py v.2.X.X
  # def __cmp__(self,other):
  #   return cmp(float(self.fn),float(other.fn))

  def __lt__(self, other):
    return self.fn < other.fn
  # def __le__(self, other):
  #   return self.fn <= other.fn
  # def __eq__(self, other):
  #   return self.fn == other.fn
  # def __ne__(self, other):
  #   return self.fn != other.fn
  def __gt__(self, other):
    return self.fn > other.fn
  # def __ge__(self, other):
  #   return self.fn >= other.fn


  def setposition(self,x,y):
    self.x,self.y = x,y
    
  def getposition(self):
    return self.x,self.y
  
  def setBoxposition(self,bx,by):
    self.bx,self.by = bx,by
    
  def getBoxposition(self):
    return self.bx,self.by
  
  def setGoalposition(self,gx,gy):
    self.gx,self.gy = gx,gy
    
  def getGoalposition(self):
    return self.gx,self.gy
    
  def goalTest(self,stateNode):
    if stateNode.getBoxposition() == stateNode.getGoalposition():
      return True
    return False
  
  def Action(self,node):
    action = []
    for i in range(4):
      if node.state[node.x+node.directionB[i][0]][node.y+node.directionB[i][1]] == 'B' and node.state[node.x+node.directionB[i][3]][node.y+node.directionB[i][4]] != '#':
         #movement(node.directionB[i][2])
         action.append(node.directionB[i])  
          
      if node.state[node.x+node.directionS[i][0]][node.y+node.directionS[i][1]]  != '#' and node.state[node.x+node.directionS[i][0]][node.y+node.directionS[i][1]] != 'B':
         #movement(node.directionS[i][2])
         action.append(node.directionS[i]) 
    return action 
  
  def euclidean(self,x1,y1,x2,y2):
    return math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
  
  def getFn(self):
      return self.fn
    
  def updateFn(self):
    self.fn = len(self.sol) + self.euclidean(self.bx,self.by,self.gx,self.gy)  #f(n) = g(n) + h(n)
    return self.fn


def Child(node,act):
  
  child = copy.deepcopy(node)
  if len(act)==3:

    #------S actions------#
    if child.state[node.x][node.y] != 'T':
          child.state[child.x][child.y] = ' '
    child.x,child.y = child.x+act[0],child.y+act[1]
    if child.state[child.x][child.y] != 'T':
          child.state[child.x][child.y] = 'S'    
    
  else:
    #------S and B actions------#
        if child.state[child.x][child.y] != 'T':
          child.state[child.x][child.y] = ' '
        if child.state[child.x+act[0]][child.y+act[1]] != 'T':
          child.state[child.x+act[0]][child.y+act[1]] = 'S'
        child.state[child.x+act[3]][child.y+act[4]] = 'B'
        child.bx,child.by = child.bx+act[0],child.by+act[1]
        child.x,child.y = child.x+act[0],child.y+act[1]   
         
  sol = act[2]
  return child,sol

def Greedy(prb):

  fron = queue.PriorityQueue()
  node = copy.deepcopy(prb)
  check = []
  
  if prb.goalTest(node):
    return node.sol
  node.updateFn()
  # fron.put((node.getFn(),node))
  fron.put(node)
#   check.append(node.fn)
  explored = []
  
  while True:
    
    if fron.empty():
      print('fail')
      return [-1]
  
    node = fron.get()
    
    if node.state in explored: #avoid loop
        # print('avoid loop naja')
        continue
    
    
    explored.append(node.state)

    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#' and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':   
        continue 

    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)
      if child.state not in explored and child not in fron.queue:
        if prb.goalTest(child):
          #print(pd.DataFrame(child.state))
          print('Found Goal!!')
          return child.sol
        child.updateFn()
        fron.put(child)


def Astar(prb):

  fron = queue.PriorityQueue()
  node = copy.deepcopy(prb)
  check = []

  if prb.goalTest(node):
    return node.sol

  node.updateFn()
  fron.put(node)
  check.append(node.fn)
  explored = []

  
  while True:
    if fron.empty():
      print('fail')
      return [-1]
    
    node = fron.get()

    if node.state in explored: #avoid loop
      continue
    
    
    explored.append(node.state)

    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#' and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':   
        continue 

    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)
      if child.state not in explored and child not in fron.queue:
        if prb.goalTest(child):
          #print(pd.DataFrame(child.state))
          print('Found Goal!!')
          return child.sol
        child.updateFn()
        fron.put(child)


def BFS(prb):
  fron = queue.Queue()
  node = copy.deepcopy(prb)

  if prb.goalTest(node):
    return node.sol
  
  fron.put(node) #frontier
  explored = []  
  
  while True:
    if fron.empty():
      print('Goal not Found!!')
      return [-1]

    node = fron.get()
    if node.state in explored: #avoid loop
      continue
    explored.append(node.state)

    #-----Check if Box can not move-----#
    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#' and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':       
        continue 
    
    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)

      
      if child.state not in explored and child not in fron.queue:
        if prb.goalTest(child):
          print('Found Goal!!')
          return child.sol
        fron.put(child)
      
    
  
def DFS_limit(prb,limit):
  sol = []
  fron = queue.LifoQueue()
  node = copy.deepcopy(prb)
  if prb.goalTest(node):
    return node.sol
  
  fron.put(node)
  explored = []

  while True:
    if fron.empty():
      break
    node = fron.get()
    explored.append(node.state)
    if len(node.sol) > limit :
        continue
    
    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#'and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':
        # print('fail can not move Box')
        break
        continue

    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)
      
      if child.state not in explored and child not in fron.queue:
        if prb.goalTest(child):
          sol.append(child.sol)
          # return child.sol
        fron.put(child)
  
  return sol
  
  
def IDS(prb,limit):
  # print('start_IDS')
  for i in range(1,limit):
    # print(i)
    sol = DFS_limit(prb,i)
    if sol != []:
        return sol
  return [-1]

#---------------------------------------
#main     
#---------------------------------------
import copy
import time
import os
# import psutil

R,C = input("Enter Map's size (RxC) : ").split('x')
R,C = int(R),int(C)

mapp = [[' '] * C for i in range(R)]
for i in range(R):
    mapp[i][:C]=input()
    if len(mapp[i]) > C:
      print("out range !!!")
      break
      
RAW_mapp = copy.deepcopy(mapp)

print('Map Problem: ')
prb = Problem(mapp)
print('start : ',prb.getposition())
print('box : ',prb.getBoxposition())
print('goal : ',prb.getGoalposition())

##################################################################################################
print("\nGREEDY")
start_time = time.time()
SOL_Greedy = Greedy(prb)
time_Greedy = str((time.time() - start_time))
print("--- %s seconds ---" % (time.time() - start_time))

ANS_Greedy = copy.deepcopy(SOL_Greedy)
print(SOL_Greedy)

print("\nASTAR")
start_time = time.time()
SOL_Astar = Astar(prb)
time_Astar = str((time.time() - start_time))
print("--- %s seconds ---" % (time.time() - start_time))

ANS_Astar = copy.deepcopy(SOL_Astar)
print(SOL_Astar)

print("\nBFS")
start_time = time.time()
SOL_BFS = BFS(prb)
time_BFS =str((time.time() - start_time))
print("--- %s seconds ---" % (time.time() - start_time))

ANS_BFS = copy.deepcopy(SOL_BFS)
print(SOL_BFS)
global walk
walk = []
walk = SOL_BFS

print("\nIDS")
start_time = time.time()
SOL_IDS = IDS(prb,50) #normally 50 
time_IDS =str((time.time() - start_time))
print("--- %s seconds ---" % (time.time() - start_time))

cnt_sol_ids = 0
ANS_IDS = copy.deepcopy(SOL_IDS)
print(SOL_IDS)

last_str = 'Greedy time = ' + time_Greedy + '\n' 
last_str += 'Greedy path : ' + str(ANS_Greedy) 
last_str += '\n' + 'Astar time = ' + time_Astar + '\n' 
last_str += 'Astar path : ' + str(ANS_Astar) + '\n' 
last_str += 'BFS time = ' + time_BFS + '\n' 
last_str += 'BFS path : ' + str(ANS_BFS) + '\n' 
last_str += 'IDS time = ' + time_IDS + '\n' 
last_str += 'IDS path : ' + str(ANS_IDS)
# intForStr = 1
# if ANS_IDS is not None:
#   for i in ANS_IDS:
#     str_ids = str(intForStr)+' : '
#     for j in i:
#       str_ids += j
#     last_str += str_ids+'\n'
#     intForStr+=1
print(last_str)

"""
-------------------------------------------------------
maptest

4x4
####
# B#
#ST#
####

5x5
#####
#T  #
# B #
#  S#
#####

5x5
#####
#  S#
# B #
#T  #
#####

6x6
######
#T#  #
##B  #
#    #
#   S#
######
[['n', 'n', 'w', 'W', 's', 'w', 'N'],

6x6
######
#    #
# B S#
# ## #
#T   #
######

7x7
#######
#   S #
###   #
#  B  #
#   ###
#T    #
#######


20x20
####################
#                  #
#  T               #
#######     ########
#                  #
#      ### ##      #
#       B    S     #
#                  #
###                #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
####################

8x8
########
#T# #  #
#      #
#  B # #
#      #
# #### #
#     S#
########

12x12
############
#   T#  #S #
#  #   #   #
## #   #   #
##     #   #
## ##  #   #
##  ###    #
##  ###### #
#          #
##  #####B #
#       #  #
############


###############
# T        B  #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#            S#
###############


7x11
###########
#T##      #
# # #  ####
#    B   S#
# ######  #
#         #
###########


8x8
########
#  S # #
#     T#
# B ## #
#      #
# #### #
#      #
########


20x20
####################
#                  #
#  T               #
#                  #
#                  #
#                  #
#       B    S     #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
####################


10x10
##########
#        #
#    B   #
# #      #
# S      #
#   #### #
#        #
#        #
###  T   #
##########


10x10
##########
#   T    #
#######  #
#     #  #
#  B  #  #
#     #  #
#     #  #
#        #
#S       #
##########


"""    

