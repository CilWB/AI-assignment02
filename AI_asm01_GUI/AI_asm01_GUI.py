import math
class Problem:
  def __init__(self,prb):
    
    self.sol = []       #solution
    self.state = prb    #current map
    self.x,self.y,self.bx,self.by,self.gx,self.gy = -1,-1,-1,-1,-1,-1  #initial position of S,B,T
    self.directionS = [[-1,0,'n'],[0,-1,'w'],[1,0,'s'],[0,1,'e']]      #S actions                     
    self.directionB = [[-1,0,'N',-2,0],[1,0,'S',2,0],[0,-1,'W',0,-2],[0,1,'E',0,2]] #S and B actions
    
    self.fn = len(self.sol) + self.euclidean(self.bx,self.by,self.gx,self.gy)  #f(n) = g(n) + h(n)

    #------get S,B,T positions from map------#
    for i in range(len(self.state)):
      for j in range(len(self.state[0])):
        if self.state[i][j] == 'S':
          self.setposition(i,j)
        elif self.state[i][j] == 'T':
          self.setGoalposition(i,j)
        elif self.state[i][j] == 'B':
          self.setBoxposition(i,j)


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

  fron = []
  node = copy.deepcopy(prb)
  check = []
  

  if prb.goalTest(node):
    return node.sol
  
  fron.append(node)
  check.append(node.fn)
  explored = []

  
  while True:
    
    if fron==[]:
      print('fail')
      return [-1]
    
    count = 0
    num = min(check)
    check.remove(num)
    for i in fron:
      if i.fn == num:
        node = fron.pop(count)
        break
      count+=1
    
    if node.state in explored: #avoid loop
      continue
    
    
    explored.append(node.state)

    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#' and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':   
        continue 

    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)
      if child.state not in explored and child.state not in fron:
        if prb.goalTest(child):
          #print(pd.DataFrame(child.state))
          print('Found Goal!!')
          return child.sol
        fron.append(child)
        check.append(child.fn)


def Astar(prb):

  fron = []
  node = copy.deepcopy(prb)
  check = []
  

  if prb.goalTest(node):
    return node.sol
  
  fron.append(node)
  check.append(node.fn)
  explored = []

  
  while True:
    
    if fron==[]:
      print('fail')
      return [-1]
    
    count = 0
    num = min(check)
    check.remove(num)
    for i in fron:
      if i.fn == num:
        node = fron.pop(count)
        break
      count+=1
    
    if node.state in explored: #avoid loop
      continue
    
    
    explored.append(node.state)

    for i in range(4):
      if node.state[node.bx+node.directionS[i][0]][node.by+node.directionS[i][1]]=='#' and node.state[node.bx+node.directionS[(i+1)%4][0]][node.by+node.directionS[(i+1)%4][1]]=='#':   
        continue 

    for action in prb.Action(node):
      child,tempsol = Child(node,action)
      child.sol.append(tempsol)
      if child.state not in explored and child.state not in fron:
        if prb.goalTest(child):
          #print(pd.DataFrame(child.state))
          print('Found Goal!!')
          return child.sol
        fron.append(child)
        check.append(child.fn)


def BFS(prb):
  fron = []
  node = copy.deepcopy(prb)

  if prb.goalTest(node):
    return node.sol
  
  fron.append(node) #frontier
  explored = []  
  
  while True:
    if fron==[]:
      print('Goal not Found!!')
      return [-1]

    node = fron.pop(0)
    
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

      
      if child.state not in explored and child.state not in fron:
        if prb.goalTest(child):
          print('Found Goal!!')
          return child.sol
        fron.append(child)
      
    
  
def DFS_limit(prb,limit):
  sol = []
  fron = []
  node = copy.deepcopy(prb)
  if prb.goalTest(node):
    return node.sol
  
  fron.append(node)
  explored = []

  while True:
    if fron==[]:
      break
    node = fron.pop(0)
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
      
      if child.state not in explored and child.state not in fron:
        if prb.goalTest(child):
          # sol.append(child.sol)
          return child.sol
        fron.append(child)
  
  return sol
  
  
def IDS(prb,limit):
  for i in range(limit):
    # print(i)
    sol = DFS_limit(prb,i)
    if sol != []:
        return sol

#-------------------------------------#
#                                     #
#---------- GUI Functions ------------#
#                                     #
#-------------------------------------#
import tkinter

def findPlayer():
    for i in range(w):
        for j in range(h):
            if(mapp[j][i] == 'S'):
                return(i,j)

def kvadrat(x, y, barva):
    canvas.create_rectangle(x, y, x+wid, y+hei, fill=barva)

def krog(x, y, barva):
    canvas.create_oval(x, y, x+wid, y+hei, fill=barva)
    
def draw():
    canvas.delete("all")
    for i in range(wid, width, wid):
        canvas.create_line(i, 0, i, height)

    for i in range(hei, height, hei):
        canvas.create_line(0, i, width, i)

    for i in range(w):
        for j in range(h):
            if(mapp[j][i] == '#'):
                kvadrat(i*wid, j*hei, "#252525")
            if(mapp[j][i] == 'S'):
                krog(i*wid, j*hei, "red")
            if(mapp[j][i] == 'B'):
                kvadrat(i*wid, j*hei, "blue")
            if(mapp[j][i] == 'T'):
                kvadrat(i*wid, j*hei, "yellow")

