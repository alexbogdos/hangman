# Setup python
import pygame as pyg, sys, random, json

from pygame.locals import *


def _game():
	# initialize pygame
	pyg.init()

	# Surfaces
	pyg.display.set_caption("HangMan")
	pyg.display.set_icon(pyg.image.load('assets/icon.png'))
	window_size = [pyg.display.Info().current_w, pyg.display.Info().current_h]
	screen = pyg.display.set_mode(window_size, pyg.FULLSCREEN)

	# Variables
	scr_size = (screen.get_width(), screen.get_height())
	scr_midle = (scr_size[0] * 0.5, scr_size[1] * 0.5)

	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
				'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	buttons_used = []
	letters = []

	clicking = False

	# Words
	with open('assets/words.txt', 'r') as words_txt:
		txt_data = words_txt.read()
		txt_data = txt_data.split('\n')
		words = []
		for w in txt_data:
			words.append(str(w))

	word = random.choice(words).upper()
	word_Surf = pyg.Surface((48 * len(word) - 16, 100))

	correct_letters = []
	letter_guessed = ""

	if " " in word:
		score = len(word) - word.count(" ")
		tries = len(word) + 3 - word.count(" ")
	else:
		score = len(word)
		tries = len(word) + 3

	if tries > 10:
		tries = 10

	with open('assets/score.json', 'r') as sc_file:
		f = json.load(sc_file)
	score_words = f['score']

	# Colors
	BKG = (100, 100, 100)
	ORANGE = (255, 130, 60)
	BLACK = (0, 0, 0)

	def save_score(target_label, target_var):
		with open('assets/score.json', 'r') as file:
			data = json.load(file)
		data[str(target_label)] = target_var
		with open('assets/score.json', 'w') as file:
			json.dump(data, file)

	def draw_text(string, size, color, pos, surface):
		font = pyg.font.SysFont('Arial', size)
		text = font.render(string, True, color)
		text_rect = text.get_rect()
		text_rect.center = pos
		surface.blit(text, text_rect)
		return text_rect

	n = 0
	running = True
	wt = 0
	while running:
		screen.fill(BKG)
		word_Surf.fill(BKG)
		mouse_pos = pyg.mouse.get_pos()

		draw_text("Correct words: " + str(score_words), 38, ORANGE, (122, 22), screen)
		pyg.draw.line(screen, (190, 190, 190), (0, 44), (246, 44), 2)
		pyg.draw.line(screen, (190, 190, 190), (246, 44), (246, 0), 2)

		for event in pyg.event.get():
			if tries == 0:
				letter_guessed += word
				wt += 1
				if wt == 4:
					pyg.time.delay(1000)
					running = False
					_game()
			if score == 0:
				score_words += 1
				save_score("score", score_words)
				pyg.time.delay(1000)
				running = False
				_game()
			if event.type == QUIT:
				pyg.display.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					save_score("score", 0)
					pyg.display.quit()
					sys.exit()
				elif event.key == K_r:
					save_score("score", score_words)
					_game()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					clicking = True
			else:
				clicking = False

		# Buttons pos and other variables
		x = 1
		xc = - 78
		y = 80
		index = 0
		button_rects = []
		guess = ""

		# Buttons Creation
		for cir in range(26):
			rect = pyg.Rect(x * 114 + xc, 0 + y, 95, 85)
			button_color = (190, 190, 190)
			letter_color = BLACK
			lined = False
			# Checking collision and clicking
			rectColMouse = rect.collidepoint(mouse_pos)
			if rectColMouse and rect not in buttons_used:
				outside_b_color = ORANGE
				if clicking:
					buttons_used.append(rect)
					n += 1
			else:
				outside_b_color = BLACK
			if rect in buttons_used:
				if alphabet[index] not in letters:
					letters.append(alphabet[index])
					guess = alphabet[index]
					if alphabet[index] in word:
						correct_letters.append(rect)
						c_w = word.count(alphabet[index])
						score -= c_w
					if alphabet[index] not in word:
						if tries != 0:
							tries -= 1
				else:
					pass

				if rect in correct_letters:
					button_color = (60, 130, 190)
					outside_b_color = BKG
					letter_color = (205, 205, 205)
					lined = False
				else:
					button_color = ORANGE
					outside_b_color = BKG
					letter_color = (132, 132, 132)
					lined = True

			pyg.draw.rect(screen, outside_b_color, rect, border_radius=15)
			pyg.draw.rect(screen, button_color, rect.copy().inflate(0, -10), border_radius=15)
			draw_text(alphabet[index], 42, letter_color, rect.center, screen)
			if lined:
				rect_line = rect.copy().inflate(-5, -30)
				pyg.draw.line(screen, BLACK, rect_line.topright, rect_line.bottomleft, 5)
			button_rects.append(rect)
			x += 1
			index += 1

			if cir == 12:
				x = 1
				y += 110

		# Text
		draw_text("Guess the word: ", 38, BLACK, (scr_size[0] * 0.5, scr_size[1] - 300), screen)
		# Show tries
		draw_text("You have  __  tries remaining", 42, BLACK, (scr_midle[0], scr_size[1] - 70), screen)
		draw_text(str(tries), 46, ORANGE, (scr_midle[0] - 44, scr_size[1] - 70), screen)

		word_Surf_rect = word_Surf.get_rect()
		word_Surf_rect.center = (scr_size[0] * 0.5, scr_size[1] - 200)

		word_count = word.count(guess)
		for _ in range(word_count):
			letter_guessed += guess

		x_t = 16
		t = 1
		for char in word:
			if char in letter_guessed:
				draw_text(str(char), 48, BLACK, (0 + x_t, 60), word_Surf)
			elif char == " ":
				draw_text(" ", 48, BLACK, (0 + x_t, 60), word_Surf)
			else:
				draw_text("_", 48, BLACK, (0 + x_t, 60), word_Surf)
			t += 1
			x_t += 48

		# Surfaces
		screen.blit(word_Surf, word_Surf_rect)

		pyg.time.Clock().tick(60)
		pyg.display.update()


_game()
