from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from const import *
from widgets import LabelB, BoardWidget
from run import GameProcessor
from copy import copy

# Window configuration
Config.set('graphics','resizable','0')
Config.set('graphics','width','1200')
Config.set('graphics','height','600')


REGULAR = 1
INVERSE = -1

def another_orientation(orientation):
    if orientation == REGULAR:
    	return INVERSE
    return REGULAR


class Orienteer(object):
    def __init__(self, player_color=WHITE):
        if player_color == WHITE:
        	self.orientation = REGULAR
        else:
        	self.orientation = INVERSE

    def invert(self):
        self.orientation = another_orientation(self.orientation)

    def oriented_board(self,board):
    	orient_board = []
    	if (self.orientation == REGULAR):
        	for i in range(8):
            	for j in range(8):
            		if board.data[i][j] == None:
            			orient_board.append('img/nothing.png')
            		else:
            			figure = board.data[i][j]
            			figure = figurecolor[figure.color] + figuretype[figure.type] 
            			orient_board.append(figure)
            return(orient_board)

        return list(reversed(board))

    def oriented_coordinates(coordinates, board_size):
        if (self.orientation == REGULAR):
            return coordinates
        return board_size - coordinates[0], board_size - coordinates[1]


class MainApp(App):
	def build(self):
		self.start_screen = FloatLayout(
			size_hint=(1, 1),
			pos_hint={'center_x': 0.5, 'center_y': 0.5}
		)

		background_image = Image(
			source=INITIAL_BACKGROUND,
			size_hint=[1, 1],
			pos_hint={'center_x': 0.5, 'center_y': 0.5},
			allow_stretch=True
		)

		game_label = LabelB(
			text='Chess game',
			size_hint=[0.15, 0.1],
			pos_hint={'center_x': 0.7, 'center_y': 0.8},
			color=[0, 0, 0, 1],
			bcolor=[0, 0, 0, 0],
			font_name=FONT,
			font_size=100
		)
		
		self.buttons = BoxLayout(
			orientation='vertical',
			spacing=10,
			size_hint=(0.3, 0.4),
			pos_hint={'center_x': 0.7, 'center_y': 0.4}
		)

		start_game_button = Button(
			text='Start game',
			on_press=self.change_screen,
		    background_normal='',
		    background_color=INITIAL_BUTTON_COLOR,
		    color=[0, 0, 0, 1]
		)

		settings_button = Button(
			text='Settings',
			on_press=self.show_settings,
		    background_normal='',
		    background_color=INITIAL_BUTTON_COLOR,
		    color=[0, 0, 0, 1]
		)
		                   
		exit_button = Button(
			text='Quit',
			on_press=self.leave,
			background_normal='',
			background_color=INITIAL_BUTTON_COLOR,
			color=[0, 0, 0, 1]
		)
		                   
		self.buttons.add_widget(start_game_button)
		self.buttons.add_widget(settings_button)
		self.buttons.add_widget(exit_button)
		
		self.start_screen.add_widget(background_image)
		self.start_screen.add_widget(game_label)
		
		self.start_screen.add_widget(self.buttons)
		self.main_layout = FloatLayout()
		self.main_layout.add_widget(self.start_screen)
		
		return self.main_layout

	def change_screen(self, button):
		self.main_layout.remove_widget(self.start_screen)
		self.draw_game_screen()

	def draw_game_screen(self):

		self.GameProcessor = GameProcessor()
		self.Orienteer = Orienteer()


		self.gameplay = FloatLayout(
			size_hint=[0.5,1],
			pos_hint={'center_x': 0.5, 'center_y': 0.5}
		)

		self.gameplay.add_widget(Image(
			source=GAME_BACKGROUND,
			size_hint=[2,2],
			pos_hint={'center_x': 0.5, 'center_y': 0.5},
			allow_stretch=True
		))

		self.gameplay.add_widget(Button(
			text='Quit',
			on_press=self.leave,
			size_hint=[0.35,0.1],
			pos_hint={'center_x':1.25,'center_y':0.78},
			background_color=GAME_BUTTON_COLOR,
			background_normal=''
		))

		self.gameplay.add_widget(Button(
			text='Restart',
			on_press=self.restart,
			size_hint=[0.35,0.1],
			pos_hint={'center_x':1.25,'center_y':0.90},
			background_color=GAME_BUTTON_COLOR,
			background_normal=''
		))
		self.move_label=LabelB(
			text='',
			bcolor=GAME_BUTTON_COLOR,
			size_hint=[.35,.1],
			pos_hint={'center_x':-0.25,'center_y':0.9}
		)
		self.gameplay.add_widget(self.move_label)
		self.gameplay.add_widget(Button(
			text='Cancel selection',
			on_press=self.cancel_move,
			size_hint=[0.35,0.1],
			pos_hint={'center_x':-0.25,'center_y':0.66},
			background_color=GAME_BUTTON_COLOR,
			background_normal=''
		))
		self.gameplay.add_widget(Button(
			text='Make movement',
			on_press=self.commit_move,
			size_hint=[0.35,0.1],
			pos_hint={'center_x':-0.25,'center_y':0.78},
			background_color=GAME_BUTTON_COLOR,
			background_normal=''
		))
		self.board = BoardWidget(self.Orienteer.oriented_board(self.GameProcessor.board))
		self.gameplay.add_widget(self.board)
		self.main_layout.add_widget(self.gameplay)

	def leave(self, button):
		self.stop()

	def show_settings(self, button):
		self.start_screen.remove_widget(self.buttons)

		self.settings = BoxLayout(
			orientation='vertical',
			spacing=10,
			size_hint=(0.3, 0.4),
			pos_hint={'center_x': 0.7, 'center_y': 0.4})
		crimea = Button(
			text='Whose Crimea?: Russian',
			on_press=self.crimea,
			background_normal='',
			background_color=INITIAL_BUTTON_COLOR,
			color=[0, 0, 0, 1]
		)

		log = Button(
			text='Loging: No',
			on_press=self.loging,
			background_normal='',
			background_color=INITIAL_BUTTON_COLOR,
			color=[0, 0, 0, 1]
		)

		back_to_start_screen = Button(
			text='Back',
			on_press=self.back_to_start,
			background_normal='',
			background_color=INITIAL_BUTTON_COLOR,
			color=[0, 0, 0, 1]
		)
		self.settings.add_widget(crimea)
		self.settings.add_widget(log)
		self.settings.add_widget(back_to_start_screen)
		self.start_screen.add_widget(self.settings)

	def back_to_start(self, button):

		self.start_screen.remove_widget(self.settings)
		self.start_screen.add_widget(self.buttons)

	def crimea(self, button):
		if button.text == 'Whose Crimea?: Russian':
			button.text = 'Whose Crimea?: Ukraine'
		else:
			button.text = 'Whose Crimea?: Russian'

	def loging(self, button):
		if button.text == 'Loging: No':
			button.text = 'Loging: Yes'
		else:
			button.text = 'Loging: No'
	def cancel_move(self, button):
		pass

	def commit_move(self, button):
		pass

	def restart(self, button):
		pass


if __name__ == "__main__":
	app = MainApp()
	app.run()
