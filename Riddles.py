 #Riddles.py

import csv
import io
import os.path

GLOBAL_PATH = os.getcwd()

class Riddle:

	def __init__(self, row):
		#Row number of the CSV for the riddle or anagram or whatever, my current idea is a two column CSV with the left column being the riddle and the right column being the solution
		riddlefile = open(GLOBAL_PATH + "/qanda.csv", newline='') # csv is encoded in UTF-8
		reader = csv.reader(riddlefile)
		for x in range(row + 1):
			next(riddlefile)
		rowz = next(reader)
		print(rowz)
		self.riddle = rowz[0]
		self.solution = rowz[1]
		riddlefile.close()
		
	def getSolution(self, attempt):
		if attempt == self.solution:
			return True
		return False
		
	def getRiddle(self):
		return self.riddle


	def changeRiddle(row):
		#Row number of the CSV for the riddle or anagram or whatever, my current idea is a two column CSV with the left column being the riddle and the right column being the solution
		riddlefile = open(GLOBAL_PATH + "/qanda.csv")
		reader = csv.reader(riddlefile)
		for x in range(row):
			next(riddlefile)
		rowz = next(reader)
		self.riddle = rowz[0]
		self.solution = rowz[1]
		riddlefile.close()
