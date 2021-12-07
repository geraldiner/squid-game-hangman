#-----import statements-----
import turtle
import random
import string
import math

#-----game configuration----
secret = "SQUIDWARD SMELLS GOOD"
unique_letters = list(set([x for x in list(secret) if x != " "]))
wrong_letters = [
    x for x in list(string.ascii_uppercase) if x not in unique_letters
]
guessed_so_far = ""
guessed_letters = []
guesses_left = math.floor(len(unique_letters)/2)-1
game_over = False
game_won = False

font_size = 12
font_family = "Arial"

image = "startbutton.gif"

start_x = -200
panel_size = 40
total_panels = len(unique_letters)
current_panel_num = 0
current_correct_letter = ""
current_wrong_letter = ""

#-----initialize turtle-----

### Screen Turtle
wn = turtle.Screen()
wn.setup(width=1.0, height=1.0)
wn.addshape(image)

### Start Button Turtle
start = turtle.Turtle(image)

### Feedback Writer Turtle
writer = turtle.Turtle("blank")
writer.hideturtle()
writer.penup()
writer.home()
writer.sety(150)

### Panel 1
panel1 = turtle.Turtle()
panel1.hideturtle()
panel1.speed(0)

### Panel 1 Writer
panel1_writer = turtle.Turtle("blank")
panel1_writer.hideturtle()

### Panel 2
panel2 = turtle.Turtle()
panel2.hideturtle()
panel2.speed(0)

### Panel 2 Writer
panel2_writer = turtle.Turtle("blank")
panel2_writer.hideturtle()

## Player
player = turtle.Turtle("arrow")
player.hideturtle()
player.penup()
player.goto(start_x - panel_size, 0)


#-----game functions--------
def run_game(x, y):
	global guesses_left, game_over
	start.hideturtle()
	player.showturtle()
	while game_over == False:
		if (guesses_left > 0):
			reveal_letters()
			write_to_screen(
			    guessed_so_far +
			    "\n\nEnter your choice in the console and press ENTER.\n\nYou have "
			    + str(guesses_left) + " guess(es) left.")
			draw_panel_pairs(start_x + (panel_size * current_panel_num),
			                 panel_size)
			write_panel_letters(start_x + (panel_size * current_panel_num),
			                    panel_size)
			user_guess = input("Type a letter and press ENTER. ").upper()
			if (user_guess == ""):
				print("You just gave up a guess. -1 guess\n")
				guesses_left -= 1
			elif (not user_guess.isalpha()):
				print("Your guess must be a letter. -1 guess\n")
				guesses_left -= 1
			elif (user_guess != current_correct_letter
			      and user_guess != current_wrong_letter):
				print("You must choose between the given letters. -1 guess\n")
				guesses_left -= 1
			else:
				check_guess(user_guess)
		else:
			game_over = True
			write_to_screen(guessed_so_far + "\n\nToo bad so sad, you lost.")
	if (game_won == False):
		write_to_screen(guessed_so_far + "\n\nToo bad so sad, you lost.")
	else:
		player.goto(
		    start_x + (panel_size / 2) + (panel_size * current_panel_num), 0)
		write_to_screen(guessed_so_far +
		                "\n\nCongratulations, you made it across alive.")


def reveal_letters():
	global guessed_so_far
	guessed_so_far = ""
	for letter in secret:
		if letter == " ":
			guessed_so_far += " "
		elif letter in guessed_letters:
			guessed_so_far += letter
		else:
			guessed_so_far += "_"


def write_to_screen(phrase):
	writer.clear()
	writer.write(phrase,
	             align="center",
	             font=(font_family, font_size, "normal"))


def draw_panel_pairs(x, y):
	draw_panel(panel1, x, y)
	draw_panel(panel2, x, y - panel_size)
	player.goto(start_x + (panel_size * current_panel_num), 0)


def write_panel_letters(x, y):
	global current_correct_letter, current_wrong_letter
	current_correct_letter = get_letter(unique_letters)
	current_wrong_letter = get_letter(wrong_letters)
	heads = random.randint(0,1)
	if heads == 1:
		write_panel_letter(panel1_writer, x + (panel_size / 2),
		                   y - (panel_size / 2), current_correct_letter)
		write_panel_letter(panel2_writer, x + (panel_size / 2),
		                   y - panel_size - (panel_size / 2),
		                   current_wrong_letter)
	else:
		write_panel_letter(panel1_writer, x + (panel_size / 2),
		                   y - (panel_size / 2), current_wrong_letter)
		write_panel_letter(panel2_writer, x + (panel_size / 2),
		                   y - panel_size - (panel_size / 2),
		                   current_correct_letter)


def draw_panel(panel, x, y):
	panel.penup()
	panel.goto(x, y)
	panel.pendown()
	panel.fillcolor("gray")
	panel.begin_fill()
	for i in range(4):
		panel.forward(panel_size)
		panel.right(90)
	panel.end_fill()


def write_panel_letter(panel_writer, x, y, letter):
	panel_writer.clear()
	panel_writer.penup()
	panel_writer.goto(x, y)
	panel_writer.pendown()
	panel_writer.write(letter,
	                   align="center",
	                   font=(font_family, font_size, "normal"))


def get_letter(choices):
	letter = random.choice(choices)
	while (letter in guessed_letters):
		letter = random.choice(choices)
	return letter


def check_guess(guess):
	global guesses_left, guessed_letters, current_panel_num
	guessed_letters.append(guess)
	reveal_letters()
	check_solved()

	if guess in secret:
		print("YOU MAY PROCEED.\n")
		current_panel_num += 1
	else:
		print("TOO BAD, SO SAD. TRY AGAIN.\n")
		guesses_left -= 1


def check_solved():
	global game_over, game_won
	if secret == guessed_so_far:
		game_over = True
		game_won = True
		return


#-----events----------------
write_to_screen(
    "You have " + str(guesses_left) +
    " guesses to solve the secret phrase\n and make it to the other side of the bridge."
)

start.onclick(run_game)

wn.listen()
wn.mainloop()

#-----plan----------------
# Hangsquid
# word to be guessed (string) = Secret
# limited number of guesses (number) = TryCount
# letters guessed (list) = LettersGuessed
# glass panels to get across
# while TryCount > 0
# - 1 panel has a correct letter, 1 panel is a wrong letter
# player has to guess a letter by "stepping" on one of the panels
# - onclick event on panels
# - if player clicks the panel with the correct letter
# -- move forward/respawn to next choice
# - if it's wrong
# -- -1 TryCount, update panel choices to new letters
#
# if TryCount == 0 and secret not guessed, player lose & game over
# if TryCount > 0 and secret is guessed, player wins & game over

# [A]    [E]
# [S] -> [Z]
