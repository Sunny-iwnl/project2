from random import randint

class Player():
    def __init__(self,name, number):
        self.name = name
        self.number = number
        self.score = 0
        self.tries = 3
        self.next= None
        self.prev= None

    def update(self, correct, points):
        if correct:
            self.score += points
        else:
            self.score -= 5
            self.tries -= 1

    def getName(self):
        return self.name

    def getPlayerNum(self):
        return self.number

    def getScore(self):
        return self.score

    def getTries(self):
        return self.tries
       
    def setNext(self,node):
        self.next=node
        
    def setPrev(self,node):
        self.prev=node
      
    def getNext(self):
        return self.next
    
    def getPrev(self):
        return self.prev

    def addPlayer(self, node):
        self.setNext(node)
        node.setPrev(self)
    
    def deletePlayer(self):
        self.prev.setNext(self.next)
        self.next.setPrev(self.prev)

