from random import randint

class Player():
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.tries = 0


    def update(self, correct=True):
        if correct:
            self.score += randint(100,1000)
        else:
            self.score -= randint(100,1000)

        self.tries += 1

