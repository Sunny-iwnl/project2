from tkinter import * 

VERSION = 0.1

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


def main():

	# instantiate the main game window
	master = Tk()
	master.geometry("800x600")
	master.title("Trivia Game v" + str(VERSION))

	input_frame = Frame(master, bg="lightgray")
	entry_field = Entry(text="", relief="groove", highlightbackground="lightgray")
	feedback_field = Text(bg="black", foreground="lightgreen", highlightbackground="black")
	submit_button = Button(text="Submit", command=lambda: [send_outputln(feedback_field, str(entry_field.get())), check_input(master, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])
	score_w = Label(text="Score: " + str(global_score) + ", Tries Remaining: " + str(global_tries), bg="lightgray")

	input_frame.pack(side="bottom", anchor="s", fill="x")
	score_w.pack(side="bottom", anchor="w", fill="x")

	submit_button.pack(in_=input_frame, side="right", ipady=5, ipadx=5)
	entry_field.pack(in_=input_frame, fill="x", ipady=5)
	feedback_field.pack(side="top", fill="both", expand=True)

	send_outputln(feedback_field, "Use the textbox to submit input.")

	entry_field .bind("<Return>", lambda event: [send_outputln(feedback_field, entry_field.get().strip()), check_input(master, feedback_field, entry_field.get()), entry_field.delete(0, END), entry_field.focus()])

	master.mainloop()

main()