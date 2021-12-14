#-----import statements-----
import turtle
import random
import string
import math

#-----game configuration----
secret = "THE COMPUTER ONLY DOES WHAT YOU TELL IT TO DO"
unique_letters = list(set([x for x in list(secret) if x != " "]))
wrong_letters = [
    x for x in list(string.ascii_uppercase) if x not in unique_letters
]
guessed_so_far = ""
guessed_letters = []
guesses_left = math.floor(len(unique_letters) / 2) - 1
game_over = False
game_won = False

font_size = 12
font_family = "Arial"

panel_shapesize = 5
panel_size = panel_shapesize * 5
start_x = -panel_size * 2.5 - 10
total_panels = len(unique_letters)
current_panel_num = 0
current_correct_letter = ""
current_wrong_letter = ""
panel1_letter = ""
panel2_letter = ""

#-----initialize turtle-----

### Screen Turtle
wn = turtle.Screen()
wn.setup(width=1.0, height=1.0)
wn.addshape("startbutton.gif")
wn.bgpic("squidgame.png")

### Feedback Writer Turtle
writer = turtle.Turtle("blank")
writer.hideturtle()
writer.color("yellow")
writer.penup()
writer.home()
writer.sety(150)

### Panel 1
panel1 = turtle.Turtle("square")
panel1.hideturtle()
panel1.color("gray")
panel1.shapesize(panel_shapesize)
panel1.penup()
panel1.speed(0)

### Panel 1 Writer
panel1_writer = turtle.Turtle("blank")
panel1_writer.hideturtle()
panel1_writer.color("white")

### Panel 2
panel2 = turtle.Turtle("square")
panel2.hideturtle()
panel2.color("gray")
panel2.shapesize(panel_shapesize)
panel2.penup()
panel2.speed(0)

### Panel 2 Writer
panel2_writer = turtle.Turtle("blank")
panel2_writer.hideturtle()
panel2_writer.color("white")

## Player
player = turtle.Turtle("arrow")
player.hideturtle()
player.color("green")
player.penup()
player.goto(start_x - panel_size, 0)

### Start Button Turtle
start = turtle.Turtle("startbutton.gif")


#-----game functions--------
def run_game(x, y):
	start.hideturtle()
	player.showturtle()
	panel1.showturtle()
	panel2.showturtle()
	reveal_letters()
	play_game()



def play_game():
	global game_over
	if (not game_over):
		if (guesses_left > 0):
			write_to_screen(guessed_so_far + "\n\nChoose the next panel wisely.\n(Make sure to click on the panel, not the letter.)\n\nYou have " + str(guesses_left) + " guess(es) left.")
			move_panel_pairs(start_x, 0)
			write_panel_letters(start_x, 0)
		else:
			game_over = True
	else:
		display_results()


def display_results():
	if (game_won == False):
		write_to_screen(guessed_so_far + "\n\nToo bad so sad, you lost.")
	else:
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
	writer.write(phrase, align="center", font=(font_family, font_size, "bold"))


def move_panel_pairs(x, y):
	panel1.goto(x, y)
	panel2.goto(x + panel_size * 4 + 10, y)


def draw_panel_pairs(x, y):
	draw_panel(panel1, x, y)
	draw_panel(panel2, x, y - panel_size)
	player.goto(start_x, 0)


def write_panel_letters(x, y):
	global current_correct_letter, current_wrong_letter, panel1_letter, panel2_letter
	current_correct_letter = get_letter(unique_letters)
	current_wrong_letter = get_letter(wrong_letters)
	heads = random.randint(0, 1)
	if heads == 1:
		panel1_letter = current_correct_letter
		panel2_letter = current_wrong_letter
		print(panel1_letter, panel2_letter)
		write_panel_letter(panel1_writer, x, y, current_correct_letter)
		write_panel_letter(panel2_writer, x + panel_size * 4 + 10, y,current_wrong_letter)
	else:
		print(panel1_letter, panel2_letter)
		panel1_letter = current_wrong_letter
		panel2_letter = current_correct_letter
		write_panel_letter(panel1_writer, x + panel_size * 4 + 10, y,current_wrong_letter)
		write_panel_letter(panel2_writer, x, y, current_correct_letter)


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
	panel_writer.write(letter,align="center",font=(font_family, panel_shapesize * 5, "bold"))


def get_letter(choices):
	letter = random.choice(choices)
	while (letter in guessed_letters):
		letter = random.choice(choices)
	return letter


def panel1_click(x, y):
	check_guess(panel1_letter)


def panel2_click(x, y):
	check_guess(panel2_letter)


def check_guess(guess):
	global guesses_left, guessed_letters
	guessed_letters.append(guess)
	reveal_letters()
	if guess in secret:
		check_solved()
	else:
		guesses_left -= 1

	play_game()


def check_solved():
	global game_over, game_won
	if secret == guessed_so_far:
		game_over = True
		game_won = True


#-----events----------------
write_to_screen(
    "You have " + str(guesses_left) +
    " guesses to solve the secret phrase\n and make it to the other side of the bridge."
)

start.onclick(run_game)
panel1.onclick(panel1_click)
panel2.onclick(panel2_click)

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
