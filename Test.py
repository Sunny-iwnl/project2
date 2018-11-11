from tkinter import *
from Questions import Questions
from player import Player
from PIL import ImageTk, Image
import sys
import os.path


INSTALL_DIR = os.getcwd() + "/"

class Application:

    def __init__(self, master):
        self.master = master
        self.VERSION = 1.0
        self.PROGRAM_TITLE = "Hack Your Boss: Trivia Edition, v" + str(self.VERSION)
        self.DEFAULT_QUESTIONS = 9

        # instantiate the main game window
        self.master.geometry("800x600")
        self.master.title(self.PROGRAM_TITLE)
        self.master.config(bg="black")

        ''' ------- Window Element Variables -------- '''

        # prepare the text field for the feedback to be presented to the user
        self.feedback_field = Text(bg="black", foreground="#33FF00", highlightbackground="black")

        # load the fonts on macOS and Windows most similar to the font the scene pictures use.
        if ( sys.platform == 'darwin' ):
            self.feedback_field.config(font=("Andale Mono", 14))
        elif ( sys.platform == 'win32' ):
            self.feedback_field.config(font=("Lucida Console", 14))

        #create a frame to house the entry field and submit button
        self.input_frame = Frame(master, bg="lightgray")
        self.entry_field = Entry(text="", relief="groove", highlightbackground="lightgray", disabledbackground="darkgray")
        self.submit_button = Button(text="Submit", command=lambda: self.submit_input(self.entry_field.get().lower()))
        # label widget which keeps track of the global variables 
        self.score_widget = Label(text="Score: " + str(0) + ", Tries Remaining: " + str(3), bg="lightgray")
        self.panel = Label(self.master, bg="black")

        ''' ----------------------------------- '''

        ''' ------- "Global" Variables -------- '''

        #self.input = ""
        self.in_game = False
        self.asking_num_players = False
        self.num_players = 0
        self.active_player = Player("Player 1", 1)
        self.curr_question = Questions()
        self.q_counter = 0

        ''' ----------------------------------- '''

        self.program()

        self.entry_field.bind("<Return>", lambda event: self.submit_input(self.entry_field.get().lower()))

    def boot_os_sequence(self):
        self.load_console()
        self.load_os_sequence()
        self.unload_console()

    def program(self):
        #self.boot_os_sequence()
        self.title_screen()

    def update_scene(self, milsec, filename):
        self.img = ImageTk.PhotoImage(Image.open(INSTALL_DIR + filename))
        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.master.after(milsec, self.panel.config(image = self.img))
        self.master.update()

    def load_scene_widget(self, spec_relx, spec_rely):
        self.panel.place(relx=spec_relx, rely=spec_rely, anchor=CENTER)

    def unload_scene_widget(self):
        self.panel.place_forget()

    def update_score_widget(self):
        self.score_widget.config(text="Score: " + str(self.active_player.getScore()) + ", Tries Remaining: " + str(self.active_player.getTries()))

    def reset_states(self):
        # self.input = ""
        self.in_game = False
        self.asking_num_players = False
        self.num_players = 0
        self.active_player = Player("Player 1", 1)
        self.q_counter = 0
        self.curr_question = Questions()
        self.clear_console()
        self.score_widget.config(text="Score: " + str(0) + ", Tries Remaining: " + str(3), fg="black", bg="lightgray")
        self.unload_score_widget()
        self.unload_entry_field()
        self.unload_scene_widget()
        self.load_console()
        self.master.after(3000, self.send_outputln("Restarting system..."))
        self.unload_console()

    # def submit_input(self):
    #     self.input = self.entry_field.get().lower()
    #     self.entry_field.delete(0, END)
    #     self.entry_field.focus()
    #     self.check_input()

    def submit_input(self, entry):
        self.entry_field.delete(0, END)
        self.entry_field.focus()
        self.check_input(entry)

    def check_input(self, entry):
        if ( entry == "about" ):
            about = Toplevel(self.master)
            about.geometry("250x250")
            about_text = Label(about, text=self.PROGRAM_TITLE)
            ok_button = Button(about, text="ok", command=lambda: about.destroy())

            about_text.pack(side="top")
            ok_button.pack(side="top")
            

            about.mainloop()

        if ( not self.in_game ):
            if ( self.asking_num_players ):
                try:
                    self.num_players = int(entry)
                    self.send_outputln(entry)
                except ValueError:
                    self.send_outputln("\"" + entry + "\" is not a valid number of players.")
                    self.send_output("> ")
                else:
                    # self.start_game()

                    if ( self.num_players == 1 ):
                        self.start_game()
                    elif ( self.num_players > 1 ):
                        self.send_outputln("Multiplayer not yet implemented.")
                        self.send_output("> ")
                    # elif ( self.num_players > 1 ):
                    #     i = 1
                    #     while (i <= self.num_players):
                    #         new_player = Player("Player " + str(i), i)
                    #         new_player.setPrev(self.active_player)
                    #         self.active_player.setNext(new_player)
                    #         i+=1

                    #     i = 1
                    #     temp = self.active_player
                    #     while (i <= self.num_players):
                    #         print( temp.getName())
                    #         temp = temp.getNext()
                    #         i+=1

                        
            elif ( not self.asking_num_players ):
                if (entry == "start"):
                    self.reset_states()
                    self.player_start_screen()
        elif ( self.in_game ):
            if ( self.num_players == 1 ):
                if ( self.q_counter <= self.DEFAULT_QUESTIONS ):
                        # if (self.curr_question.trySolution(self.input)):
                        result = self.curr_question.trySolution(entry)
                        self.active_player.update(result, self.curr_question.getPointValue())
                        self.update_score_widget()

                        if ( self.active_player.getTries() > 0 ):
                            if ( self.active_player.getTries() == 1 ):
                                self.score_widget.config(fg="red")
                            if ( self.q_counter < self.DEFAULT_QUESTIONS ):
                                if ( result ):
                                    self.get_next_question()
                            elif ( self.q_counter >= self.DEFAULT_QUESTIONS ):
                                self.win_sequence()
                        elif ( self.active_player.getTries() == 0 ):
                            self.game_over_sequence()


            # if ( self.input == "right" ):
            #     self.send_outputln("we are in game and this would be a correct answer")
            # elif ( self.input == "game over" ):
            #     self.game_over_sequence()
            # elif ( self.input == "win" ):
            #     self.win_sequence()

    ''' ------- TITLE SCREEN FUNCTIONS -------- '''

    def title_screen(self):
        # self.panel.pack(side = "top", anchor="n", fill = "both", expand="yes")
        self.load_scene_widget(0.5,0.38)
        self.update_scene(0, "home.png")

        # set the start button to destroy the title screen when it is clicked.
        # i am still working out the logic for what i want to happen next.
        self.start_button = Button(text="Start Game", command=lambda: self.oh_no_sequence())
        self.skip_button = Button(text="Skip to Game", command=lambda: [self.unload_title_screen(), self.player_start_screen()])
        self.start_button.pack(side=BOTTOM, anchor="se", ipadx=5, ipady=5, pady=10)
        self.skip_button.pack(side=BOTTOM, anchor="sw", ipadx=5, ipady=5, pady=10)
        # self.img = ImageTk.PhotoImage(Image.open(INSTALL_DIR + "home.png"))
        # #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        # self.panel = Label(self.master, image = self.img, bg = "black")

        #The Pack geometry manager packs widgets in rows or columns.
        # self.panel.place()

    def unload_title_screen(self):
        self.unload_scene_widget()
        self.start_button.pack_forget()
        self.skip_button.pack_forget()
        # self.load_interface()

    ''' --------------------------------------- '''

    ''' ------- CONSOLE SCREEN FUNCTIONS -------- '''
    def send_output(self, string):

        self.feedback_field.config(state=NORMAL)
        self.feedback_field.insert(END, str(string))
        self.feedback_field.see("end")
        self.feedback_field.config(state=DISABLED)
        self.feedback_field.update()

    def send_outputln(self, string):

        self.feedback_field.config(state=NORMAL)
        self.feedback_field.insert(END, str(string) + "\n")
        self.feedback_field.see("end")
        self.feedback_field.config(state=DISABLED)
        self.feedback_field.update()

    def clear_console(self):
        self.feedback_field.config(state=NORMAL)
        self.feedback_field.delete('1.0', END)
        self.feedback_field.config(state=DISABLED)
        self.feedback_field.update()

    def load_console(self):
        self.feedback_field.pack(side="top", fill="both", expand=True, ipadx=20, ipady=20)

    def load_entry_field(self):
        #pack the input frame and the score and tries tracker first
        self.input_frame.pack(side="bottom", anchor="s", fill="x")

        #pack the entry field and button onto their designated frame
        self.submit_button.pack(in_=self.input_frame, side="right", ipady=5, ipadx=5)
        self.entry_field.pack(in_=self.input_frame, fill="x", ipady=5)

    def unload_console(self):
        self.feedback_field.pack_forget()

    def unload_entry_field(self):
        self.submit_button.pack_forget()
        self.entry_field.pack_forget()
        self.input_frame.pack_forget()

    def disable_entry_field(self):
        self.entry_field.config(state=DISABLED)
        self.submit_button.config(state=DISABLED)

    def enable_entry_field(self):
        self.entry_field.config(state=NORMAL)
        self.submit_button.config(state=NORMAL)

    def unload_game_interface(self):
        self.unload_console()
        self.unload_entry_field()

    def load_game_interface(self):
        self.load_entry_field()
        self.load_console()

    def load_score_widget(self):
        self.score_widget.pack(side="bottom", anchor="w", fill="x")

    def unload_score_widget(self):
        self.score_widget.pack_forget()


    def start_game(self):
        self.asking_num_players = False
        self.in_game = True

        self.clear_console()
        self.unload_console()
        self.load_score_widget()
        self.load_console()
        self.disable_entry_field()

        if ( self.num_players > 1 ):
            self.master.after(2000, self.send_outputln("Number of players: " + str(self.num_players)))
        self.master.after(3000, self.send_outputln("Loading security questions..."))
        self.clear_console()
        self.enable_entry_field()

        if ( self.num_players == 1 ):
            self.get_next_question()

    def get_next_question(self):
        self.clear_console()
        self.q_counter += 1
        self.curr_question.getSpecificQuestion(self.q_counter)
        self.send_outputln(str(self.q_counter) + ". " + self.curr_question.getQuestion())


    ''' --------------------------------------- '''

    ''' ------- GAME RELATED FUNCTIONS -------- '''
    # loads the "operating system" to lead into the game title screen
    def game_over_sequence(self):
        self.in_game = False
        self.unload_game_interface()
        self.unload_score_widget()
        self.load_scene_widget(0.5, 0.38)
        self.load_entry_field()
        self.load_score_widget()
        self.disable_entry_field()
        self.master.after(0, self.score_widget.config(text=self.det_losers(), fg="white", bg="darkred"))
        
        self.update_scene(0, "access_d.png")
        self.update_scene(3000, "access_d2.png")
        self.enable_entry_field()
        # self.master.after(5000, self.unload_scene_widget())
        # self.master.after(3000, self.player_start_screen())
        # self.reset_states()
        # self.load_os_sequence()
        # self.instr_and_playernum_screen()


    # accounts for ties if there is more than one player
    def get_winners(self):
        winners = []

        for i in range(self.num_players):
            winners.append(i+1)

        return winners

    def get_losers(self):
        losers = []

        for i in range(self.num_players):
            losers.append(i+1)

        return losers

    def det_losers(self):

        res_str = ""
        if ( self.num_players == 1 ):
            res_str += "You"
            #self.send_output("You")
        elif ( self.num_players > 1 ):
            loser = self.get_losers()
            if ( len(loser) == 1 ):
                res_str += "Player " + str(loser[0])
                #self.send_output("Player " + str(winner[0]))
            elif( len(loser) > 1 ):
                res_str += "Player(s) "
                #self.send_output("Player(s) ")
                for i in range(len(loser)-1):
                     res_str += str(loser[i]) + ", "
                     #self.send_output(str(winner[i]) + ", ")
                res_str += "and " + str(loser[len(loser)-1])
                #self.send_output(str(winner[len(winner)-1]))
        res_str += " ran out of attempts, system locked!"
        
        return res_str

    def det_winner(self):

        res_str = ""
        if ( self.num_players == 1 ):
            res_str += "You"
            #self.send_output("You")
        elif ( self.num_players > 1 ):
            winner = self.get_winners()
            if ( len(winner) == 1 ):
                res_str += "Player " + str(winner[0])
                #self.send_output("Player " + str(winner[0]))
            elif( len(winner) > 1 ):
                res_str += "Player(s) "
                #self.send_output("Player(s) ")
                for i in range(len(winner)-1):
                     res_str += str(winner[i]) + ", "
                     #self.send_output(str(winner[i]) + ", ")
                res_str += "and " + str(winner[len(winner)-1])
                #self.send_output(str(winner[len(winner)-1]))
        res_str += " won!"
        
        return res_str
        # self.score_widget.config(text=res_str)
        # self.score_widget.update()
        #self.send_outputln(" won!")

    # loads the "operating system" to lead into the game title screen
    def win_sequence(self):
        self.in_game = False
        self.clear_console()

        self.master.after(3000, self.score_widget.config(text=self.det_winner(), fg="white", bg="darkgreen"))
        self.unload_game_interface()
        self.unload_score_widget()
        self.load_scene_widget(0.5, 0.38)
        self.load_entry_field()
        self.load_score_widget()
        self.disable_entry_field()
        self.update_scene(0, "access_g.png")
        self.update_scene(3000, "access_g2.png")
        self.enable_entry_field()
        # self.master.after(5000, self.unload_scene_widget())
        # self.master.after(3000, self.player_start_screen())
        # self.reset_states()
        # self.load_os_sequence()
        # self.instr_and_playernum_screen()


    def load_os_sequence(self):
        self.clear_console()
        self.master.after(2000, self.send_outputln("Starting operating system..."))
        self.master.after(1000, self.send_output("|-> Loading base system... "))
        self.master.after(2000, self.send_outputln("DONE."))

        self.master.after(1000, self.send_output("|-> Loading command acceptance module... "))
        self.master.after(2000, self.send_outputln("DONE."))

        self.master.after(1000, self.send_output("|-> Loading connection to database... "))
        self.master.after(2000, self.send_outputln("DONE."))

        self.master.after(3000, self.send_outputln("|-> Loading user account BESTBOSS4EVER... "))
        self.master.after(1500, self.clear_console())

    def send_email(self):
        self.send_output("Sending email to YOUR BOSS in ")

        self.master.after(2000, self.send_output("3... "))
        self.master.after(2000, self.send_output("2... "))
        self.master.after(2000, self.send_outputln("1... "))
        self.master.after(2000, self.send_outputln("Email sent."))
        self.master.after(3000, self.clear_console())

    def oh_no_sequence(self):
        self.unload_title_screen()
        # self.load_game_interface()
        # self.disable_entry_field()
        self.load_console()
        self.send_email()
        self.unload_console()
        # self.unload_game_interface()
        self.load_scene_widget(0.5, 0.5)
        self.update_scene(0, "dialogue1.png")
        self.update_scene(5000, "dialogue2.png")
        self.master.after(5000, self.unload_scene_widget())
        self.master.after(3000, self.player_start_screen())

    def player_start_screen(self):
        self.load_game_interface()
        self.clear_console()

        #pack the entry field and button onto their designated frame
        self.disable_entry_field()   
        self.send_outputln("Welcome to OS-329E, BESTBOSS4EVER.")
        self.send_outputln("Your account has been locked.  Verification is required to regain access.")
        self.send_outputln("")
        self.send_outputln("Answer the following \"security\" questions to gain access to this user account.")
        self.send_outputln("Use the textbox below to type your responses.  Either press the ENTER key or click the \"Submit\" button to submit your response.")
        self.send_outputln("")
        self.send_outputln("========== BE CAREFUL! ==========")
        self.send_outputln("You have 3 tries to answer all the questions succesfully!  If you run out of attempts, the computer will lock itself and it will be GAME OVER.\n")
        self.send_outputln("\n-------------------------------\n")
        self.master.after(3000, self.send_outputln("Starting command line...\n"))
        self.ask_num_players()

    def ask_num_players(self):
        self.asking_num_players = True
        self.send_outputln("How many players will be playing?")
        self.send_outputln("Enter a number below, then either press ENTER or click the \"Submit\" button to submit your response.")
        self.send_output("> ")
        self.enable_entry_field()
    ''' --------------------------------------- '''

root = Tk()
my_gui = Application(root)
root.mainloop()
