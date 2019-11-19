import queue

# class tt:
#     def __init__(self,a,b,text):
#         self.a = a
#         self.b = b
#         self.text = text
#     def __str__(self):
#         return 'a=' + str(self.a) +'\t,b='+str(self.b)+'\t'+str(self.text)
# q = queue.PriorityQueue()

# t1 = tt(4,0,'1111')
# t2 = tt(5,0,'2222')
# t3 = tt(2,0,'3333')
# t4 = tt(-11,0,'4444')
# # print(t1)
# q.put((t1.a,t1))
# q.put((t2.a,t2))
# q.put((t3.a,t3))
# q.put((t4.a,t4))

# while not q.empty():
#     print(q.get()[1].text)

"""
5x5
#####
#  S#
# B #
#T  #
#####
"""


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
  
  def getFn(self):
      return self.fn
    
  def updateFn(self):
    self.fn = len(self.sol) + self.euclidean(self.bx,self.by,self.gx,self.gy)  #f(n) = g(n) + h(n)
    return self.fn

  def __cmp__(self,other):
    return cmp(self.fn,other.fn)
    

