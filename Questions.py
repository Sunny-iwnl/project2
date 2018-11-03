import csv
import io
import os.path

GLOBAL_PATH = os.getcwd()

class Questions:

	def __init__(self):
	
		self.question = ""
		self.solution = ""
		file = open(GLOBAL_PATH + "/qanda.csv")
		reader = csv.reader(file)
		row_count = sum(1 for row in reader)
		self.given = range(row_count)
		
	def trySolution(self, attempt):
		if attempt == self.solution:
			return True
		return False
		
	def getQuestion(self):
		return self.question

	def getRandomQuestion(self):
		file = open(GLOBAL_PATH + "/qanda.csv")
		reader = csv.reader(file)
		row_count = sum(1 for row in reader)
		row = random.randint(1,row_count)
		while row in self.given:
			row = random.randint(1,row_count)
		for x in range(row):
			next(file)
		rowz = next(reader)
		self.question = rowz[0]
		self.question = fixNewLine(self.question)
		self.solution = rowz[1]
		file.close()
		
	def getSpecificQuestion(self, row):

		file = open(GLOBAL_PATH + "/qanda.csv")
		reader = csv.reader(file)
		for x in range(row):
			next(file)
		rowz = next(reader)
		self.question = rowz[0]
		self.question = fixNewLine(self.question)
		self.solution = rowz[1]
		file.close()
		
	def fixNewLine(self, input):
		y = input.split("\\n")
		for x in range(y):
			out += x
			out += "\n"
		return out
		
	