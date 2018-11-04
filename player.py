from random import randint

class Player():
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.tries = 0
        self.next=""
        self.prev=""


    def update(self, correct=True, points):
        if correct:
            self.score += points
        else:
            self.score -= randint(100,1000)

        self.tries += 1
       
    def setNext(self,node):
        self.next=node
        
    def setPrev(self,node):
        self.prev=node
      
    def getNext(self):
        return self.next
    
    def getPrev(self):
        return self.prev
    
    def deletePlayer(self):
        self.prev.setNext(self.next)
        self.next.setPrev(self.prev)

