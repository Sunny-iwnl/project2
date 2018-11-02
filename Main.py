from tkinter import * 

VERSION = 0.1


#global variables for the score and the tries for the duration of the game
global_score = 0
global_tries = 3


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

def check_input(master, text, input):
	if ( input == "quit" ):
		master.destroy()
	if ( input == "clear" ):
		clear_textbox(text)


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
	submit_button = Button(text="Submit", command=lambda: [send_outputln(feedback_field, str(entry_field.get())), check_input(master, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])

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
	send_outputln(feedback_field, "Use the textbox to submit input.")

	# and the things to take place whenever the enter button is presssed.
	# you can actually chain together function calls as seen below.
	entry_field .bind("<Return>", lambda event: [send_outputln(feedback_field, entry_field.get().strip()), check_input(master, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])

	master.mainloop()

main()