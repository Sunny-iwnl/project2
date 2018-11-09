from tkinter import *
from Questions import Questions

'''-----------------Global Variables ------------------'''
VERSION = 0.1
ACTIVE_SCORE = 0
DEF_NUM_QUESTIONS = 9
DEFAULT_TRIES = 3
ACTIVE_TRIES = DEFAULT_TRIES
ACTIVE_QUESTION = 0
ACTIVE_PLAYER = 0
ASKING_NUM_PLAYERS = FALSE
ACTIVE_TURN = 0

# instantiate the main game window
MASTER = Tk()
MASTER.geometry("800x600")
MASTER.title("Trivia Game v" + str(VERSION))

# lets us know if we're in game
IN_GAME = False

# prepare the text field for the feedback to be presented to the user
FEEDBACK_FIELD = Text(bg="black", foreground="lightgreen", highlightbackground="black")

#create a frame to house the entry field and submit button
INPUT_FRAME = Frame(MASTER, bg="lightgray")
ENTRY_FIELD = Entry(text="", relief="groove", highlightbackground="lightgray")
SUBMIT_BUTTON = Button(text="Submit", command=lambda: [check_input(ENTRY_FIELD.get().lower()), ENTRY_FIELD.delete(0, END), ENTRY_FIELD.focus()])

