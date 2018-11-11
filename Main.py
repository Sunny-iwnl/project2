from tkinter import * 
from Questions import Questions

VERSION = 0.1
DEF_NUM_QUESTIONS = 10
DEFAULT_TRIES = 3

#global variables for the score and the tries for the duration of the game
global_score = 0
global_q_counter = 0
global_tries = DEFAULT_TRIES

begun = False

# keep track of current question
current_q = Questions()
current_q.getSpecificQuestion(1)



def send_output(text, entry):
	text.config(state=NORMAL)
	text.insert(END, str(entry))
	text.see("end")
	text.config(state=DISABLED)

def send_outputln(text, entry):
	text.config(state=NORMAL)
	text.insert(END, str(entry) + "\n")
	text.see("end")
	text.config(state=DISABLED)

def clear_textbox(text):
	text.config(state=NORMAL)
	text.delete('1.0', END)
	text.config(state=DISABLED)


def give_strike(score_w):
	global global_score
	global global_tries
	global begun

	global_tries -= 1
	global_score -= 10

	if ( global_tries > 1 ):
		score_w.config(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries))
	elif ( global_tries == 1):
		score_w.config(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries))
		score_w.config(fg="red")
	elif ( global_tries == 0 ):
		score_w.config(text="Game Over!  Type \"start\" to play again, or \"quit\" to quit.", fg="white", bg="red")

	score_w.update()

#should be whatever the intro sequence for the game is.  
# edit this code accordingly.
def intro_sequence(text):
	send_outputln(text, "Welcome to version " + str(VERSION) + " of our trivia game!  Type \"begin\" to begin, or \"quit\" to quit")

def load_next_question(master, score_w, text):
	global global_score
	global global_q_counter

	clear_textbox(text)

	global_score += 10
	global_q_counter += 1
	current_q.getSpecificQuestion(global_q_counter)
	send_outputln(text, str(global_q_counter+1) + ". " + str(current_q.getQuestion()))
	
	score_w.config(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries), bg="lightgray", fg="black")
	score_w.update()

	defined_winner(text)

def defined_winner(feedback_field):
        global global_score

        if global_score == 70:
                clear_textbox(feedback_field)
                send_outputln(feedback_field, "Congradulations! You have won the game!")
                
                

# when the game ends or if the user gets a game over
# call this method to reset all values to their defaults
# and throw the user back to the first part of the game
def reset_everything(master, score_w, text):
	global global_tries
	global global_score
	global global_q_counter
	global begun

	begun = False

	# reset the global score and tries to their default values
	global_tries = DEFAULT_TRIES
	global_score = 0
	global_q_counter = 0

	# clear the textbox of any previous feedback 
	clear_textbox(text)

	# display starting text (this is how it will be for now until we get the actual game in)
	# put whatever the intro sequence is here
	intro_sequence(text)

	#reset the text widget back to what it was at the beginning
	score_w.config(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries), bg="lightgray", fg="black")
	score_w.update()


def check_input(master, score_w, text, input):
	global global_tries
	global current_q
	global begun

	if ( input == "quit" ):
		master.destroy()
	elif ( input == "begin" and not begun ):
		clear_textbox(text)
		send_outputln(text, str(global_q_counter+1) + ". " + str(current_q.getQuestion()))
		begun = True

	elif ( global_tries == 0 and input == "start"):
		reset_everything(master, score_w, text)
	elif ( not current_q.trySolution(input) and begun):
		give_strike(score_w)
	elif (current_q.trySolution(input) and global_q_counter < DEF_NUM_QUESTIONS and begun ):
		load_next_question(master, score_w, text)


# where the window is set up and such
def main():

	# instantiate the main game window
	master = Tk()
	master.geometry("800x600")
	master.title("Trivia Game v" + str(VERSION))

	# prepare the text field for the feedback to be presented to the user
	feedback_field = Text(bg="black", foreground="lightgreen", highlightbackground="black")

	#create a frame to house the entry field and submit button
	input_frame = Frame(master, bg="lightgray")
	entry_field = Entry(text="", relief="groove", highlightbackground="lightgray")
	submit_button = Button(text="Submit", command=lambda: [check_input(master, score_w, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])

	# label widget which keeps track of the global variables 
	score_w = Label(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries), bg="lightgray")

	#pack the input frame and the score and tries tracker first
	input_frame.pack(side="bottom", anchor="s", fill="x")
	score_w.pack(side="bottom", anchor="w", fill="x")

	#pack the entry field and button onto their designated frame
	submit_button.pack(in_=input_frame, side="right", ipady=5, ipadx=5)
	entry_field.pack(in_=input_frame, fill="x", ipady=5)

	#then pack the feedback field onto the window!
	feedback_field.pack(side="top", fill="both", expand=True)

	# huzzah, our first feedback thingy!
	intro_sequence(feedback_field)

	# and the things to take place whenever the enter button is presssed.
	# you can actually chain together function calls as seen below.
	entry_field .bind("<Return>", lambda event: [check_input(master, score_w, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])
        
	master.mainloop()

main()
