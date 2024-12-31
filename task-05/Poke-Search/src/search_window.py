
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import Qt, QRect
from stats import PopupWindow
from display_window import PokeDisplay
import requests
import os.path
import threading
from time import sleep


url = "https://pokeapi.co/api/v2/pokemon"

data = []

WindowWidth = 850
WindowHeight = 500
img_size = 250
marginX = WindowWidth//2-100

if os.path.isfile("assets/pokemon.json"):
	data = eval(open("assets/pokemon.json", "r").read())
else:
	file = open("assets/pokemon.json", "w")
	data = requests.get(url+"?limit=-1").json()
	file.write(str(data))

class SearchWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.w = None
		self.popup_window = None
		self.setFixedSize(WindowWidth, WindowHeight)
		self.setWindowTitle(" ")
		self.setWindowIcon(QIcon("assets/pokeball.png"))

		self.image = QLabel(self)
		self.landingpixmap = QPixmap("assets/landing.jpg")
		self.image.setPixmap(self.landingpixmap)
		self.image.resize(self.landingpixmap.width(), self.landingpixmap.height())
		self.image.setGeometry(0, 0, WindowWidth, WindowHeight)
		self.image.setScaledContents(True)

		self.display_window = None

		self.setStyleSheet("""
			
			QPushButton {
				background-color: dark-grey;
				color: white;
				border: 1px solid #BA263E;
				font: bold 16px;
				text-align: center;
				border-radius: 10px;
			}
					 
			QLineEdit {
				border: 2px solid #BA263E;
				border-radius: 10px;
				padding: 5px;
				text-align: center;
				font: 16px;
			}

			QLabel {
				font-family: "Roboto";
				font-size: 16px;
			}
			QPushButton:hover {
				background-color: #BA263E;
				color: dark-grey;
			}
		""")

		label1 = QLabel("Enter the name", self)
		label1.setGeometry(125, 110, 600, 70)

		self.textbox = QLineEdit(self)
		self.textbox.move(20, 20) 
		self.textbox.setGeometry(50, 175, 250, 40)

		enter_button = QPushButton(text="Search", parent=self)
		enter_button.setGeometry(50, 300, 160, 43)
		enter_button.clicked.connect(self.search)
		
		capture_button = QPushButton("Capture", self)
		capture_button.setGeometry(50, 350, 160, 43)
		capture_button.clicked.connect(self.capture)

		display_button = QPushButton("Display", self)
		display_button.setGeometry(50, 400, 160, 43)
		display_button.clicked.connect(self.display)

		self.stats_button = QPushButton("Stats", self)

		self.table = QLabel(self)
		self.grid = QGridLayout(self)
		self.table.setGeometry(marginX+img_size//2, img_size+10, img_size, 200)
		self.grid.addWidget(self.stats_button, 3, 0, alignment=Qt.AlignCenter)
		self.name = QLabel("Name: ")
		self.grid.addWidget(self.name, 0, 0, alignment=Qt.AlignCenter)
		self.ability = QLabel("Abilities: ")
		self.grid.addWidget(self.ability, 1, 0, alignment=Qt.AlignCenter)
		self.types = QLabel("Types: ")
		self.grid.addWidget(self.types, 2, 0, alignment=Qt.AlignCenter)
		self.pixmap = QPixmap()
		self.table.hide()
		self.table.setLayout(self.grid)
		self.table.setObjectName("table")
		self.table.setStyleSheet("""
			#table {
				font-size: 16px;
				margin: 1px;
				padding: 1px;
				color: white;
				border-radius: 10px;
				border: 1px solid #BA263E;
				background-color: dark-grey;
			}
			
			QPushButton {
				margin-left: 0px;
				margin-right: 0px;
				padding: 8px;
			}
		""")

		self.labelmov = QLabel(self)
		self.labelmov.setScaledContents(True)
		self.movie = QMovie("assets/openingpokeball-pokemon.gif")
		self.labelmov.setGeometry(QRect(0, 0, WindowWidth, WindowHeight))
		self.labelmov.setMovie(self.movie)
		self.labelmov.hide()
		self.movie.frameChanged.connect(self.reset_frame)


	def fetch_pokemon(self, pokemon):
		poke = requests.get(pokemon).json()
		
		self.pixmap.loadFromData(requests.get(poke['sprites']['other']['official-artwork']['front_default']).content)
		self.image.setPixmap(self.pixmap)
		self.image.setGeometry(marginX+img_size//2, 0, img_size, img_size)

		self.name.setText("Name: " + poke['name'].capitalize())
		self.ability.setText("Abilities: " + ", ".join([ability['ability']['name'].capitalize() for ability in poke['abilities']]).replace("-", " "))
		self.types.setText("Types: " + ", ".join([type['type']['name'].capitalize() for type in poke['types']]).replace("-", " "))
		self.stats_button.clicked.connect(lambda: self.ShowStats(poke['stats']))
		self.table.show()
		self.labelmov.hide()
	
	def reset_frame(self, current_frame):
		if current_frame > 55:
			self.movie.stop()

	def search(self):
		name = self.textbox.text()
		hit = False
		for pokemon in data['results']:
			if pokemon['name'] == name:
				hit = True

				self.labelmov.show()
				self.movie.start()
				self.movie.jumpToFrame(0)

				thread = threading.Thread(target=self.fetch_pokemon, args=(pokemon['url'],))
				thread.start()

				break
	
		if not hit:
			self.table.hide()
			self.image.setPixmap(self.landingpixmap)
			self.image.resize(self.landingpixmap.width(), self.landingpixmap.height())
			self.image.setGeometry(0, 0, WindowWidth, WindowHeight)

			error = QMessageBox()
			error.setWindowTitle("Error!")
			error.setText("No such Pokemon found!")
			error.setStandardButtons(QMessageBox.Ok)
			error.setStyleSheet("""
				QMessageBox {
					background-color: dark-grey;
					color: white;
					font: 16px;
					text-align: center;
				}
				QPushButton {
					background-color: #5E81AC;
					color: white;
					border-radius: 8px;
					padding: 5px;
				}
				QPushButton:hover {
					background-color: #81A1C1;
				}
			""")
			error.exec()

	def capture(self):

		message = QMessageBox()
		
		if self.table.isVisible():
			
			if not os.path.isdir("assets/captured"):
				os.mkdir("assets/captured")
			
			name = self.name.text().split(": ")[1]

			if not name+".png" in os.listdir("assets/captured"):
				self.pixmap.save("assets/captured/"+name+".png")
				message.setWindowTitle("Success!")
				message.setText("Pokemon captured!")
			else:
				message.setWindowTitle("Error!")
				message.setText("Pokemon already captured!")
			
		else:
			message.setWindowTitle("Error!")
			message.setText("No Pokemon to capture!")
		
		message.setStyleSheet("""
			QMessageBox {
				background-color: dark-grey;
				color: white;
				font: 16px;
				text-align: center;
			}
			QPushButton {
				background-color: #5E81AC;
				color: white;
				border-radius: 8px;
				padding: 5px;
			}
			QPushButton:hover {
				background-color: #81A1C1;
			}
		""")

		message.setStandardButtons(QMessageBox.Ok)

		x = self.geometry().x() + (self.geometry().width() - message.sizeHint().width()) // 2
		y = self.geometry().y() + (self.geometry().height() - message.sizeHint().height()) // 2

		message.move(x, y)
		message.exec()

	def ShowStats(self, stats):
		if self.popup_window is not None:
			self.popup_window.close()
		self.popup_window = PopupWindow(self.pixmap, stats)
		self.popup_window.show()

	def display(self):
		if len(os.listdir("assets/captured")) == 0:
			message = QMessageBox()
			message.setWindowTitle("Error!")
			message.setText("No Pokemon captured!")
			message.setStyleSheet("""
				QMessageBox {
					background-color: dark-grey;
					color: white;
					font: 16px;
					text-align: center;
				}
				QPushButton {
					background-color: #5E81AC;
					color: white;
					border-radius: 8px;
					padding: 5px;
				}
				QPushButton:hover {
					background-color: #81A1C1;
				}
			""")
			message.setStandardButtons(QMessageBox.Ok)
			message.exec()
			return
		if self.display_window is not None:
			self.display_window.close()
		self.display_window = PokeDisplay()
		self.display_window.show()

if __name__ == "__main__":
	import sys
	from PySide6.QtWidgets import QApplication

	app = QApplication(sys.argv)
	window = SearchWindow()
	window.show()
	sys.exit(app.exec())
