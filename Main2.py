from tkinter import *
from Questions import Questions

'''-----------------Global Variables ------------------'''
VERSION = 0.1
ACTIVE_SCORE = 0
DEF_NUM_QUESTIONS = 10
DEFAULT_TRIES = 3
ACTIVE_TRIES = DEFAULT_TRIES
ACTIVE_QUESTION = 0
ASKING_NUM_PLAYERS = FALSE

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
SUBMIT_BUTTON = Button(text="Submit", command=lambda: [send_outputln(FEEDBACK_FIELD, str(ENTRY_FIELD.get())), check_input(ENTRY_FIELD.get()), ENTRY_FIELD.delete(0, END), ENTRY_FIELD.focus()])

# label widget which keeps track of the global variables 
SCORE_WIDGET = Label(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray")

# go ahead and 
CURRENT_QUESTION = Questions()

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

	clear_textbox()

	ACTIVE_SCORE += 10
	ACTIVE_QUESTION += 1 
	CURRENT_QUESTION.getSpecificQuestion(ACTIVE_QUESTION)
	send_outputln(str(ACTIVE_QUESTION) + ". " + str(CURRENT_QUESTION.getQuestion()))

	SCORE_WIDGET.config(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
	SCORE_WIDGET.update()

def give_strike():
	global ACTIVE_SCORE
	global ACTIVE_TRIES
	global IN_GAME
	global SCORE_WIDGET

	ACTIVE_TRIES -= 1

	if ( ACTIVE_TRIES > 1 ):
		SCORE_WIDGET.config(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES))
	elif ( ACTIVE_TRIES == 1):
		SCORE_WIDGET.config(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES))
		SCORE_WIDGET.config(fg="red")
	elif ( ACTIVE_TRIES == 0 ):
		SCORE_WIDGET.config(text="Game Over!  Type \"start\" to play again, or \"quit\" to quit.", fg="white", bg="red")

	SCORE_WIDGET.update()

# when the game ends or if the user gets a game over
# call this method to reset all values to their defaults
# and throw the user back to the first part of the game
def reset_everything(master, SCORE_WIDGET, text):
	global ACTIVE_TRIES
	global ACTIVE_SCORE
	global ACTIVE_QUESTION
	global begun

	begun = False

	# reset the global score and tries to their default values
	ACTIVE_TRIES = DEFAULT_TRIES
	ACTIVE_SCORE = 0
	ACTIVE_QUESTION = 0

	# clear the textbox of any previous feedback 
	clear_textbox(text)

	# display starting text (this is how it will be for now until we get the actual game in)
	# put whatever the intro sequence is here
	intro_sequence(text)

	#reset the text widget back to what it was at the beginning
	SCORE_WIDGET.config(text="Score: " + str(ACTIVE_SCORE) + ", Tries Remaining: " + str(ACTIVE_TRIES), bg="lightgray", fg="black")
	SCORE_WIDGET.update()

def check_input(input):
	global MASTER
	global SCORE_WIDGET
	global ENTRY_FIELD
	global FEEDBACK_FIELD
	global IN_GAME
	global PLAYERS
	global NUM_PLAYERS

	if ( input == "quit" ):
		MASTER.destroy()
	elif ( ASKING_NUM_PLAYERS ):
		NUM_PLAYERS = int(input)

		for i in range(0, NUM_PLAYERS):
			# slot 1 is their tries, slot 2 is their score, slot 3 is their current question
			player_state = [0, 0, 0]


	elif ( input == "begin" and not IN_GAME ):
		clear_textbox()
		send_outputln("How many people are playing?  Type the number below and press ENTER.")
		ASKING_NUM_PLAYERS = True

		# and the things to take place whenever the enter button is presssed.
		# you can actually chain together function calls as seen below.
		# IN_GAME = True
		# clear_textbox()
		# load_next_question()
	elif ( ACTIVE_TRIES == 0 and input == "start"):
		reset_everything(MASTER, SCORE_WIDGET, text)
	elif ( not CURRENT_QUESTION.trySolution(input) and IN_GAME):
		give_strike()
	elif (CURRENT_QUESTION.trySolution(input) and ACTIVE_QUESTION < DEF_NUM_QUESTIONS and IN_GAME ):
		load_next_question()
	# elif ( win condition ):
	# do win condition things

'''-----------------------------------'''

# where the window is set up and such
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

	send_outputln("Start Page")

	# and the things to take place whenever the enter button is presssed.
	# you can actually chain together function calls as seen below.
	ENTRY_FIELD.bind("<Return>", lambda event: [send_outputln(ENTRY_FIELD.get().strip()), check_input(ENTRY_FIELD.get()), ENTRY_FIELD.delete(0, END), ENTRY_FIELD.focus()])

def main():

	load_window()

	MASTER.mainloop()


main()