# label widget which keeps track of the global variables 
SCORE_WIDGET = Label(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray")

# go ahead and 
CURRENT_QUESTION = Questions()
currentpointvalue=Questions.getPointValue()

PLAYERS = []
NUM_PLAYERS = 0

'''-----------------------------------'''

def send_output(string):
	global FEEDBACK_FIELD

	FEEDBACK_FIELD.config(state=NORMAL)
	FEEDBACK_FIELD.insert(END, str(string))
	FEEDBACK_FIELD.see("end")
	FEEDBACK_FIELD.config(state=DISABLED)

def send_outputln(string):
	global FEEDBACK_FIELD

	FEEDBACK_FIELD.config(state=NORMAL)
	FEEDBACK_FIELD.insert(END, str(string) + "\n")
	FEEDBACK_FIELD.see("end")
	FEEDBACK_FIELD.config(state=DISABLED)

def clear_textbox():
	global FEEDBACK_FIELD

	FEEDBACK_FIELD.config(state=NORMAL)
	FEEDBACK_FIELD.delete('1.0', END)
	FEEDBACK_FIELD.config(state=DISABLED)

def load_next_question():
	global ACTIVE_SCORE
	global ACTIVE_QUESTION
	
	global IN_GAME

	clear_textbox()
	if IN_GAME:
		ACTIVE_SCORE += CURRENT_QUESTION.getPointValue()

		if (ACTIVE_QUESTION < DEF_NUM_QUESTIONS):
			ACTIVE_QUESTION += 1 
		elif (ACTIVE_QUESTION == DEF_NUM_QUESTIONS):
			ACTIVE_QUESTION = 0
		
	if (ACTIVE_QUESTION == DEF_NUM_QUESTIONS):
		ACTIVE_QUESTION = 0

	CURRENT_QUESTION.getSpecificQuestion(ACTIVE_QUESTION+1)
	

	send_outputln(str(ACTIVE_QUESTION+1) + ". " + str(CURRENT_QUESTION.getQuestion()))

	SCORE_WIDGET.config(text="Player " + str(ACTIVE_PLAYER) + "\'s Turn, " + "Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
	SCORE_WIDGET.update()

def give_strike():
	global ACTIVE_SCORE
	global ACTIVE_TRIES
	global IN_GAME
	global SCORE_WIDGET
	global ACTIVE_PLAYER
	global NUM_PLAYERS

	if IN_GAME:
		ACTIVE_TRIES -= 1
		ACTIVE_SCORE -= 5

		if ( ACTIVE_TRIES > 1 ):
			SCORE_WIDGET.config(text="Player " + str(ACTIVE_PLAYER) + "\'s Turn, " + "Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
		elif ( ACTIVE_TRIES == 1):
			SCORE_WIDGET.config(text="Player " + str(ACTIVE_PLAYER) + "\'s Turn, " + "Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
			SCORE_WIDGET.config(fg="red")
		elif ( NUM_PLAYERS == 1 and ACTIVE_TRIES == 0 ):
			SCORE_WIDGET.config(text="Game Over!  Type \"start\" to play again, or \"quit\" to quit.", fg="white", bg="red")

	SCORE_WIDGET.update()

# when the game ends or if the user gets a game over
# call this method to reset all values to their defaults
# and throw the user back to the first part of the game
def reset_everything():
	global ACTIVE_TRIES
	global ACTIVE_SCORE
	global ACTIVE_QUESTION
	global IN_GAME
	global PLAYERS
	global begun

	IN_GAME = False

	# reset the global score and tries to their default values
	ACTIVE_TRIES = DEFAULT_TRIES
	ACTIVE_SCORE = 0
	ACTIVE_QUESTION = 0

	PLAYERS = []

	# clear the textbox of any previous feedback 
	clear_textbox()

	intro_sequence()

	#reset the text widget back to what it was at the beginning
	SCORE_WIDGET.config(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
	SCORE_WIDGET.update()

#should be whatever the intro sequence for the game is.  
# edit this code accordingly.
def intro_sequence():
	global FEEDBACK_FIELD
	clear_textbox()
	send_outputln("Welcome to version " + str(VERSION) + " of our trivia game!  Type \"begin\" to begin, or \"quit\" to quit")

def check_input(input):
	global MASTER
	global SCORE_WIDGET
	global ENTRY_FIELD
	global FEEDBACK_FIELD
	global IN_GAME
	global PLAYERS
	global NUM_PLAYERS
	global ASKING_NUM_PLAYERS
	global ACTIVE_SCORE
	global ACTIVE_TRIES
	global ACTIVE_PLAYER
	global ACTIVE_TURN

	if ( input == "quit" ):
		MASTER.destroy()
	elif ( ASKING_NUM_PLAYERS and not IN_GAME ):
		NUM_PLAYERS = int(input)


		for i in range(0, NUM_PLAYERS):
		# slot 1 is their tries, slot 2 is their score, slot 3 is their current question
			player_state = [0, DEFAULT_TRIES]
			PLAYERS.append(player_state)
			print(len(PLAYERS))

		if NUM_PLAYERS == 1: 
			ASKING_NUM_PLAYERS = False
			ACTIVE_PLAYER = 1
			load_next_question()
			IN_GAME = True

		elif NUM_PLAYERS > 1:
			send_outputln("Multiplayer not yet implemented.")

	elif ( input == "begin" and not IN_GAME ):
		clear_textbox()
		send_outputln("How many people are playing?  Type the number below and press ENTER.")
		ASKING_NUM_PLAYERS = True

	elif ( (ACTIVE_TRIES == 0  or IN_GAME == FALSE) and input == "start"):
		reset_everything()
	elif ( not CURRENT_QUESTION.trySolution(input) and IN_GAME):
		give_strike()

		if ( ACTIVE_TRIES > 0 ):
			load_next_question()
		
	elif (CURRENT_QUESTION.trySolution(input) and ACTIVE_QUESTION < DEF_NUM_QUESTIONS and IN_GAME ):
		load_next_question()

		SCORE_WIDGET.config(text="Player " + str(ACTIVE_PLAYER) + "\'s Turn, " + "Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
		SCORE_WIDGET.update()
def load_window():
	global INPUT_FRAME
	global SCORE_WIDGET
	global SUBMIT_BUTTON
	global ENTRY_FIELD
	global FEEDBACK_FIELD
	global VERSION

	#pack the input frame and the score and tries tracker first
	INPUT_FRAME.pack(side="bottom", anchor="s", fill="x")
	SCORE_WIDGET.pack(side="bottom", anchor="w", fill="x")

	#pack the entry field and button onto their designated frame
	SUBMIT_BUTTON.pack(in_=INPUT_FRAME, side="right", ipady=5, ipadx=5)
	ENTRY_FIELD.pack(in_=INPUT_FRAME, fill="x", ipady=5)

	#then pack the feedback field onto the window!
	FEEDBACK_FIELD.pack(side="top", fill="both", expand=True)


	intro_sequence()

	# and the things to take place whenever the enter button is presssed.
	# you can actually chain together function calls as seen below.
	ENTRY_FIELD.bind("<Return>", lambda event: [check_input(ENTRY_FIELD.get().lower()), ENTRY_FIELD.delete(0, END), ENTRY_FIELD.focus()])

def main():

	load_window()

	MASTER.mainloop()


main()