def premikanje(x, y):
#    print("Hej")
    global ply_y, ply_x
    if(mapp[ply_y + y][ply_x + x] in dovoljeni):
        odmik(ply_x, ply_y)
        ply_y += y
        ply_x += x
        premik_na(ply_x, ply_y)

    elif(mapp[ply_y + y][ply_x + x] in premikajoci):
        if(mapp[ply_y + 2*y][ply_x + 2*x] in dovoljeni):
            odmik_stvar(ply_x + x, ply_y + y)
            premik_stvar_na(ply_x + 2*x, ply_y + 2*y)
            odmik(ply_x, ply_y)
            ply_y += y
            ply_x += x
            premik_na(ply_x, ply_y)

def odmik(x, y):
    #global ply_y, ply_x
    if(mapp[y][x] == 'S'):
        mapp[y][x] = ' '
    # if(p[y][x] == 'A'):
    #     p[y][x] = 'X'

def premik_na(x, y):
    # if(p[y][x] == 'X'):
    #     p[y][x] = 'A'
    if(mapp[y][x] == ' '):
        mapp[y][x] = 'S'

def odmik_stvar(x, y):
    if(mapp[y][x] == 'B'):
        mapp[y][x] = ' '
    if(mapp[y][x] == 'R'):
        mapp[y][x] = 'T'
        
def premik_stvar_na(x, y):
    if(mapp[y][x] == ' '):
        mapp[y][x] = 'B'
    if(mapp[y][x] == 'T'):
        mapp[y][x] = 'R'

def isWin(n):
    global walk
    if len(walk)==0:
      return True
    return False
  
def movement(n):
    global ply_x, ply_y

    if(n == 'n' or n == 'N'):
        premikanje(0, -1)

    elif(n == 's' or n == 'S'):
        premikanje(0, 1)

    elif(n == 'w' or n == 'W'):
        premikanje(-1, 0)

    elif(n == 'e' or n == 'E'):
        premikanje(1, 0)

    draw()
    if(isWin(len(SOL_BFS))):
        showinfo("You won!",last_str) #"Congratulations, you won!----------------------------------------")
        # root.destroy()

def restart():
    global prb
    global ply_x, ply_y
    global mapp
    global RAW_mapp
    # p = makeLevel(level)
    mapp = copy.deepcopy(RAW_mapp)
    for i in range(len(mapp)):
      for j in range(len(mapp[i])):
        if mapp[i][j] == 'S' :
          ply_x, ply_y = i,j #prb.getposition() #findPlayer()
    draw()
    
    


def keyHandler(event):
  
    global ANS_IDS,ANS_BFS,SOL_IDS,SOL_BFS
    global walk,cnt_sol_ids
    foo = event.keysym
    print(foo)
    if foo == 'space' : 
      print(walk)
      if walk != [] :
          movement(walk.pop(0))
    elif (event.char == 'r'):
        if walk == []:
          print('you pressed r!')
          restart()
    elif foo=='e':
        root.destroy()
    elif foo=='i':
        if walk == []:
          walk = copy.deepcopy(ANS_IDS[cnt_sol_ids])
          print('ids #',cnt_sol_ids,' = ',walk,end='')
          cnt_sol_ids += 1
          cnt_sol_ids %= len(ANS_IDS)
    elif foo=='b' or foo=='B':
        if walk == []:
          walk = copy.deepcopy(ANS_BFS)



#---------------------------------------
#main     
#---------------------------------------
import copy
import time
import os
# import psutil

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
try:
    from tkinter.filedialog import askopenfilename
except ImportError:
    from tkFileDialog import askopenfilename
try:
    from tkinter.messagebox import *
except ImportError:
    from tkMessageBox import *





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

#                                  #
#--------- GUI Map BEGIN ----------#
#                                  #
if(not mapp):
    pass
else:
    w = len(mapp[0])
    h = len(mapp)

    dovoljeni = [' ', 'T']
    premikajoci = ['B', 'R']


    max_width = 1000
    max_height = 1000


    wid = hei = 50

    if(wid*w > max_width or hei*h > max_height):
        wid = hei = min(max_width//w, max_height//h)
    width = wid * w
    height = hei * h



    ply_x, ply_y = findPlayer()
    #print(ply_x,ply_y)

    root = Tk()
    root.title("Easy Sokoban")
    root.focus_force()
    label = tkinter.Label(root, text = "Easy Sokoban", font = "2005_iannnnnCPU.ttf",).grid(row = 0)
    canvas = Canvas(root, width=width, height=height)
    canvas.grid(row = 1)
    draw()

    
#                                #
#--------- GUI Map END ----------#
#                                #


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
    SOL_IDS = IDS(prb,50) 
    time_IDS =str((time.time() - start_time))
    print("--- %s seconds ---" % (time.time() - start_time))

    cnt_sol_ids = 0
    ANS_IDS = copy.deepcopy(SOL_IDS)
    print(SOL_IDS)


    
  
    last_str = 'Greedy time = ' + time_Greedy + '\n' + 'Greedy path : ' + str(ANS_Greedy) + '\n' + 'Astar time = ' + time_Astar + '\n' + 'Astar path : ' + str(ANS_Astar) + '\n' + 'BFS time = ' + time_BFS + '\n' + 'BFS path : ' + str(ANS_BFS) + '\n' + 'IDS time = ' + time_IDS + '\n' + 'IDS path : ' 
    last_str += str(ANS_IDS)
    # intForStr = 1
    # if ANS_IDS is not None:
    #   for i in ANS_IDS:
    #     str_ids = str(intForStr)+' : '
    #     for j in i:
    #       str_ids += j
    #     last_str += str_ids+'\n'
    #     intForStr+=1

    root.bind_all("<Key>", keyHandler)
    root.mainloop()

      





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

"""    

