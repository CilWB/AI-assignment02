import queue

class tt:
    def __init__(self,a,b,text):
        self.a = a
        self.b = b
        self.text = text
    def __str__(self):
        return 'a=' + str(self.a) +'\t,b='+str(self.b)+'\t'+str(self.text)
q = queue.PriorityQueue()

t1 = tt(4,0,'1111')
t2 = tt(5,0,'2222')
t3 = tt(2,0,'3333')
t4 = tt(-11,0,'4444')
# print(t1)
q.put((t1.a,t1))
q.put((t2.a,t2))
q.put((t3.a,t3))
q.put((t4.a,t4))

while not q.empty():
    print(q.get()[1].text)

"""
5x5
#####
#  S#
# B #
#T  #
#####
"""

